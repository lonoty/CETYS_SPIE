#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import sys
import copy
import numpy as np
global center
global error
global lineheight
lineheight = 300
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def callback(data):
    global center
    br = CvBridge()
    #print ("reciving image")
    data1 = br.imgmsg_to_cv2(data, desired_encoding="bgr8")
    data2 = copy.deepcopy(data1)
    gray = cv2.cvtColor(data1, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape
    roi = gray[ lineheight:lineheight +20, 0:width]
    lower_black = np.array([0], dtype = "uint16")
    upper_black = np.array([50], dtype = "uint16")
    black_mask = cv2.inRange(roi, lower_black, upper_black)
    edges = cv2.Canny(black_mask, 100, 255)
    roiheight, roiwidth = roi.shape
    edgeloc = np.transpose(np.nonzero(edges))

    if edgeloc.size != 0:
        count = 0
        total = 0
        for i in range(roiheight):
            m = [i[1] for i in edgeloc if i[0] == 1]
            if m:
                mmax = np.max(m)
                mmin = np.min(m)
                count = count +1
                mid = (mmax + mmin)/2
                total = total + mid

        if count != 0:
            center = total/count
            modcenter= int(translate(center, 0, 640, 90, 138))
            print(modcenter)

    cv2.line(data1, (center, 0), (center, height), (0,255,0), 2)
    cv2.imshow('mask0',edges)
    cv2.imshow('masks0',data2)
    cv2.imshow('mask1',gray)
    cv2.imshow('Canny', edges)
    cv2.imshow('mask0',black_mask)
    cv2.imshow("camera", roi )
    cv2.imshow("yay", data1)
    #print(edgeloc)
    cv2.waitKey(1)

def listener():

    rospy.init_node('linedetect')
    topicss = "/usb_cam/image_raw"
    rospy.Subscriber(topicss, Image, callback)
    rospy.spin()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    listener()
