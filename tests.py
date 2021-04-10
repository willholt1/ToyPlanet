UP = 0
DOWN = 180
LEFT = 90
RIGHT = 270

direction = UP

import numpy as np
def angleBetween(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))

def getVectors(creatureX, creatureY, foodX, foodY):
    xVec = foodX - creatureX
    yVec = foodY - creatureY
    return (xVec, yVec)

x1 = 10
y1 = 10

x2 = 10
y2 = 20

A = (500,500)

if (direction == UP):
    A = (0, -1)
elif (direction == DOWN):
    A = (0, 1)
elif (direction == LEFT):
    A = (-1, 0)
else:
    A = (1, 0)


B = getVectors(x1,y1,x2,y2)

angle = angleBetween(A, B)

if angle > 180:
    angle = 360 - angle
    angle = angle * -1

    

print(angle)
