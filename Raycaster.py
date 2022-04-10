
import math
import pygame

from pygame import Vector2
import Colors
from Utility import getLineCircleIntersectionPoint, getLineEquation, getPointDistance, getPointToLineDistance, getSlope

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

        self.lengthLimit = 800

        self.debug = True

    def update(self, _dt):
        pass

    def getEndpoint(self, startPoint, endPoint, i = -1):

        # generate line equation Ax + By + C = 0 from (y-y1) = m(x-x1) -> y = mx + (-mx1 + y1) -> mx - y + (-mx1 + y1) = 0
        # y = mx + C
        A,B,C,m,p1,p2 = getLineEquation(startPoint, endPoint)

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

                if (xMin <= x3 and x3 <= xMax and yMin <= y3 and  y3 <= yMax):
                    # find line-circle intersection point

                    # find circle equation (x-x3)^2 + (y-y3)^2 = r^2
                    # substitude with linear eq y = mx + C
                    # (x-x3)^2 + (mx + C -y3)^2 = r^2
                    # x^2 - 2xx3 + x3^2 + m^2x^2 + 2mx(C-y3) + (C-y3)^2 = r^2
                    # x = (1/(m^2+1)) * (+- sqrt(-(C*C) + 2y3(C+mx3)-2Cmx3 + m*m*r*r-m*m*x3*x3+r*r-y3*y3)-Cm+my3+x3))
                    
                    ansX1, ansX2 = getLineCircleIntersectionPoint(A,B,C,m,x3,y3,r)
                    if i == 0:
                        print(i, " ", m)
                        print(ansX1 , " " , ansX2)

                    ansY1 = m*ansX1+C
                    ansY2 = m*ansX2+C
                    
                    dist1 = getPointDistance(p1.x, p1.y, ansX1, ansY1)
                    dist2 = getPointDistance(p1.x, p1.y, ansX2, ansY2)

                    if dist1 < getPointDistance(p1.x, p1.y, endPoint.x, endPoint.y):
                        endPoint = Vector2(ansX1, ansY1)
                    if dist2 < getPointDistance(p1.x, p1.y, endPoint.x, endPoint.y):
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

            

        pass