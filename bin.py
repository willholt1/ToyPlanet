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