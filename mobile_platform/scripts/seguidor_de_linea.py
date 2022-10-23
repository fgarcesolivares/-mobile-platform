# Author: Fredys Garces
# Description: Subscritor/publicador seguidor de linea

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




def main(args=None):
  
  # Initialize the rclpy library
  rclpy.init(args=args)
  
  # Create the node
  follower = LineFollower()
   #image_subscriber = ImageSubscriber()
  # Spin the node so the callback function is called.
  rclpy.spin(follower)
   #rclpy.spin(image_subscriber)
 
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  follower.destroy_node()
   #image_subscriber.destroy_node()
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()
