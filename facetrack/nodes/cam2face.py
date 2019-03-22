#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import sys
import numpy as np

face_cascade = cv2.CascadeClassifier('/home/tommy/rostest/src/facetrack/src/cascades/data/haarcascade_eye.xml')

def callback(data):
    br = CvBridge()
    #print ("reciving image")
    data1 = br.imgmsg_to_cv2(data)
    gray = cv2.cvtColor(data1, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.7, minNeighbors=5)
    for (x, y, w, h) in faces:
        #print(x,y,w,h)
        roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
        roi_color = data1[y:y+h, x:x+w]

        colorss = (255, 0, 0) #BGR 0-255
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(data1, (x, y), (end_cord_x, end_cord_y), colorss, stroke)

    cv2.imshow("camera", data1 )
    cv2.waitKey(1)

def listener():

    rospy.init_node('listener', anonymous=True)
    topicss = "/usb_cam/image_raw"

    rospy.Subscriber(topicss, Image, callback)
    rospy.spin()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    listener()
