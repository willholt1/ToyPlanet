import math
import numpy as np
#calculate the distance between two points
def getDistance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
#calculate the angle between two vectors
def angleBetween(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))

def getVectors(creatureX, creatureY, foodX, foodY):
    xVector = foodX - creatureX
    yVector = foodY - creatureY
    return (xVector, yVector)

def adjustAngle(angle):
    if angle > 180:
        angle = 360 - angle
    else:
        angle = angle * -1
    return angle