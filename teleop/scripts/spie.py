#!/usr/bin/env python
import rospy , struct
import serial, time
import numpy as np
import time
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int16
from std_msgs.msg import Bool
from teleop.msg import bamboo
from graphics import *
global anglesin
global v
global anglecos
maxx= 10
maxy= 10
midx = maxx/2
midy = maxy/2
tolerance = 0 #number of points there must be to count the square (0 is only one)
res = .2
tests = []
rast = []
iter =int(maxx/res)
quadra = iter/2

global sqr
sqr = [[0 for x in range(iter*2)] for y in range(iter*2)]

for i in xrange(360):
    rast.insert(i,Rectangle(Point(0,0), Point(0,0)))
for i in xrange(360):
    tests.insert(i,Point(0,0))

v = GraphWin("Spie", 1000, 1000, autoflush=False)
v.setCoords(0, 0, maxx, maxy)

angle = np.arange(360)
angle = np.deg2rad(angle)
anglesin = np.sin(angle)
anglecos = np.cos(angle)


#origin
test = Point(2,3)
test.draw(v)


global start
global lasterr
global xpoint
global ypoint
xpoint = np.zeros(360) * anglesin
ypoint = np.zeros(360) * anglecos
def clear(win):
    for item in win.items[:]:
        item.undraw()
    crosshair(win)
    boundry(win)
    grid(win)
    win.update()

def boundry(v):
    global min
    refresh = Circle(Point(maxx-.5,maxy -.5), .5)
    safety = Circle(Point(maxx-.5,maxy-.5), .25)
    if min < .25:
        refresh.setFill("red")
        if min < .16:
            safety.setFill("purple")
    else:
        refresh.setFill("white")
        safety.setFill("white")
    refresh.draw(v)
    safety.draw(v)
    v.update()

def crosshair (v):
    LH = Line(Point(midy,0 ), Point(midy,maxx ))
    LH.setWidth(3)
    LH.draw(v)
    LV = Line(Point(0, midx), Point(maxy, midx))
    LV.setWidth(3)
    LV.draw(v)
def grid (v):


    for x in range(0 , iter):
        linesv = Line(Point(x*res, 0), Point(x*res, maxy))
        linesv.draw(v)
    for y in range(0 , iter):
        linesv = Line(Point(0, y*res), Point(maxx, y*res))
        linesv.draw(v)
    v.update()
def callback(data):
    global anglesin
    global anglecos
    global xpoint
    global ypoint
    global min

    xpoint = data.ranges * anglesin
    ypoint = data.ranges * anglecos
    min = np.min(data.ranges)



def start():
    global v
    time.sleep(.2)
    rospy.init_node('lidarss')
    rospy.Subscriber("scan", LaserScan, callback)
    grid(v)
    crosshair(v)
    rxpoint=0
    rypoint=0
    while not rospy.is_shutdown():
        global v
        global xpoint
        global ypoint
        global min
        global sqr
        boundry(v)
        holder = 0
        for x in xrange(360):

            if np.isinf(xpoint[x]) == 0 and np.isinf(ypoint[x]) == 0:

                tests[x] = Point(xpoint[x]+midx,ypoint[x]+midy)
                tests[x].draw(v)
                if(xpoint[x] > 0 and ypoint[x] >0): #first quadrant
                    rxpoint= (int(xpoint[x]*(1/res)) + quadra)
                    rypoint= (int(ypoint[x]*(1/res)) + quadra)
                elif(xpoint[x] < 0 and ypoint[x] >0): #second quadrant
                    rxpoint= (int(xpoint[x]*(1/res)) + quadra) -1
                    rypoint= (int(ypoint[x]*(1/res)) + quadra)
                elif(xpoint[x] < 0 and ypoint[x] < 0): #third quadrant
                    rxpoint= (int(xpoint[x]*(1/res)) + quadra) -1
                    rypoint= (int(ypoint[x]*(1/res)) + quadra) -1
                elif(xpoint[x] > 0 and ypoint[x] < 0): #forth quadrant
                    rxpoint= (int(xpoint[x]*(1/res)) + quadra)
                    rypoint= (int(ypoint[x]*(1/res)) + quadra)-1

                sqr[rxpoint][rypoint]= sqr[rxpoint][rypoint] + 1
                if sqr[rxpoint][rypoint] >= tolerance:
                     rast[holder] = Rectangle(Point((rxpoint * res) ,(rypoint * res)), Point(((rxpoint * res)+res),((rypoint * res)+res)))
                     rast[holder].setFill("red")
                     rast[holder].draw(v)
                     holder= holder + 1
        v.update()



        time.sleep(.1)
        for ii in xrange(360):
            rast[ii].undraw()
        for i in xrange(360):
            tests[i].undraw()


        #clear(v)

if __name__ == '__main__':
    start()
