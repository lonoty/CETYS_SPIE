#!/usr/bin/env python
import rospy , struct
from graphics import *
from std_msgs.msg import Bool
from teleop.msg import robotstatus
from teleop.msg import bamboo
import time
global menu
global velocity
global mode
global voltage
global stats
global angle

velocity = 0
mode = 0
voltage = 0
stats = 0
angle = 0
program = 0
programm =0
global acciones
acciones = []
pub = rospy.Publisher('start', Bool, queue_size=10)
pub2 = rospy.Publisher('control', bamboo, queue_size=10)
def tuple(data):
    global acciones
    global program

    acciones.append((data.var1,data.var2))
    program = data.mode
    if data.mode == 1:
        acciones.append((0,0))
def callback(data):
    global velocity
    global mode
    global voltage
    global stats
    global angle
    global volt
    global state
    global velocity

    global time
    velocity =data.velocity
    mode = data.mode
    angle = data.angle
    stats = data.stats
    voltage = data.voltage





def start():

    msg = bamboo()
    velocity = 0
    i=0
    mode = 0
    voltage = 0
    stats = 0
    angle = 0
    rospy.init_node('Menu')
    rospy.Subscriber("status", robotstatus, callback)
    rospy.Subscriber("trayectoria", bamboo, tuple)

    menu = GraphWin("Menu",600,500, autoflush=True)
    menu.setBackground("black")

    logo = Image(Point(100,50),"/home/tommy/bamboo/src/teleop/src/Q.png")
    logo.draw(menu)
    Q = Text(Point(100,100), "Quantum")
    Q.setFill("white")
    Q.draw(menu)

    #Titulo
    bp = Text(Point(300,50),"Bamboo Project")
    bp.setFace("helvetica")
    bp.setStyle("bold")
    bp.setSize(24)
    bp.setFill("white")
    bp.draw(menu)

    atf = Text(Point(520,50), "Autonomous\n track follower")
    atf.setFace("helvetica")
    atf.setSize(10)
    atf.setFill("white")
    atf.draw(menu)

    #Botones
    stop = Rectangle(Point(150,400),Point(250,430))
    stop.setFill("white")
    stop.draw(menu)
    stopt = Text(Point(200,415),"STOP")
    stopt.setFill("black")
    stopt.setStyle("bold")
    stopt.draw(menu)

    c = Circle(Point(300,415),20)
    c.setFill("red")
    c.setOutline("red")
    c.draw(menu)

    run = Rectangle(Point(350,400),Point(450,430))
    run.setFill("white")
    run.draw(menu)
    runt = Text(Point(400,415), "RUN")
    runt.setFill("black")
    runt.setStyle("bold")
    runt.draw(menu)

    #Stop sign
    ss = Rectangle(Point(350,300),Point(450,330))
    ss.setOutline("red")
    ss.setFill("red")
    sst = Text(Point(400,315),"STOP")
    sst.setFill("white")
    sst.setStyle("bold")

    #Setting
    setting = Text(Point(400,145)," Setting")
    setting.setFill("white")
    setting.setStyle("bold")
    setting.setSize(16)
    setting.draw(menu)
    global volt
    global state
    global velocity
    global stats
    global time
    global program

    status = Text(Point(150,150)," Status" )
    status.setFill("white")
    status.setStyle("bold")
    status.setSize(16)
    status.draw(menu)

    volt = Text(Point(130,180),"Voltage: " + str(voltage))
    volt.setFill("white")
    volt.draw(menu)

    state = Text(Point(120,210),"State: " + str(mode))
    state.setFill("white")
    state.draw(menu)

    velocitys = Text(Point(130,240),"Velocity: " + str(velocity) )
    velocitys.setFill("white")
    velocitys.draw(menu)

    angless = Text(Point(120,270),"angle: " + str(angle))
    angless.setFill("white")
    angless.draw(menu)



    vel = Text(Point(380,180),"Velocity:")
    vel.setFill("white")
    # vel.setFace()
    vel.draw(menu)

    v = Entry(Point(440,180),4)
    v.setFill("white")
    v.draw(menu)

    L1 = Line(Point(330,145),Point(360,145))
    L1.setFill("white")
    L1.setWidth(3)
    L1.draw(menu)

    L2 = Line(Point(330,144),Point(330,210))
    L2.setFill("white")
    L2.setWidth(3)
    L2.draw(menu)

    L3 = Line(Point(450,145),Point(480,145))
    L3.setFill("white")
    L3.setWidth(3)
    L3.draw(menu)

    L4 = Line(Point(480,144),Point(480,210))
    L4.setFill("white")
    L4.setWidth(3)
    L4.draw(menu)

    L5 = Line(Point(329,210),Point(482,210))
    L5.setFill("white")
    L5.setWidth(3)
    L5.draw(menu)





    LS1 = Line(Point(80,150),Point(110,150))
    LS1.setFill("white")
    LS1.setWidth(3)
    LS1.draw(menu)

    LS2 = Line(Point(80,149),Point(80, 300))
    LS2.setFill("white")
    LS2.setWidth(3)
    LS2.draw(menu)

    LS3 = Line(Point(80,300),Point(240,300))
    LS3.setFill("white")
    LS3.setWidth(3)
    LS3.draw(menu)

    LS4 = Line(Point(240,301),Point(240,149))
    LS4.setFill("white")
    LS4.setWidth(3)
    LS4.draw(menu)

    LS5 = Line(Point(240,150),Point(200,150))
    LS5.setFill("white")
    LS5.setWidth(3)
    LS5.draw(menu)

    #Variables
    inspeed = v.getText()
    stopsign = 0


    #Boton STOP - click
    while not rospy.is_shutdown():
        global velocity
        global mode
        global voltage
        global state
        global angle
        global stats
        global menu
        global program
        global acciones
        global programm
        #status
        volt.setText("Voltage: " + str(stats))
        velocitys.setText("Velocity: " + str(velocity))
        state.setText(" Status: " + str(mode))
        angless.setText("Angle: " + str(angle))




        point = menu.checkMouse()
        if point != None:
            x = point.getX()
            y = point.getY()
            if x>=150 and x<=250 and y>=400 and y<=430:
                programm = 0
                print(acciones)
                pub.publish(False)
            if x>=350 and x<=450 and y>=400 and y<=430:
                programm = 1
                pub.publish(True)
                v.setText("")
        #boton RUN - click

        #boton ROJO
        if program == 1:
            c.setFill("green")
            c.setOutline("green")
        else:
            c.setFill("red")
            c.setOutline("red")
        if programm == 1:
            if stats == 0:
                if((len(acciones) -1 )>= i):
                    msg.mode = 2
                    msg.var1 = acciones[i][0]
                    msg.var2 = acciones[i][1]
                    print(acciones[i][0],acciones[i][1] )
                    
                    time.sleep(3)

                    pub2.publish(msg)
                    i = i +1


                else:
                    msg.mode = 0
                    msg.var1 = 0
                    msg.var2 = 0

                    program = 0
                    pub2.publish(msg)

        #Stop sign
        if stopsign ==1:
            ss.draw(menu)
            sst.draw(menu)
if __name__ == '__main__':
    start()
