import pygame
from pygame import Vector2

from Asteriod import Asteriod
from Utility import checkCollisionCircle

class AsteriodManager:


    spawnRate = 0.75 # x per second
    spawnInterval = 1/spawnRate
    spawnIntervalCounter = 0

    def __init__(self, game):
        self.game = game
        self.player = game.player
        self.asteriods = []

    def update(self, _dt):
        self.spawnIntervalCounter += _dt/1000

        if(self.spawnIntervalCounter >= self.spawnInterval):
            self.spawnIntervalCounter -= self.spawnInterval
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
            else:
                newAsteriods.append(ast)
        
        self.asteriods = newAsteriods

    def draw(self, window):
        for i in range(len(self.asteriods)):
            self.asteriods[i].draw(window)

    def spawn(self):
        asteriod = Asteriod()
        self.asteriods.append(asteriod)