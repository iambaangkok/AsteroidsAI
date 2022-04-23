import random
import pygame
from pygame import Vector2

import Config
import Colors
from Asteriod import Asteriod
from Utility import checkCollisionCircle

class AsteriodManager:

    def __init__(self, games = []):
        self.games = games

        self.circleColor = Colors.YELLOW_DIRT

        self.spawnRate = Config.asteriod_spawnrate # x per second
        self.spawnInterval = 1/self.spawnRate
        self.spawnIntervalCounter = self.spawnInterval #0
        self.limit = self.spawnRate * Config.genetic_simulationtime # no more than x asteriods on screen at same time

        self.asteriods = []

        # FORCE STAYING IN PLACE TO BE OBSOLETE
        self.spawn(False, Config.game_left + Config.game_width/2, Config.game_top + 1, 0, 0.2)

    def update(self, _dt):
        # spawn
        self.spawnIntervalCounter += _dt/1000
    
        while(self.spawnIntervalCounter >= self.spawnInterval):
            self.spawnIntervalCounter -= self.spawnInterval
            if(len(self.asteriods) < self.limit):
                self.spawn()
            else:
                self.spawnIntervalCounter = 0
        
        # update 
        newAsteriods = []
        
        for i in range(len(self.asteriods)):
            ast = self.asteriods[i]
            ast.update(_dt)

            for j in range(0, len(self.games)):
                game = self.games[j]
                if checkCollisionCircle(ast, game.player) and not ast.hasCollided[game.id]:
                    ast.hasCollided[game.id] = True
                    ast.markedForDelete += 1
                    game.scoreManager.addScoreFromAsteriod()

                    game.player.isAlive = False

            # delete
            if ast.markedForDelete >= len(self.games):
                del ast
            else:
                newAsteriods.append(ast)
        self.asteriods = newAsteriods

    def draw(self, window, gameId):
        for i in range(len(self.asteriods)):
            ast = self.asteriods[i]
            if not ast.hasCollided[gameId]:
                ast.draw(window)

    def spawn(self, random = True, x = 0, y = 0, rotation = 0, moveSpeedMax = 1):
        ast = Asteriod()
        self.asteriods.append(ast)
        ast.circleColor = self.circleColor
        ast.randomSelf()
        if not random:
            ast.x = x
            ast.y = y
            ast.rotation = rotation
            ast.moveSpeedMax = moveSpeedMax
            ast.calculateMoveSpeed()