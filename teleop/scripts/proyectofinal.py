#!/usr/bin/env python

import rospy , struct
import pygame as pg
from collections import deque
import os
import csv
import time
import operator
import math

pg.init()


# grid 10x10
def grid(surface, ws, squaresbyside):
    ss = int(ws / squaresbyside) + 1
    surface.fill(white)
    for x in range(1, squaresbyside):
        pg.draw.line(surface, black, (0, x * ss), (ws, x * ss))
        pg.draw.line(surface, black, (x * ss, 0), (x * ss, ws))
    pg.display.flip()


# convertir a coordenadas
def xconverter(tamano, cuadros, x):
    paso = int(tamano / cuadros) + 1
    x = paso * x
    return int(x)


def yconverter(tamano, cuadros, y):
    paso = int(tamano / cuadros) + 1
    y = tamano - paso * y
    return int(y)


# radio de los circulos
radio = 10
# colors
camino = (200, 150, 35)
violeta = [206, 53, 124]
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
# tiempo de pausa
tiempo = 0.005
# window setup
cuadriculade = 10
winsize = 700
winsize = winsize + cuadriculade - 1
window = pg.display.set_mode((winsize, winsize))
pg.display.set_caption('Autonomous robot in a partially known environment')
# clock=pg.time.Clock()
grid(window, winsize, cuadriculade)
print(pg.display.get_surface())

print('Please select which map would you like to use')
print('0.map00')
print('1.map01')
print('2.map02')
print('3.map03')

while (True):
    mapa = input('Enter the number of the map you want to use: ')
    if mapa == '1':
        mapa = 'map01.csv'
        break
    elif mapa == '2':
        mapa = 'map02.csv'
        break
    elif mapa == '3':
        mapa = 'map03.csv'
        break
    elif mapa == '0':
        mapa = 'map00.csv'
        break
    else:
        print('Please introduce one of the available options shown above')

print('The following are the resolution options available for this application')
print('option 1. 1x')
print('option 2. 2x')
print('option 4. 4x')
reso = input('Please select the resoluton that best fits your needs: ')
while (True):
    if reso == '1':
        resolution = 1
        w, h = 11, 11;
        Matrix = [[0 for x in range(w)] for y in range(h)]
        break
    elif reso == '2':
        resolution = 2
        w, h = 21, 21;
        Matrix = [[0 for x in range(w)] for y in range(h)]
        break
    elif reso == '4':
        resolution = 4
        w, h = 41, 41;
        Matrix = [[0 for x in range(w)] for y in range(h)]
        break
    else:
        print("please introduce a correct value")
# lista de coordenadas donde se encuentran obstáculos
obs = []
# generación visual de obstáculos
with open(mapa, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        ox, oy, w, h = float(row[0]), float(row[1]), float(row[2]), float(row[3])
        xo = xconverter(winsize, cuadriculade, ox)
        yo = 700 + cuadriculade - 1 - xconverter(winsize, cuadriculade, oy)
        pg.draw.rect(window, red, [xo, yo, xconverter(winsize, cuadriculade, w), -xconverter(winsize, cuadriculade, h)])
        pg.display.update()
        for xi in range(0, int(h * resolution + 1)):
            for xa in range(0, int(w * resolution + 1)):
                obs.append((ox * resolution + xa, oy * resolution + xi))

if (obs[0] == (0.0, 0.0) and len(obs) == 1):
    obs.clear()
pg.display.update()

# asking for information

while (True):
    a = float(input('Please type the initial coordiante in x: '))
    b = float(input('Please type the initial coordiante in y: '))
    if (a * resolution, b * resolution) in obs:
        print("There is an obstacle in that initial location for the bot")
        continue
    ################Verificar con posterioridad
    # elif (a % int(a) != 1 / resolution or b % int(b) != 1 / resolution) and (a % int(a) != 0 or b % int(b) != 0):
    # print("Please enter a coordinate that obeys the resolution chosen, in this case a multiple of", 1 / resolution)
    # continue
    c = float(input('Please type the goal coordiante in x: '))
    d = float(input('Please type the goal coordiante in y: '))
    if (c * resolution, d * resolution) in obs:
        print("There is an obstacle in that final location for the bot to achieve")
        continue
    # elif (c % int(c) != 1 / resolution or d % int(d) != 1 / resolution) and (c % int(c) != 0 or d % int(d) != 0):
    # print("Please enter a coordinate that obeys the resolution chosen, in this case a multiple of", 1 / resolution)
    # continue
    inipo = (a, b)
    finalpo = (c, d)
    if a < 0 or b < 0 or a > 10 or b > 10 or c < 0 or d < 0 or c > 10 or d > 10:
        print(
            "Please introduce a valid value since the grid is 10x10, being the minimal coordinaate (0,0) and the maximum one (10,10)")
    elif finalpo == inipo:
        print('Please introduce a goal coordinate different from the initial coordinate')
    else:
        xi = a
        yi = b
        xf = c
        yf = d
        break
pg.draw.circle(window, green, (xconverter(winsize, cuadriculade, xi), yconverter(winsize, cuadriculade, yi)), radio, 0)
pg.draw.circle(window, blue, (xconverter(winsize, cuadriculade, xf), yconverter(winsize, cuadriculade, yf)), radio, 0)
pg.display.flip()

# Forward search
Q = deque([])
Q.append((xi * resolution, yi * resolution))
visited = []
visited.append((xi * resolution, yi * resolution))
acciones = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
found = False
while (len(Q) > 0):
    ct = Q.popleft()
    if found == True:  # ct[0] == xf*resolution and ct[1]*resolution == yf:
        break
    for accion in acciones:
        nueva = (ct[0] + accion[0], ct[1] + accion[1])
        if (((nueva[0] <= 10 * resolution) and (nueva[0] >= 0 * resolution) and (nueva[1] <= 10 * resolution)) and ((
                nueva[1] >= 0 * resolution))) and nueva not in visited and nueva not in obs:
            visited.append(nueva)
            Q.append(nueva)
            pg.draw.circle(window, violeta, (xconverter(winsize, cuadriculade, nueva[0] / resolution),
                                             yconverter(winsize, cuadriculade, nueva[1] / resolution)),
                           radio - resolution * 2, 0)
            pg.display.flip()
            time.sleep(tiempo)
            if nueva[0] == xf * resolution and nueva[1] == yf * resolution:
                found = True
                break
#esta seccion permite tratar con situaciones en donde xi=xf y yi=yf
izqui=[]
dere=[]
arriba=[]
abajo=[]
if xi==xf:
    for x in visited:
        if x[0]<xi*resolution:
            izqui.append(x)
        else:
            dere.append(x)
    if len(dere)>len(izqui):
        visited=dere
    else:
        visited=izqui
if yi==yf:
    for y in visited:
        if y[1]<yi*resolution:
            abajo.append(y)
        else:
            arriba.append(y)
    if len(arriba)>len(abajo):
        visited=arriba
    else:
        visited=abajo
######################################################################################3




# A* implementation
dicti = {}
path = []
path.append((xi * resolution, yi * resolution))
visited.append((xf * resolution, yf * resolution))  # * resolution

for x in visited:
    x = path[-1]
    for y in acciones:
        new = (x[0] + y[0], x[1] + y[1])
        old_price = ((xf * resolution - path[-1][0]) ** 2 + (yf * resolution - path[-1][1]) ** 2) ** (1 / 2)
        pasado = ((xi * resolution - new[0]) ** 2 + (yi * resolution - new[1]) ** 2) ** (1 / 2)

        new_price = ((xf * resolution - new[0]) ** 2 + (yf * resolution - new[1]) ** 2) ** (1 / 2)


        if xi==xf:
            if(new[1]!=yf*resolution):#si no se esta a la misma altura
                if new in visited and new not in path and new[1]!=yi*resolution and abs(yf*resolution-new[1])<=abs(yf*resolution-path[-1][1]): #and new[1]>=path[-1][1]:
                    dicti[new] = new_price

                else:
                    dicti[new] = 10000000000000
            else:#si no se esta a la misma distancia horizontal
                if new in visited and new not in path and new[1]!=yi*resolution and abs(xf*resolution-new[0])<=abs(xf*resolution-path[-1][0]): #and new[1]>=path[-1][1]:
                    dicti[new] = new_price

                else:
                    dicti[new] = 10000000000000





        elif yi==yf:
            if(new[0]!=xf*resolution):#si no se esta a la misma distancia horizontal
                if new in visited and new not in path and new[0]!=xi*resolution and abs(xf*resolution-new[0])<=abs(xf*resolution-path[-1][0]):
                    dicti[new] = new_price
                else:
                    dicti[new] = 10000000000000
            else:#si no se esta a la misma altura
                if new in visited and new not in path and new[0]!=xi*resolution and abs(yf*resolution-new[1])<=abs(yf*resolution-path[-1][1]):
                    dicti[new] = new_price
                else:
                    dicti[new] = 10000000000000



        else:
            if new in visited and new not in path:
                dicti[new] = new_price

            else:
                dicti[new] = 10000000000000




    t = min(dicti.items(), key=operator.itemgetter(1))[0]
    # se anade a la lista de los buenos
    path.append((t[0], t[1]))
    if t == (xf * resolution, yf * resolution):
        break
    # se limpia el diccionario
    dicti.clear()

# hora de dibujar
for x in range(0, len(path) - 1):
    pg.draw.line(window, camino, [xconverter(winsize, cuadriculade, path[x][0] / resolution),
                                  yconverter(winsize, cuadriculade, path[x][1] / resolution)],
                 [xconverter(winsize, cuadriculade, path[x + 1][0] / resolution),
                  yconverter(winsize, cuadriculade, path[x + 1][1] / resolution)], 10)
    pg.display.update()

# Para implementación en el robot

angulos = {
    (0, 0): 90,
    (0, 1): 90,
    (1, 1): 45,
    (1, 0): 0,
    (1, -1): -45,
    (0, -1): -90,
    (-1, -1): -135,
    (-1, 0): 180,
    (-1, 1): 135

}

acciones = []
mov = []
for x in range(0, len(path) - 1):
    mov.append((path[x + 1][0] - path[x][0], path[x + 1][1] - path[x][1]))

mov.insert(0, (0, 0))

for x in range(0, len(mov) - 1):
    if (abs(mov[x + 1][0]) + abs(mov[x + 1][1])) == 2:
        acciones.append((angulos[mov[x + 1]] - angulos[mov[x]], (((1 / resolution) ** 2) * 2) ** (1 / 2)))
    else:
        acciones.append((angulos[mov[x + 1]] - angulos[mov[x]], 1 / resolution))

###################Movimientos fluidos##############################
accionesfluidas = []
x = 0

while (x < len(acciones) - 1):
    rota = acciones[x][0]
    trasla = acciones[x][1]
    for w in range(x + 1, len(acciones)):

        if acciones[x][1] == acciones[w][1] and acciones[w][0] == 0:

            trasla = trasla + acciones[w][1]
            x = w

        else:
            break
    accionesfluidas.append((rota, trasla))
    x = x + 1

##################################################################

costofinal = 0
for x in mov:
    if x == (1, 1) or x == (-1, -1) or x == (-1, 1) or x == (1, -1):
        costofinal = costofinal + (((1 / resolution) ** 2) * 2) ** (1 / 2)
    else:
        costofinal = costofinal + (1 / resolution)

# print(mov)
# print(acciones)
# print(visited)
# print(path)
#print(accionesfluidas)
#print('El cossto final del recorrido es: ', costofinal)

quitting = False
while not quitting:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quitting = True
    pg.display.update()

pg.quit()
quit()
