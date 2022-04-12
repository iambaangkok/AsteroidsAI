import random
import pygame
from pygame import Vector2

import Config
import Colors
from Asteriod import Asteriod
from Utility import checkCollisionCircle

class AsteriodManager:

    def __init__(self, game):
        self.game = game
        self.player = game.player
        self.scoreManager = game.scoreManager

        self.circleColor = Colors.YELLOW_DIRT

        self.spawnRate = 0.75 # x per second
        self.spawnInterval = 1/self.spawnRate
        self.spawnIntervalCounter = self.spawnInterval #0
        self.limit = 10 # no more than x asteriods on screen at same time

        self.asteriods = []

    def update(self, _dt):
        self.spawnIntervalCounter += _dt/1000

        if(self.spawnIntervalCounter >= self.spawnInterval):
            self.spawnIntervalCounter -= self.spawnInterval
            if(len(self.asteriods) < self.limit):
                self.spawn()

        newAsteriods = []
        
        for i in range(len(self.asteriods)):
            ast = self.asteriods[i]
            ast.update(_dt)

            if checkCollisionCircle(ast, self.player):
                self.player.isAlive = False
                ast.markedForDelete = True

            # delete
            if ast.markedForDelete:
                del ast
                self.scoreManager.addScoreFromAsteriod()
            else:
                newAsteriods.append(ast)
        
        self.asteriods = newAsteriods

    def draw(self, window):
        for i in range(len(self.asteriods)):
            self.asteriods[i].draw(window)

    def spawn(self):
        ast = Asteriod()
        self.asteriods.append(ast)
        ast.circleColor = self.circleColor
        ast.randomSelf()