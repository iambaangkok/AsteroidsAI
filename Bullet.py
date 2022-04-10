from copy import deepcopy
import math
import random
import numpy as np

import pygame
from pygame import Vector2

import Config
import Colors
from Utility import clamp


class Bullet:



    def __init__(self, game):

        self.game = game
        self.player = game.player

        self.circleRadius = 4
        self.scale = 1

        self.circleColor = Colors.RED

        self.rotation = 90
        
        self.x = self.player.x
        self.y = self.player.y
        self.moveSpeed = Vector2(0,0)
        self.moveSpeedMax = 0.5
        self.moveAcceleration = 0.02
        self.moveDeceleration = 0.0001
        
        self.markedForDelete = False

        #####

        forward = self.player.getForwardVector()
        self.moveSpeed.x = forward.x * self.moveSpeedMax
        self.moveSpeed.y = forward.y * self.moveSpeedMax

        if self.moveSpeed.magnitude() > self.moveSpeedMax:
            factor = self.moveSpeedMax / self.moveSpeed.magnitude()
            self.moveSpeed *= factor

    def update(self, _dt):
        # movement
        self.x += self.moveSpeed.x * _dt
        self.y += self.moveSpeed.y * _dt

    def draw(self, window):
        pygame.draw.circle(window, self.circleColor, (self.x, self.y), 1, 1)
        pygame.draw.circle(window, self.circleColor, (self.x, self.y), self.circleRadius * self.scale, 1)

    