from copy import deepcopy
import pygame
from pygame import Vector2

class Player:
    polygon = [
        Vector2(0,10),
        Vector2(-5,-2),
        Vector2(0,1),
        Vector2(5,-2)
    ]





    def getPolygonAtPoint(self, point = Vector2(0,0)):
        newPolygon = deepcopy(self.polygon)
        for i in range(len(newPolygon)):
            newPolygon[i] += point

        print(newPolygon)#[0], " ", self.polygon[0])
        return newPolygon