#!/usr/bin/env python

import sys
import rospy, struct
from teleop.srv import *

def astar_client(mapa, xi, yi, xf, yf):
    rospy.wait_for_service('astar')
    try:
        astar = rospy.ServiceProxy('astar', astarmsg)
        resp1 = astar(mapa,xi,yi,xf, yf)
        print(resp1.pointsx)
        print(resp1.pointsy)
        print(resp1.acciones1)
        print(resp1.acciones2)

    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 6:
        mapa = float(sys.argv[1])
        xi = float(sys.argv[2])
        yi = float(sys.argv[3])
        xf = float(sys.argv[4])
        yf = float(sys.argv[5])
        print(mapa,xi,yi,xf,yf)

    else:
        print usage()
        sys.exit(1)
    astar_client(mapa,xi,yi,xf, yf)
