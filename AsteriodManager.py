import pygame
from pygame import Vector2

from Asteriod import Asteriod

class AsteriodManager:

    asteriods = []

    spawnRate = 1 # x per second
    spawnInterval = 1/spawnRate
    spawnIntervalCounter = 0

    def __init__(self):
        pass

    def update(self, _dt):
        self.spawnIntervalCounter += _dt/1000

        if(self.spawnIntervalCounter >= self.spawnInterval):
            self.spawnIntervalCounter -= self.spawnInterval
            self.spawn()
        
        for i in range(len(self.asteriods)):
            self.asteriods[i].update(_dt)

    def draw(self, window):
        for i in range(len(self.asteriods)):
            self.asteriods[i].draw(window)

    def spawn(self):
        asteriod = Asteriod()
        self.asteriods.append(asteriod)