
import math
import pygame

from pygame import Vector2
import Colors
from Utility import getSlope

class Raycaster:

    def __init__(self, game):

        self.game = game
        self.player = game.player
        self.astManager = game.astManager
        
        self.nAngles = 16
        self.degreePerAngle = 360/self.nAngles
        
        self.angles = []
        for i in range(0, self.nAngles):
            self.angles.append(self.degreePerAngle*i)

        self.lineColor0 = Colors.YELLOW
        self.lineColor1 = Colors.WHITE_153
        self.lineColor2 = Colors.WHITE_34

        self.lengthLimit = 600

        self.debug = True

    def update(self, _dt):
        pass


    def draw(self, window):

        for i in range(0, self.nAngles):
            forward = self.player.getForwardVector()
            angle = self.angles[i]
            rotatedDirection = forward.rotate(angle).normalize()
            
            startPoint = Vector2(self.player.x, self.player.y) # x1 y1
            endPoint = startPoint + rotatedDirection * self.lengthLimit # x2 y2

            # check collision with asteriods
            asteriods = self.astManager.asteriods
            for j in range(0, len(asteriods)): # with help from khawhom
                # generate line equation Ax + By + C = 0 from (y-y1) = m(x-x1) -> y = mx + (-mx1 + y1) -> mx - y + (-mx1 + y1) = 0 
                ast = asteriods[j]

                p1 = startPoint
                p2 = endPoint
                m = getSlope(p1.x,p2.x,p1.y,p2.y)

                A = m
                B = -1
                C = (-m * p1.x + p1.y)

                x3 = ast.x
                y3 = ast.y

                if self.debug:
                    if i == 0:
                        pygame.draw.line(window, Colors.RED, startPoint, (x3,y3))
                        pygame.draw.circle(window, Colors.YELLOW, endPoint, 8, 1)
                        #pygame.draw.line(window, Colors.RED, (x3,y3), (0,0))

                distance = abs(A*x3 + B*y3 + C)/(math.hypot(A, B))
                radius = ast.circleRadius * ast.scale
                if (distance <= radius): # ray hit the asteroid
                    xMin = min(p1.x,p2.x)
                    xMax = max(p1.x,p2.x)
                    yMin = min(p1.y,p2.y)
                    yMax = max(p1.y,p2.y)

                    if (xMin <= x3 and x3 <= xMax and yMin <= y3 and  y3 <= yMax):
                        print("hit ", i, distance)

            if i == 0:
                
                pygame.draw.line(window, self.lineColor0, startPoint, endPoint)
            elif i%2 == 0:
                pygame.draw.line(window, self.lineColor1, startPoint, endPoint)
            else:
                pygame.draw.line(window, self.lineColor2, startPoint, endPoint)
        
        pass