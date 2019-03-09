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
distance1 = .3
start = 0
orden = False
def callbacks(data):
    global start
    start = data.data
    print(start == True)


def callback(data):
    global start
    global distance
    global orden
    msg = bamboo()
    pub = rospy.Publisher('control', bamboo, queue_size=10)


    if (True == True):


        kp = 20
        kd = 29
        error =  data.ranges[180] - distance1
        speed = (error * kp) + kd * (error - lasterr)
        speed = speed
        speed = int(speed)
        if (speed < 5):
            speed=0
        if (speed  >= 100):
            speed = 100
        print(speed)
        """
        if data.ranges[270] <= distance :
            msg.var1 = 0
            msg.var2 = speed
            orden = True

        elif data.ranges[270] < distance and data.ranges[180] < .5:
            msg.var1 = speed
            msg.var2 = speed + 100

        elif data.ranges[270] < distance and data.ranges[0] < .5:
            msg.var1 = speed + 100
            msg.var2 = speed

        elif data.ranges[270] < distance and data.ranges[0] < distance and data.ranges[180] < .25:
            msg.var1 = speed + 100
            msg.var2 = speed

        else:

            msg.var1 = speed
            msg.var2 = speed
            """
        msg.mode = 0
        msg.var1 = speed
        msg.var2 = speed



        pub.publish(msg)
        #print(data.ranges[270])



def start():
    time.sleep(.2)
    rospy.init_node('lidarss')
    rospy.Subscriber("scan", LaserScan, callback)
    rospy.Subscriber("start", Bool, callbacks)
    rospy.spin()

if __name__ == '__main__':
    start()
