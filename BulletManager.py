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
                if collide and not ast.hasCollided[self.game.id]:
                    ast.hasCollided[self.game.id] = True
                    ast.markedForDelete += 1
                    self.game.scoreManager.addScoreFromAsteriod()
                    
                    bullet.markedForDelete = True
                    
            
            # screen border collision
            if bullet.x < Config.game_left or bullet.x > Config.game_right or bullet.y < Config.game_top or bullet.y > Config.game_bottom:
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

    