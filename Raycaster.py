
import math
import pygame

from pygame import Vector2
import Colors
from Utility import getLineCircleIntersectionPoint, getLinearEquation, getPointDistance, getPointToLineDistance, getSlope

class Raycaster:

    def __init__(self, game):

        self.game = game
        self.player = game.player
        self.astManager = game.astManager

        self.nAngles = 16
        self.degreePerAngle = 360/self.nAngles

        self.angles = []
        self.endPoints = []
        self.distance = []
        for i in range(0, self.nAngles):
            self.angles.append(self.degreePerAngle*i)
            self.endPoints.append(Vector2(0,0))
            self.distance.append(0)


        self.lineColor0 = Colors.YELLOW
        self.lineColor1 = Colors.WHITE_119
        self.lineColor2 = Colors.WHITE_34

        self.lengthLimit = 1000

        self.debug = True

    def update(self, _dt):
        pass

    def getEndpoint(self, startPoint, endPoint, i = -1):
        # find line equation
        A,B,C,m,p1,p2 = getLinearEquation(startPoint, endPoint)

        # check collision with asteriods
        asteriods = self.astManager.asteriods
        for j in range(0, len(asteriods)): # with help from khawhom
            ast = asteriods[j]
            x3 = ast.x
            y3 = ast.y
            
            distance = getPointToLineDistance(A,B,C,x3,y3)
            r = ast.circleRadius * ast.scale
            if (distance <= r): # ray hit the asteroid
                xMin = min(p1.x,p2.x)
                xMax = max(p1.x,p2.x)
                yMin = min(p1.y,p2.y)
                yMax = max(p1.y,p2.y)
                # find line-circle intersection point
                ansX1, ansX2 = getLineCircleIntersectionPoint(A,B,C,m,x3,y3,r)
                ansY1 = m*ansX1+C
                ansY2 = m*ansX2+C
                
                dist1 = getPointDistance(p1.x, p1.y, ansX1, ansY1)
                dist2 = getPointDistance(p1.x, p1.y, ansX2, ansY2)

                if dist1 < getPointDistance(p1.x, p1.y, endPoint.x, endPoint.y):
                    if ((xMin <= ansX1 and ansX1 <= xMax) or (yMin <= ansY1 and  ansY1 <= yMax)):
                        endPoint = Vector2(ansX1, ansY1)
                if dist2 < getPointDistance(p1.x, p1.y, endPoint.x, endPoint.y):
                    if ((xMin <= ansX2 and ansX2 <= xMax) or (yMin <= ansY2 and  ansY2 <= yMax)):
                        endPoint = Vector2(ansX2, ansY2)
        return endPoint


    def draw(self, window):
        for i in range(0, self.nAngles):
            forward = self.player.getForwardVector()
            angle = self.angles[i]
            rotatedDirection = forward.rotate(angle).normalize()

            startPoint = Vector2(self.player.x, self.player.y) # x1 y1
            endPoint = startPoint + rotatedDirection * self.lengthLimit # x2 y2
            endPoint = self.getEndpoint(startPoint, endPoint, i)
            self.endPoints[i] = endPoint
            self.distance[i] = getPointDistance(startPoint.x,startPoint.y, endPoint.x, endPoint.y)

            # actual drawing
            color = self.lineColor0
            if i == 0:
                color = self.lineColor0
            elif i%2 == 0:
                color = self.lineColor1
            else:
                color = self.lineColor2
            pygame.draw.line(window, color, startPoint, endPoint)
            pygame.draw.circle(window, self.lineColor1, endPoint, 8, 1)