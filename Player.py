from copy import deepcopy
import numpy as np
import pygame
from pygame import Vector2

from Utility import clamp
import Config
import Colors

class Player:
    def __init__(self, game):

        self.game = game

        self.polygon = [
            Vector2(0,8),
            Vector2(-5,-4),
            Vector2(0,-3),
            Vector2(5,-4)
        ]
        self.circleRadius = 8
        self.scale = 1.5

        self.polygonColor = Colors.GREEN_JUNGLE
        self.circleColor = Colors.MAGENTA

        self.playerWidth = 0

        self.rotation = 180
        self.angularSpeed = 0
        self.angularSpeedMax = 0.4
        self.angularAcceleration = 0.0006
        self.angularDeceleration = 0.0006
        
        self.x = Config.game_left + Config.game_width/2
        self.y = Config.game_top + Config.game_height/2
        self.moveSpeed = Vector2(0,0)
        self.moveSpeedMax = 0.4
        self.moveAcceleration = 0.0006
        self.moveDeceleration = 0.0001

        self.fireRate = 3 # x shots per second
        self.shootInterval = 1/self.fireRate
        self.shootIntervalCounter = 0

        self.isAlive = True

        #####

    def update(self, _dt, inputs = []):
        if Config.debug_player_invincible:
            self.isAlive = True
        if not self.isAlive:
            self.moveSpeed = Vector2(0,0)
            self.polygonColor = Colors.RED
            return

        keys = pygame.key.get_pressed()

        # angular 
        angularInput = 0
        if (keys[pygame.K_a] and Config.debug_player_manualcontrol) or (len(inputs) >= 4 and inputs[0] and Config.debug_player_neuralcontrol):
            angularInput -= 1
        if (keys[pygame.K_d] and Config.debug_player_manualcontrol) or (len(inputs) >= 4 and inputs[1] and Config.debug_player_neuralcontrol):
            angularInput += 1            

        self.angularSpeed += angularInput * self.angularAcceleration * _dt
        sign = 0
        if angularInput == 0:
            sign = np.sign(self.angularSpeed)
            if(abs(self.angularSpeed) > self.angularDeceleration * _dt):
                self.angularSpeed += (-sign) * self.angularDeceleration * _dt
            elif(abs(self.angularSpeed) <= self.angularDeceleration * _dt):
                self.angularSpeed = 0

        self.angularSpeed = clamp(self.angularSpeed, -self.angularSpeedMax, self.angularSpeedMax)
        self.rotation += self.angularSpeed * _dt
        
        if(self.rotation >= 360):
            self.rotation -= 360
        if(self.rotation < -0):
            self.rotation = 360 - abs(self.rotation)

        # movement
        if (keys[pygame.K_w] and Config.debug_player_manualcontrol) or (len(inputs) >= 4 and inputs[3] and Config.debug_player_neuralcontrol):
            forward = Vector2(0,1).rotate(self.rotation).normalize()
            self.moveSpeed.x += forward.x * self.moveAcceleration * _dt
            self.moveSpeed.y += forward.y * self.moveAcceleration * _dt


        signX = np.sign(self.moveSpeed.x)
        if(abs(self.moveSpeed.x) > self.moveDeceleration * _dt):
            self.moveSpeed.x += (-signX) * self.moveDeceleration * _dt
        elif(abs(self.moveSpeed.x) <= self.moveDeceleration * _dt):
            self.moveSpeed.x = 0

        signY = np.sign(self.moveSpeed.y)
        if(abs(self.moveSpeed.y) > self.moveDeceleration * _dt):
            self.moveSpeed.y += (-signY) * self.moveDeceleration * _dt
        elif(abs(self.moveSpeed.y) <= self.moveDeceleration * _dt):
            self.moveSpeed.y = 0

        if self.moveSpeed.magnitude() > self.moveSpeedMax:
            factor = self.moveSpeedMax / self.moveSpeed.magnitude()
            self.moveSpeed *= factor

        
        self.x += self.moveSpeed.x * _dt
        self.y += self.moveSpeed.y * _dt

        # screen border collision
        if self.x < Config.game_left :
            self.x = Config.game_right
        if self.x > Config.game_right:
            self.x = Config.game_left

        if self.y < Config.game_top :
            self.y = Config.game_bottom
        if self.y > Config.game_bottom:
            self.y = Config.game_top

        # shooting
        self.shootIntervalCounter += _dt/1000
        if ((keys[pygame.K_SPACE] or keys[pygame.K_k]) and Config.debug_player_manualcontrol) or (len(inputs) >= 4 and inputs[2] and Config.debug_player_neuralcontrol):
            if self.shootIntervalCounter >= self.shootInterval:
                self.shootIntervalCounter = 0
                self.shoot()

    def shoot(self):
        self.game.bulletsManager.shoot()

    def draw(self, window):
        pygame.draw.polygon(window, self.polygonColor, self.getPolygon(), self.playerWidth)
        if Config.debug_player_hitbox_show:
            self.drawHitBox(window)

    def drawHitBox(self, window):
        pygame.draw.circle(window, self.circleColor, (self.x, self.y), 1, 1)
        pygame.draw.circle(window, self.circleColor, (self.x, self.y), self.circleRadius * self.scale, 1)

    def getForwardVector(self):
        return Vector2(0,1).rotate(self.rotation).normalize()

    def getPolygon(self):
        return self.getPolygonAtPoint((self.x,self.y))

    def getPolygonAtPoint(self, point = Vector2(0,0)):
        newPolygon = deepcopy(self.polygon)
        for i in range(len(newPolygon)):
            newPolygon[i] = newPolygon[i].rotate(self.rotation);
            newPolygon[i] = newPolygon[i] * self.scale
            newPolygon[i] += point

        return newPolygon