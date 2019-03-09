#!/usr/bin/env python
import rospy , struct
import serial, time
from sensor_msgs.msg import Joy
from std_msgs.msg import Int16


def callback(data):

    speed = int(((data.axes[5]*-1)+1)*50) - int(((data.axes[2]*-1)+1)*50)
    pub = rospy.Publisher('mode', Int16, queue_size=10)
    pub1= rospy.Publisher('var1', Int16, queue_size=10)
    pub2 = rospy.Publisher('var2', Int16, queue_size=10)
    pub.publish(speed)
    rospy.loginfo(speed)


def start():
    time.sleep(.2)
    rospy.init_node('joy2serial')
    rospy.Subscriber("joy", Joy, callback)

    rospy.spin()

if __name__ == '__main__':
    start()
