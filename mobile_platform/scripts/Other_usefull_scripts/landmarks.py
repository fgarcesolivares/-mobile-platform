#Author: Fredys Garces Olivares

# install opencv "pip install opencv-python"
from turtle import distance
import numpy as np
import cv2 
 
# Capture video from file
cap = cv2.VideoCapture(2)

# Colors
GREEN = (0, 255, 0)
RojoOscuro = np.array([8, 255, 255],np.uint8)
RojoClaro = np.array([0, 100, 20],np.uint8)

# defining the fonts
fonts = cv2.FONT_HERSHEY_COMPLEX

measured_distance = 50
real_width = 20

while True:

    ret, frame = cap.read()

    if ret == True:
        frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(frameHSV,RojoClaro,RojoOscuro)
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
                cv2.drawContours(frame, [nuevoContorno], 0, (0,0,255), 3)

            cv2.imshow('frame',frame)
            print(str(distance))            
            #cv2.putText(
            #frame, f"Distance: {round(distance,2)} CM", (30, 35),
            #fonts, 0.6, GREEN, 2)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
    
 
    # focal length finder function
    def FocalLength(measured_distance, real_width, width_in_rf_image):
        focal_length = (width_in_rf_image* measured_distance)/ real_width
        return focal_length

    # distance estimation function
    def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):
        distance = (real_face_width * Focal_Length)/face_width_in_frame
        return distance
            
                
 