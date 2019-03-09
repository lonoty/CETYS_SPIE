#!/usr/bin/env python
import rospy , struct
from std_msgs.msg import Bool
from teleop.msg import robotstatus
from teleop.msg import bamboo
import time



pub2 = rospy.Publisher('control', bamboo, queue_size=10)
pub = rospy.Publisher('statuss', robotstatus, queue_size=10)
def tuple(data):
    pub2.publish(data)
def callback(data):


    pub.publish(data)





def start():

    msg = bamboo()

    rospy.init_node('repeat')
    rospy.Subscriber("status", robotstatus, callback)
    rospy.Subscriber("controll", bamboo, tuple)

if __name__ == '__main__':
    start()
