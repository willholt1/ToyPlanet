###############################################
#useful functions found throughout the program#
###############################################
#libraries
import math
import numpy as np
import random
#classes
import Food
#misc
import constants

#calculate the distance between two points
def getDistance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
#calculate the angle between two vectors
def angleBetween(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))

#create vectors from given coordinates
def getVectors(creatureX, creatureY, foodX, foodY):
    xVector = foodX - creatureX
    yVector = foodY - creatureY
    return (xVector, yVector)

#convert angle from ranging 0 => 360 to -180 => 180
def adjustAngle(angle):
    if angle > 180:
        angle = 360 - angle
    else:
        angle = angle * -1
    return angle

#generate random x, y coordinates within the screen size
def randomXY():
    x = random.randint(constants.SPAWNBORDER, (constants.WORLDSIZE - constants.SPAWNBORDER))
    y = random.randint(constants.SPAWNBORDER, (constants.WORLDSIZE - constants.SPAWNBORDER))

    return x, y

#generate a single piece of food at a random point
def trainReplenishFood(foodList):
    x, y = randomXY()
    foodSprite = Food.Food('sprites/plant.png', x, y)
    foodList.append(foodSprite)
    return foodList