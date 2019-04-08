
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 20:08:29 2019

@author: ajain
"""
import cv2
import numpy as np
import win32api,win32con

cap = cv2.VideoCapture(0)

lower_red = np.array([170,75,190])
upper_red = np.array([180,255, 255])
'''
lower_green= np.array([45,60,100])
upper_green= np.array([75,255, 255])   ''' 
points = []
ret , frame = cap.read()
Height, Width =frame.shape[:2]
frame_count = 0


while True:
    ret , frame = cap.read()
    
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask1 = cv2.inRange(hsv_img, lower_red, upper_red)
   
    r , thresh1 = cv2.threshold(mask1, 150, 255, 0)
    _, contours, heirarchy = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    center = int(Height/2), int(Width/2)
    if len(contours) >0:
        
        c =max(contours, key =cv2.contourArea)
        (x,y), radius = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        try:
            center =(int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
        except:
            center = int(Height/2), int(Width/2)
    if radius >5:
        
        cv2.circle(frame, (int(x),int(y)), int(radius),(0,0,255),2)
        cv2.circle(frame, center, 5, (0,255,0), -1)
        
    points.append(center)
    
    win32api.SetCursorPos((x,y))
    res1 = cv2.bitwise_and(frame, frame, mask=mask1)
    cv2.drawContours(res1, contours, -1, (0,255,0),3)
    
    print(center[0],center[1])
      
      
    """ 
    mask2 = cv2.inRange(hsv_img, lower_green, upper_green)
    res2 = cv2.bitwise_and(frame, frame, mask=mask2)
    
    r , thresh2 = cv2.threshold(mask2, 200, 255, 0)
    _, contours, heirarchy = cv2.findContours(thresh2.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    """
   
 #   cv2.drawContours(res2, contours, -1, (0,255,0),3)
    cv2.imshow("original", frame)
   # cv2.imshow("mask1", mask1)
    #cv2.imshow("final1",res1)
   # cv2.imshow("mask2", mask2)
    #cv2.imshow("final2",res2)
    if cv2.waitKey(1) == 13:
        break;

cap.release()
cv2.destroyAllWindows()
