#sets foodDirection to be -1 if the food is to the left, 0 if it is in front and 1 if it is to the right
#creatures gain fitness if the closest food is in front of them
def checkFoodDirection(self):
    if (self.direction == UP):
        if (self.nearestFoodX < self.rect.centerx):
            self.foodDirection = -1
        elif (self.nearestFoodX == self.rect.centerx):
            self.foodDirection = 0
            self.fitness += 0.1
        else:
            self.foodDirection = 1
    elif (self.direction == DOWN):
        if (self.nearestFoodX > self.rect.centerx):
            self.foodDirection = -1
        elif (self.nearestFoodX == self.rect.centerx):
            self.foodDirection = 0
            self.fitness += 0.1
        else:
            self.foodDirection = 1
    elif (self.direction == LEFT):
        if (self.nearestFoodY > self.rect.centery):
            self.foodDirection = -1
        elif (self.nearestFoodY == self.rect.centery):
            self.foodDirection = 0
            self.fitness += 0.1
        else:
            self.foodDirection = 1
    else:
        if (self.nearestFoodY < self.rect.centery):
            self.foodDirection = -1
        elif (self.nearestFoodY == self.rect.centery):
            self.foodDirection = 0
            self.fitness += 0.1
        else:
            self.foodDirection = 1

#return[self.foodDirection, self.nearestFoodDistance]


#in view up
        if (((self.rect.centery - self.viewDistance) <= self.nearestPredatorY <= self.rect.centery) and ((self.rect.centerx - 10) <= self.nearestPredatorX <= (self.rect.centerx + 10))):
            predatorUp = self.rect.centery - self.nearestPredatorY
            if (predatorUp < 0):
                predatorUp = predatorUp * -1
        #in view down
        elif ((self.rect.centery <= self.nearestPredatorY <= (self.rect.centery + self.viewDistance)) and ((self.rect.centerx - 10) <= self.nearestPredatorX <= (self.rect.centerx + 10))):
            predatorDown = self.rect.centery - self.nearestPredatorY
            if (predatorDown < 0):
                predatorDown = predatorDown * -1
        #in view left
        elif (((self.rect.centerx - self.viewDistance) <= self.nearestPredatorX <= self.rect.centerx) and ((self.rect.centery - 10) <= self.nearestPredatorY <= (self.rect.centery + 10))):
            predatorLeft = self.rect.centerx - self.nearestPredatorX
            if (predatorLeft < 0):
                predatorLeft = predatorLeft * -1
        #in view right
        elif ((self.rect.centerx <= self.nearestPredatorX <= (self.rect.centerx + self.viewDistance)) and ((self.rect.centery - 10) <= self.nearestPredatorY <= (self.rect.centery + 10))):
            predatorRight = self.rect.centerx - self.nearestPredatorX
            if (predatorRight < 0):
                predatorRight = predatorRight * -1