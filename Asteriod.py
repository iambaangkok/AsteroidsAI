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
        self.scale = 3

        self.circleColor = Colors.YELLOW_DIRT

        self.rotation = 90
        
        self.x = Config.screen_width/2
        self.y = Config.screen_height/2
        self.moveSpeed = Vector2(0,0)
        self.moveSpeedMax = 0.025
        self.moveAcceleration = 0.02
        self.moveDeceleration = 0.0001
        
        self.hasCollided = [False for i in range(0,Config.genetic_agentpergeneration)]
        self.markedForDelete = 0

        self.calculateMoveSpeed()


    def randomSelf(self):
        self.scale = random.random() * 3 + 3
        self.rotation = random.randint(0, 360)
        self.moveSpeedMax = random.random() * 0.2 + 0.025

        if((self.rotation > 270+45 and self.rotation <= 0) or (self.rotation >= 0 and self.rotation < 0+45)): #top spawn
            self.x = random.randint(Config.game_left+1,Config.game_right-1)
            self.y = Config.game_top+1
        elif(self.rotation >= 90-45 and self.rotation < 90+45): #right spawn
            self.x = Config.game_right-1
            self.y = random.randint(Config.game_top+1,Config.game_bottom-1)
        elif(self.rotation >= 180-45 and self.rotation < 180-45): #bottom spawn
            self.x = random.randint(Config.game_left+1,Config.game_right-1)
            self.y = Config.game_bottom-1
        else: #left spawn
            self.x = Config.game_left+1
            self.y = random.randint(Config.game_left+1,Config.game_right-1)
        
        self.calculateMoveSpeed()
            
        
    def calculateMoveSpeed(self):
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

        # screen border collision
        if self.x < Config.game_left :
            self.x = Config.game_right
        if self.x > Config.game_right:
            self.x = Config.game_left

        if self.y < Config.game_top :
            self.y = Config.game_bottom
        if self.y > Config.game_bottom:
            self.y = Config.game_top

    def draw(self, window):
        pygame.draw.circle(window, self.circleColor, (self.x, self.y), 1, 1)
        pygame.draw.circle(window, self.circleColor, (self.x, self.y), self.circleRadius * self.scale, 1)