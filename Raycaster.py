
from cmath import isnan
import math
import pygame

from pygame import Vector2
import Config
import Colors
from Utility import getLineCircleIntersectionPoint, getLinearEquation, getPointDistance, getPointToLineDistance, getSlope, getYCircleEquation

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

        self.font = pygame.font.SysFont("UbuntuMono", 14)
        self.lineColor0 = Colors.WHITE_221
        self.lineColor1 = Colors.WHITE_119
        self.lineColor2 = Colors.WHITE_34
        self.circleColor = Colors.WHITE_119
        self.distanceColor = Colors.WHITE_187

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

            if ast.hasCollided[self.game.id]:
                continue

            x3 = ast.x
            y3 = ast.y

            distance = math.inf
            if m == math.inf:
                distance = abs(p1.x-x3)
            else:
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

                if math.isnan(ansX1) or math.isnan(ansX2):
                    ansX1 = p1.x
                    ansX2 = p1.x
                    ansY1, ansY2 = getYCircleEquation(ansX1, r, ast.x, ast.y)
                
                dist1 = getPointDistance(p1.x, p1.y, ansX1, ansY1)
                dist2 = getPointDistance(p1.x, p1.y, ansX2, ansY2)

                if dist1 < getPointDistance(p1.x, p1.y, endPoint.x, endPoint.y):
                    if ((xMin <= ansX1 and ansX1 <= xMax) and (yMin <= ansY1 and  ansY1 <= yMax)):
                        endPoint = Vector2(ansX1, ansY1)
                if dist2 < getPointDistance(p1.x, p1.y, endPoint.x, endPoint.y):
                    if ((xMin <= ansX2 and ansX2 <= xMax) and (yMin <= ansY2 and  ansY2 <= yMax)):
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

            if Config.debug_ray_show:
                pygame.draw.line(window, color, startPoint, endPoint)
                if Config.debug_ray_tip_show:
                    pygame.draw.circle(window, self.circleColor, endPoint, 4, 1)
                if Config.debug_ray_distance_show:
                    text = self.font.render(str(math.floor(self.distance[i])), True, self.distanceColor)
                    text_rect = text.get_rect()
                    text_rect.centerx = self.endPoints[i].x
                    text_rect.bottom = self.endPoints[i].y
                    window.blit(text, text_rect)
