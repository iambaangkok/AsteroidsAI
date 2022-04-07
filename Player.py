from copy import deepcopy
import numpy as np
import pygame
from pygame import K_a, K_d, Vector2
from Utility import clamp

class Player:
    polygon = [
        Vector2(0,10),
        Vector2(-5,-2),
        Vector2(0,1),
        Vector2(5,-2)
    ]

    rotation = 90
    angularSpeed = 0
    angularSpeedMax = 0.75
    angularAcceleration = 0.05
    angularDeceleration = 0.05
    
    def update(self):
        keys = pygame.key.get_pressed()

        # angular 
        angularInput = 0
        if keys[K_a]:
            angularInput -= 1
        if keys[K_d]:
            angularInput += 1            

        self.angularSpeed += angularInput * self.angularAcceleration
        sign = 0
        if angularInput == 0:
            sign = np.sign(self.angularSpeed)
            if(abs(self.angularSpeed) > self.angularDeceleration):
                self.angularSpeed += self.angularDeceleration * (-sign) 
            elif(abs(self.angularSpeed) <= self.angularDeceleration):
                self.angularSpeed = 0

        self.angularSpeed = clamp(self.angularSpeed, -self.angularSpeedMax, self.angularSpeedMax)
        self.rotation += self.angularSpeed


    def getPolygonAtPoint(self, point = Vector2(0,0)):
        newPolygon = deepcopy(self.polygon)
        for i in range(len(newPolygon)):
            newPolygon[i] = newPolygon[i].rotate(self.rotation + 90);
            newPolygon[i] += point

        #print(newPolygon)#[0], " ", self.polygon[0])
        return newPolygon