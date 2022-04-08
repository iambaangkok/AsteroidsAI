from copy import deepcopy
import numpy as np
import pygame
from pygame import Vector2

from Utility import clamp
import Config
import Colors

class Player:
    polygon = [
        Vector2(0,8),
        Vector2(-5,-4),
        Vector2(0,-3),
        Vector2(5,-4)
    ]
    circleRadius = 8
    polygonScale = 4

    polygonColor = Colors.GREEN_JUNGLE
    circleColor = Colors.MAGENTA

    rotation = 90
    angularSpeed = 0
    angularSpeedMax = 0.4
    angularAcceleration = 0.02
    angularDeceleration = 0.001
    
    x = Config.screen_width/2
    y = Config.screen_height/2
    moveSpeed = Vector2(0,0)
    moveSpeedMax = 0.4
    moveAcceleration = 0.02
    moveDeceleration = 0.0001

    def update(self, _dt):
        keys = pygame.key.get_pressed()

        # angular 
        angularInput = 0
        if keys[pygame.K_a]:
            angularInput -= 1
        if keys[pygame.K_d]:
            angularInput += 1            

        self.angularSpeed += angularInput * self.angularAcceleration
        sign = 0
        if angularInput == 0:
            sign = np.sign(self.angularSpeed)
            if(abs(self.angularSpeed) > self.angularDeceleration * _dt):
                self.angularSpeed += (-sign) * self.angularDeceleration * _dt
            elif(abs(self.angularSpeed) <= self.angularDeceleration * _dt):
                self.angularSpeed = 0

        self.angularSpeed = clamp(self.angularSpeed, -self.angularSpeedMax, self.angularSpeedMax)
        self.rotation += self.angularSpeed * _dt


        # movement
        if keys[pygame.K_w]:
            forward = Vector2(0,1).rotate(self.rotation).normalize()
            self.moveSpeed.x += forward.x * self.moveAcceleration
            self.moveSpeed.y += forward.y * self.moveAcceleration


        signX = np.sign(self.moveSpeed.x)
        if(abs(self.moveSpeed.x) > self.moveDeceleration * _dt):
            self.moveSpeed.x += (-signX) * self.moveDeceleration * _dt
        elif(abs(self.moveSpeed.x) <= self.moveDeceleration * _dt):
            self.moveSpeed.x = 0

        signY = np.sign(self.moveSpeed.y)
        if(abs(self.moveSpeed.y) > self.moveDeceleration * _dt):
            self.moveSpeed.y += (-signY) * self.moveDeceleration * _dt
        elif(abs(self.moveSpeed.y) <= self.moveDeceleration * _dt):
            self.moveSpeed.y = 0

        if self.moveSpeed.magnitude() > self.moveSpeedMax:
            factor = self.moveSpeedMax / self.moveSpeed.magnitude()
            self.moveSpeed *= factor

        
        self.x += self.moveSpeed.x * _dt
        self.y += self.moveSpeed.y * _dt

        # screen border teleport
        if self.x < 0 :
            self.x = Config.screen_width
        if self.x > Config.screen_width:
            self.x = 0

        if self.y < 0 :
            self.y = Config.screen_height
        if self.y > Config.screen_height:
            self.y = 0

    def draw(self, window):
        pygame.draw.polygon(window, self.polygonColor, self.getPolygon(), 1)

    def drawHitBox(self, window):
        pygame.draw.circle(window, self.circleColor, (self.x, self.y), 1, 1)
        pygame.draw.circle(window, self.circleColor, (self.x, self.y), self.circleRadius * self.polygonScale, 1)

    def getPolygon(self):
        return self.getPolygonAtPoint((self.x,self.y))

    def getPolygonAtPoint(self, point = Vector2(0,0)):
        newPolygon = deepcopy(self.polygon)
        for i in range(len(newPolygon)):
            newPolygon[i] = newPolygon[i].rotate(self.rotation);
            newPolygon[i] = newPolygon[i] * self.polygonScale
            newPolygon[i] += point

        return newPolygon