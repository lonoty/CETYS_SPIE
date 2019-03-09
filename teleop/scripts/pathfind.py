#!/usr/bin/env python
import rospy
from collections import deque
from pygame import *
from teleop.msg import bamboo
import sys
import time
import csv
import math
import operator
pub = rospy.Publisher('trayectoria', bamboo, queue_size=10)

# Variables
running = True
xdim, ydim = 20, 20
bWidth, bHeight = 20, 20
bxpos, bypos = 0, 0
axpos, aypos = 0, 0
margin = 10
xmax, ymax = xdim * bWidth + (xdim + 1) * margin, ydim * bHeight + (ydim + 1) * margin

# dictionary

DijkstraDict = {

}


class State(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "<State a:%s b:%s>" % (self.x, self.x)

    def __str__(self):
        return "State: X is %s, Y is %s" % (self.x, self.y)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Action(object):

    def __init__(self, xa, ya):
        self.xa = xa
        self.ya = ya


def make_action(xa, ya):
    action = Action(xa, ya)
    return action


def make_state(xs, ys):
    state = State(xs, ys)
    return state


# Display setup
bgColor = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
orange = (253, 106, 2)
green = (0, 255, 0)
purple = (148, 0, 211)
rospy.init_node('trayect')
screen = display.set_mode((xmax, ymax))
display.set_caption('A*')
screen.fill(bgColor)
display.flip()

# Grid Creation
for x in range(0, 10):
    draw.rect(screen, white, [bxpos + margin, bypos + margin, 2 * bWidth + margin, 2 * bHeight + margin])
    for y in range(0, 10):
        draw.rect(screen, white, [bxpos + margin, bypos + margin, 2 * bWidth + margin, 2 * bHeight + margin])
        bypos += 2 * bHeight + 2 * margin
    bypos = 0
    bxpos += 2 * bWidth + 2 * margin

obs = deque([])
with open('/home/tommy/bamboo/src/teleop/src/map01.csv') as file:
    reader = csv.reader(file)

    for row in reader:
        ox, oy, w, h = float(row[0]), float(row[1]), 2*float(row[2]), 2*float(row[3])
        ox=2*ox
        oy=2*oy + 2*float(row[3])
        draw.rect(screen, purple,
                  [(ox * (margin + bWidth)) + margin,(ymax - margin) - (oy * (margin + bHeight)) + margin,
                   (w * bWidth) + ((w - 1) * margin), (h * bHeight) + ((h - 1) * margin)])
        # print(row[0],row[1],row[2],row[3],)

        while (w >= 0):
            xn = make_state(ox, oy)
            print(ox, oy)
            htemp = h
            obs.append(xn)
            oytemp = oy
            while (htemp > 0):
                oytemp = oytemp - 1
                xn = make_state(ox, oytemp)
                print(ox, oy)
                obs.append(xn)
                htemp = htemp - 1
            ox = ox + 1
            w = w - 1

# Variable declarations
c = 0

n=2
while(True):
    xini = float(input('Enter the initial x coordinate: '))
    yini = float(input('Enter the initial y coordinate: '))
    xfin = float(input('Enter the final x coordinate: '))
    yfin = float(input('Enter the final y coordinate: '))

    inicio=make_state(2*xini,2*yini)
    final=make_state(2*xfin,2*yfin)

    if(xini<0 or (xini%0.5)!=0 or xini>10):
        print("Su coordenada inicial de x es menor a 0, mayor a 10 o no corresponde a la resolucion")
    elif (yini < 0 or (yini % 0.5) != 0 or yini > 10):
        print("Su coordenada inicial de y es menor a 0, mayor a 10 o no corresponde a la resolucion")
    elif (xfin < 0 or (xfin % 0.5) != 0 or xfin > 10):
        print("Su coordenada final de x es menor a 0, mayor a 10 o no corresponde a la resolucion")
    elif (yfin < 0 or (yfin % 0.5) != 0 or yfin > 10):
        print("Su coordenada final de y es menor a 0, mayor a 10 o no corresponde a la resolucion")

    elif (inicio in obs ):
        print("Su coordenada inicial se encuentra en un obstaculo preestablecido por favor escoja otra")
    elif (final in obs):
        print("Su coordenada final se encuentra en un obstaculo preestablecido por favor escoja otra")

    else:
        break




x1 = make_state(n*xini,n*yini)
xG = make_state(n*xfin,n*yfin)
U = []
up = make_action(0, 1)
upr = make_action(1, 1)
upl = make_action(-1, 1)
right = make_action(1, 0)
down = make_action(0, -1)
downr = make_action(1, -1)
downl = make_action(-1, -1)
left = make_action(-1, 0)

check = [x1.x, x1.y, xG.x, xG.y]
for x in range(0, 4):
    if check[x] > xdim:
        print("No se permiten valores mayores a %d unidades en las coordenadas" % xdim)
        sys.exit(0)
Q = deque([])
Q.append(x1)
visited = []
visited.append(x1)

xGRx, xGRy = xG.x * (margin + bWidth), (ymax - margin) - xG.y * (margin + bHeight)
x1Rx, x1Ry = x1.x * (margin + bWidth), (ymax - margin) - x1.y * (margin + bHeight)
draw.rect(screen, green, [xGRx, xGRy, margin, margin])
draw.rect(screen, red, [x1Rx, x1Ry, margin, margin])

# implementacion del diccionario
DijkstraDict[(x1.x, x1.y)] = 0
dictnuevo = {}
losbuenos = []
losbuenos.append((x1.x, x1.y))
tiempo=0.001
array=[]

while len(Q) > 0:

    xt = Q.popleft()

    if xt.x == 20 and xt.y == 20:
        break

    for x in range(0, 8):
        if x == 0:
            if 0 <= xt.x + up.xa <= xdim and 0 <= xt.y + up.ya <= ydim:
                xn = make_state(xt.x + up.xa, xt.y + up.ya)



            if xn not in visited and xn not in obs:
                DijkstraDict[(xn.x, xn.y)] = 0.5 + DijkstraDict[(xt.x, xt.y)]
                array.append((xn.x, xn.y))

                c = c + 1
                Q.append(xn)
                visited.append(xn)
                xRx, xRy = xn.x * (margin + bWidth), (ymax - margin) - xn.y * (margin + bHeight)
                draw.rect(screen, orange, [xRx, xRy, margin, margin])
                display.update()
                time.sleep(tiempo)



        elif x == 1:
            if 0 <= xt.x + upr.xa <= xdim and 0 <= xt.y + upr.ya <= ydim:
                xn = make_state(xt.x + upr.xa, xt.y + upr.ya)
            if xn not in visited and xn not in obs:
                DijkstraDict[(xn.x, xn.y)] = math.sqrt(0.5) + DijkstraDict[(xt.x, xt.y)]
                array.append((xn.x, xn.y))

                c = c + 1
                Q.append(xn)
                visited.append(xn)
                xRx, xRy = xn.x * (margin + bWidth), (ymax - margin) - xn.y * (margin + bHeight)
                draw.rect(screen, orange, [xRx, xRy, margin, margin])
                display.update()
                time.sleep(tiempo)
        elif x == 2:
            if 0 <= xt.x + right.xa <= xdim and 0 <= xt.y + right.ya <= ydim:
                xn = make_state(xt.x + right.xa, xt.y + right.ya)


            if xn not in visited and xn not in obs:
                DijkstraDict[(xn.x, xn.y)] = 0.5+ DijkstraDict[(xt.x, xt.y)]
                array.append((xn.x, xn.y))

                c = c + 1
                Q.append(xn)
                visited.append(xn)
                xRx, xRy = xn.x * (margin + bWidth), (ymax - margin) - xn.y * (margin + bHeight)
                draw.rect(screen, orange, [xRx, xRy, margin, margin])
                display.update()
                time.sleep(tiempo)
        elif x == 3:
            if 0 <= xt.x + downr.xa <= xdim and 0 <= xt.y + downr.ya <= ydim:
                xn = make_state(xt.x + downr.xa, xt.y + downr.ya)



            if xn not in visited and xn not in obs:
                DijkstraDict[(xn.x, xn.y)] = math.sqrt(0.5) + DijkstraDict[(xt.x, xt.y)]
                array.append((xn.x, xn.y))

                c = c + 1
                Q.append(xn)
                visited.append(xn)
                xRx, xRy = xn.x * (margin + bWidth), (ymax - margin) - xn.y * (margin + bHeight)
                draw.rect(screen, orange, [xRx, xRy, margin, margin])
                display.update()
                time.sleep(tiempo)

        elif x == 4:
            if 0 <= xt.x + down.xa <= xdim and 0 <= xt.y + down.ya <= ydim:
                xn = make_state(xt.x + down.xa, xt.y + down.ya)


            if xn not in visited and xn not in obs:
                DijkstraDict[(xn.x, xn.y)] = 0.5 + DijkstraDict[(xt.x, xt.y)]
                array.append((xn.x, xn.y))


                c = c + 1
                Q.append(xn)
                visited.append(xn)
                xRx, xRy = xn.x * (margin + bWidth), (ymax - margin) - xn.y * (margin + bHeight)
                draw.rect(screen, orange, [xRx, xRy, margin, margin])
                display.update()
                time.sleep(tiempo)
        elif x == 5:
            if 0 <= xt.x + downl.xa <= xdim and 0 <= xt.y + downl.ya <= ydim:
                xn = make_state(xt.x + downl.xa, xt.y + downl.ya)

            if xn not in visited and xn not in obs:
                DijkstraDict[(xn.x, xn.y)] = math.sqrt(0.5)+ DijkstraDict[(xt.x, xt.y)]
                array.append((xn.x, xn.y))
                c = c + 1
                Q.append(xn)
                visited.append(xn)
                xRx, xRy = xn.x * (margin + bWidth), (ymax - margin) - xn.y * (margin + bHeight)
                draw.rect(screen, orange, [xRx, xRy, margin, margin])
                display.update()
                time.sleep(tiempo)

        elif x == 6:
            if 0 <= xt.x + left.xa <= xdim and 0 <= xt.y + left.ya <= ydim:
                xn = make_state(xt.x + left.xa, xt.y + left.ya)


            if xn not in visited and xn not in obs:
                DijkstraDict[(xn.x, xn.y)] = 0.5+ DijkstraDict[(xt.x, xt.y)]
                array.append((xn.x, xn.y))
                c = c + 1
                Q.append(xn)
                visited.append(xn)
                xRx, xRy = xn.x * (margin + bWidth), (ymax - margin) - xn.y * (margin + bHeight)
                draw.rect(screen, orange, [xRx, xRy, margin, margin])
                display.update()
                time.sleep(tiempo)
        elif x == 7:
            if 0 <= xt.x + upl.xa <= xdim and 0 <= xt.y + upl.ya <= ydim:
                xn = make_state(xt.x + upl.xa, xt.y + upl.ya)

            if xn not in visited and xn not in obs:
                DijkstraDict[(xn.x, xn.y)] = math.sqrt(0.5)+ DijkstraDict[(xt.x, xt.y)]
                array.append((xn.x, xn.y))
                c = c + 1
                Q.append(xn)
                visited.append(xn)
                xRx, xRy = xn.x * (margin + bWidth), (ymax - margin) - xn.y * (margin + bHeight)
                draw.rect(screen, orange, [xRx, xRy, margin, margin])
                display.update()
                time.sleep(tiempo)
                #f = min(dictnuevo.items(), key=operator.itemgetter(1))[0]
                #(a, b) = f
                #xcool = make_state(a, b)
                #losbuenos.append((a, b))



                dictnuevo.clear()

        if xn.x == 20 and xn.y == 20:
            c = c + 1
            break
        if xn.x == x1.x and xn.y == x1.y:
            temp = True

        # implementacion de dijkstra
        # hacer un for para los elementos y precios del dijkstra luego borrarlos para que el diccionario se pueda llenar, de esta manera se pueden comparar, ir llenando una lista y obtener max()


    else:
        continue

    break

hurra=len(array)
for x in range(0,len(array)-1):
    DijkstraDict[array[x]] = DijkstraDict[array[x]]+math.sqrt((xG.x - array[x][0]) ** 2 + (xG.y - array[x][1]) ** 2)

#esta parte se encarga de crear la lista de pasos a seguir segun el algoritmo de dijkstra
otrodict={}


#salir=False
while (True):

    movements = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    for x in range(0, 7):
        h = movements[x][0] + losbuenos[-1][0]
        k = movements[x][1] + losbuenos[-1][1]

        movements[x] = (h, k)


        if (movements[x] in DijkstraDict):
            if (movements[x] != (x1.x, x1.y) and abs(h - xG.x) <= abs(losbuenos[-1][0] - xG.x) and abs(k - xG.y) <= abs(losbuenos[-1][1] - xG.y) and movements[x] not in losbuenos):
                otrodict[movements[x]] = DijkstraDict[movements[x]]
            elif movements[x] != (x1.x, x1.y) and abs(k-xG.y)<=abs(losbuenos[-1][1]-xG.y) and movements[x] not in losbuenos and not (losbuenos[-1][0]>h) :
                otrodict[movements[x]] = DijkstraDict[movements[x]]
            elif movements[x] != (x1.x, x1.y) and abs(h-xG.x)<=abs(losbuenos[-1][0]-xG.x) and movements[x] not in losbuenos and not (losbuenos[-1][1]>k):
                otrodict[movements[x]] = DijkstraDict[movements[x]]

    if (math.sqrt((xG.x-losbuenos[-1][0])**2+(xG.y-losbuenos[-1][1])**2)<=math.sqrt(2)):
        losbuenos.append((xG.x, xG.y))
        break

    t = min(otrodict.items(), key=operator.itemgetter(1))[0]
    losbuenos.append(t)

    otrodict.clear()






#hora de dibujar
costototal=0
for x in range(0,len(losbuenos)-1):
    px1, py1 = losbuenos[x][0] * (margin + bWidth), (ymax - margin) - losbuenos[x][1] * (margin + bHeight)
    px2, py2 = losbuenos[x+1][0] * (margin + bWidth), (ymax - margin) - losbuenos[x+1][1] * (margin + bHeight)

    if(math.sqrt((losbuenos[x+1][0]-losbuenos[x][0])**2+(losbuenos[x+1][1]-losbuenos[x][1])**2)==math.sqrt(2)):
        costototal=costototal+math.sqrt(0.5)
    else:
        costototal=costototal+0.5


    draw.line(screen, purple, [px1, py1],[px2, py2],10)
    display.update()






print("la lista de estados a seguir es",losbuenos)
#print(DijkstraDict)

print("El costo de la ruta desde el punto de inicio hasta la meta es de",costototal )
print("Se visitaron %d estados para encontrar el punto meta en el ambiente de trabajo" % (len(visited)))

#Para implementacion en el robot

angulos={
    (0,0):90,
    (0,1):   90,
    (1,1):   45,
    (1,0):   0,
    (1,-1):  -45,
    (0,-1):  -90,
    (-1,-1):  -135,
    (-1,0):   180,
    (-1,1):   135

}


acciones=[]
mov=[]
for x in range(0,len(losbuenos)-1):
    mov.append((losbuenos[x+1][0]-losbuenos[x][0],losbuenos[x+1][1]-losbuenos[x][1]))

mov.insert(0,(0,0))

for x in range(0, len(mov) - 1):
    if (abs(mov[x+1][0])+abs(mov[x+1][1]))==2:
        if (angulos[mov[x+1]]-angulos[mov[x]]) < 0:
            anggg= angulos[mov[x+1]]-angulos[mov[x]] + 360
        else:
            anggg= angulos[mov[x+1]]-angulos[mov[x]]
        acciones.append((anggg,212))
    else:
        if (angulos[mov[x+1]]-angulos[mov[x]]) < 0:
            anggg= angulos[mov[x+1]]-angulos[mov[x]] + 360
        else:
            anggg= angulos[mov[x+1]]-angulos[mov[x]]

        acciones.append((anggg,150))

msg = bamboo()


accionesfluidas=[]
x=0
print (acciones)
while(x<len(acciones) - 1):
    rota=acciones[x][0]
    trasla=acciones[x][1]
    for w in range(x+1, len(acciones) ):

        if  acciones[x][1]==acciones[w][1] and acciones[w][0]==0:

            trasla=trasla+acciones[w][1]
            x=w

        else:
            break
    accionesfluidas.append((rota,trasla))
    x=x+1

for x in range(0,len(accionesfluidas) ):
    if x == (len(accionesfluidas) -1 ):
        sent = 1
    else:
        sent =0

    ang=accionesfluidas[x][0]
    unit=accionesfluidas[x][1]
    msg.mode = sent
    msg.var1 = ang
    msg.var2 = unit
    pub.publish(msg)
    print(len(accionesfluidas))
    print(x)




print(mov)


print(accionesfluidas)

# Movement
rospy.spin()
