#Author: Fredys Garces Olivares

# Importo librerias necesarias
import rclpy 
from rclpy.node import Node 
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge
import cv2 
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
import numpy as np


class LineFollower(Node):
    """ Creo una clase de tipo seguidor de linea"""
    def __init__(self):
     super().__init__('follower') 
     self.bridge = CvBridge()
     cv2.namedWindow("window", 1)
     

     self.image_sub = self.create_subscription(Image, 'camera1/image_raw',self.image_callback,rclpy.qos.qos_profile_sensor_data)
     self.image_sub

     self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', rclpy.qos.qos_profile_system_default)
     self.cmd_vel_pub
     
     self.twist = Twist()
     self.twist


    def image_callback(self, msg):

        image = self.bridge.imgmsg_to_cv2(msg)
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        #Defino limites de mi mascara
        light_white = (0, 0, 200)
        dark_white = (145, 60, 255)
        mask_white = cv2.inRange(hsv, light_white, dark_white)
        result_white = cv2.bitwise_and(image, image, mask=mask_white)
        h, w, d = image.shape
        search_top = int( 3*h/4)
        search_bot = int(3*h/4 + 20)
        result_white[0:search_top, 0:w] = 0
        result_white[search_bot:h, 0:w] = 0

        M = cv2.moments(mask_white)
        if M['m00'] > 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(image, (cx, cy), 20, (0,255,0), -1)
#The proportional controller is implemented in the following four lines which
#is reposible of linear scaling of an error to drive the control output.
        err = cx - w/2
        self.twist.linear.x = 0.2
        self.twist.angular.z = -float(err) / 100
        self.cmd_vel_pub.publish(self.twist)
        cv2.imshow("window", image)
        cv2.waitKey(3)

class ImageSubscriber(Node):
  """
  Create an ImageSubscriber class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('object_detection')
      
    # Create the subscriber. This subscriber will receive an Image
    # from the video_frames topic. The queue size is 10 messages.
    #se crea un objeto suscriptor, se suscribe al topic donde está publicando el rosbag
    self.subscription = self.create_subscription(
      Image, 
      '/camera1/image_raw', 
      self.listener_callback, 
      rclpy.qos.qos_profile_sensor_data)

    self.subscription # prevent unused variable warning
    
    #se crea un objeto publicador, con el cual se publicarán los datos procesados
    self.publisher_ = self.create_publisher(Image, 'obj_detection', rclpy.qos.qos_profile_system_default)
    
    # We will publish a message every 0.1 seconds
    
     
    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()

  def listener_callback(self, data):
    
        #self.frame = self.br.imgmsg_to_cv2(data)
        #self.frame = data
        
        # Display the message on the console
        self.get_logger().info('Receiving video frame')
    
        # Convert ROS Image message to OpenCV image
        cap = self.br.imgmsg_to_cv2(data)

########################################
        # Capture video from file
        #cap = cv2.VideoCapture(2)

        azulBajo = (100,100,20)
        azulAlto = (125,255,255)
        light_white = (0, 0, 200)
        dark_white = (145, 60, 255)
        while True:

            frame = cap
            ret =1
            if ret == 1:
                frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(frameHSV,light_white,dark_white)
                contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for c in contornos:
                    area=cv2.contourArea(c)
                    if area > 3000:
                        M=cv2.moments(c)
                        if (M["m00"]==0): M["m00"]=1
                        x=int(M["m10"]/M["m00"])
                        y=int(M["m01"]/M["m00"])
                        cv2.circle(frame,(x,y),7,(0,255,0),-1)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(frame,'{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
                        nuevoContorno=cv2.convexHull(c)
                        cv2.drawContours(frame, [nuevoContorno], 0, (255,0,0), 3)


                
                cv2.imshow('frame',frame)
                imagen=self.br.cv2_to_imgmsg(frame)
                imagen.header.frame_id= 'base_link'
                self.publisher_.publish(imagen)
                        
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    break
            
        cap.release()
        cv2.destroyAllWindows()


def main(args=None):
  
  # Initialize the rclpy library
  rclpy.init(args=args)
  
  # Create the node
  follower = LineFollower()
  image_subscriber = ImageSubscriber()
   #image_subscriber = ImageSubscriber()
  # Spin the node so the callback function is called.
  rclpy.spin(image_subscriber)
  rclpy.spin(follower)
  
   
 
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  follower.destroy_node()
  image_subscriber.destroy_node()
  
   #image_subscriber.destroy_node()
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()
