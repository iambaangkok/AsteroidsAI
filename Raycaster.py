
import pygame

from pygame import Vector2
import Colors

class Raycaster:

    def __init__(self, game):

        self.game = game
        self.player = game.player
        
        self.nAngles = 16
        self.degreePerAngle = 360/self.nAngles
        
        self.angles = []
        for i in range(0, self.nAngles):
            self.angles.append(self.degreePerAngle*i)

        self.lineColor0 = Colors.YELLOW
        self.lineColor1 = Colors.WHITE_153
        self.lineColor2 = Colors.WHITE_34

        self.lengthLimit = 1200

        
    def update(self, _dt):
        pass

    def draw(self, window):

        for i in range(0, self.nAngles):
            forward = self.player.getForwardVector()
            angle = self.angles[i]
            rotatedDirection = forward.rotate(angle).normalize()
            startPoint = Vector2(self.player.x, self.player.y)
            endPoint = startPoint + rotatedDirection * self.lengthLimit
            if i == 0:
                pygame.draw.line(window, self.lineColor0, startPoint, endPoint)
            elif i%2 == 0:
                pygame.draw.line(window, self.lineColor1, startPoint, endPoint)
            else:
                pygame.draw.line(window, self.lineColor2, startPoint, endPoint)
        
        pass