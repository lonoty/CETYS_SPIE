#!/usr/bin/env python
import rospy , struct
import serial, time
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int16
from std_msgs.msg import Bool
from teleop.msg import bamboo
global start

global lasterr
lasterr = 0
distance = .3

start = 0
def callbacks(data):
    global start
    start = data.data
    print(start == True)
def callback(data):
    global start
    global dinstance

    pub = rospy.Publisher('control', bamboo, queue_size=10)

    msg = bamboo()
    if (start == True):


        kp = 400
        kd = 29
        error =  data.ranges[270] - distance
        speed = (error * kp) + kd * (error - lasterr)
        speed = int(speed)
        if speed > 100:
            speed = 100
        if speed < 0:
            speed = 0
        print(speed)


        pub = rospy.Publisher('control', bamboo, queue_size=10)
        msg = bamboo()
        msg.mode = 0
        msg.var1 = speed #0-100
        msg.var2 = speed
        #rospy.loginfo(data.ranges[0])
        #print(data.ranges[0], speed)
        pub.publish(msg)
        print(data.ranges[270])

        """
        if data.ranges[270] >= distance:
            speed = 100
        else:
            speed = 0


        msg.mode = 0
        msg.var1 = speed
        msg.var2 = speed
        #rospy.loginfo(data.ranges[0])
        #print(data.ranges[0], speed)

        #print(data.ranges[270])
        """
    else:

        msg.mode = 1
        msg.var1 = 0
        msg.var2 = 0
    pub.publish(msg)

def start():
    time.sleep(.2)
    rospy.init_node('lidarss')
    rospy.Subscriber("scan", LaserScan, callback)
    rospy.Subscriber("start", Bool, callbacks)
    rospy.spin()

if __name__ == '__main__':
    start()
