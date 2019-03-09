#!/usr/bin/env python
import rospy , struct
import serial, time
from sensor_msgs.msg import Joy
from std_msgs.msg import Int16
from teleop.msg import bamboo
global status
status = False
buttonstate =0;
acciones= []

def callback(data):
    global buttonstate
    global xboxdata
    global status
    xboxdata = data


    pub = rospy.Publisher('control', bamboo, queue_size=10)
    msg = bamboo()



    if (data.buttons[0] == 1):
        buttonstate = 0;
        print("1")
    elif (data.buttons[1] == 1):
        buttonstate = 1;
        print("2")
    elif (data.buttons[2] == 1):
        buttonstate =2;
        print("3")
    elif (data.buttons[3] == 1):
        buttonstate =3
        print("4")


    if (buttonstate == 0):
        msg.mode = 0
        msg.var1 = int(((data.axes[5]*-1)+1)*50)
        msg.var2 = int(((data.axes[2]*-1)+1)*50)
        pub.publish(msg)

    elif(buttonstate == 1):
        msg.mode = 1
        msg.var1 = int(((data.axes[5]*-1)+1)*50) - int(((data.axes[2]*-1)+1)*50)
        msg.var2 = 0
        pub.publish(msg)
    elif(buttonstate == 2):

        if(data.axes[7] == 1):
            msg.mode = 2
            msg.var1 = 0
            msg.var2 = 90
            pub.publish(msg)

        elif(data.axes[6] == 1):
            msg.mode = 2
            msg.var1 = 45
            msg.var2 = 0
            pub.publish(msg)

        elif(data.axes[6] == -1):
            msg.mode = 2
            msg.var1 = 270
            msg.var2 = 0
            pub.publish(msg)
        else:
            msg.mode = 2
            msg.var1 = 0
            msg.var2 = 0
            pub.publish(msg)

def start():
    global buttonstate
    global xboxdata
    global status

    rospy.init_node('joy2serial')
    rospy.Subscriber("joy", Joy, callback)
    rospy.Subscriber("trayectoria", bamboo, tuple)
    rospy.spin()







if __name__ == '__main__':
    start()
