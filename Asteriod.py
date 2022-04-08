from copy import deepcopy
import random
import numpy as np
import pygame
from pygame import Vector2

from Utility import clamp
import Config
import Colors

class Asteriod:



    def __init__(self):
        self.circleRadius = 8
        self.scale = 4

        self.circleColor = Colors.WHITE

        self.rotation = 90
        
        self.x = Config.screen_width/2
        self.y = Config.screen_height/2
        self.moveSpeed = Vector2(0,0)
        self.moveSpeedMax = 0.4
        self.moveAcceleration = 0.02
        self.moveDeceleration = 0.0001
        
        #####

        self.scale = random.random() * 3 + 1
        self.rotation = random.randint(0, 360)
        self.moveSpeedMax = random.random() * 0.2 + 0.05

        if((self.rotation > 270+45 and self.rotation <= 0) or (self.rotation >= 0 and self.rotation < 0+45)): #top spawn
            self.x = random.randint(1,Config.screen_width-1)
            self.y = 0+1
        elif(self.rotation >= 90-45 and self.rotation < 90+45): #right spawn
            self.x = Config.screen_width-1
            self.y = random.randint(1,Config.screen_height-1)
        elif(self.rotation >= 180-45 and self.rotation < 180-45): #bottom spawn
            self.x = random.randint(1,Config.screen_width-1)
            self.y = Config.screen_height-1
        else: #top spawn
            self.x = 0+1
            self.y = random.randint(1,Config.screen_height-1)
            
        
        

        forward = Vector2(0,1).rotate(self.rotation).normalize()
        self.moveSpeed.x = forward.x * self.moveSpeedMax
        self.moveSpeed.y = forward.y * self.moveSpeedMax

        if self.moveSpeed.magnitude() > self.moveSpeedMax:
            factor = self.moveSpeedMax / self.moveSpeed.magnitude()
            self.moveSpeed *= factor

    def update(self, _dt):

        # movement
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
        pygame.draw.circle(window, self.circleColor, (self.x, self.y), 1, 1)
        pygame.draw.circle(window, self.circleColor, (self.x, self.y), self.circleRadius * self.scale, 1)