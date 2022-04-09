import math
import pygame
from pygame import Vector2

import Config
from Bullet import Bullet
from Utility import checkCollisionCircle

class BulletManager:


    def __init__(self, game):
        self.bullets = []
        self.game = game
        self.astManager = game.astManager

    def update(self, _dt):
        newBullets = []    
        asteriods = self.astManager.asteriods
        for i in range(len(self.bullets)):
            bullet = self.bullets[i]
            bullet.update(_dt)

            # asteriod collision
            for j in range(len(asteriods)):
                ast = asteriods[j]
                collide = checkCollisionCircle(bullet, ast)
                if(collide):
                    ast.markedForDelete = True
                    bullet.markedForDelete = True
            
            # screen border collision
            if bullet.x < 0 or bullet.x > Config.screen_width or bullet.y < 0 or bullet.y > Config.screen_height:
                bullet.markedForDelete = True

            # delete
            if bullet.markedForDelete:
                del bullet
            else:
                newBullets.append(bullet)

        self.bullets = newBullets

 

    def shoot(self):
        bullet = Bullet(self.game)
        self.bullets.append(bullet)

    def draw(self, window):
        for i in range(len(self.bullets)):
            self.bullets[i].draw(window)

    