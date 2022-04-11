import math
import pygame

import Config
import Colors

class ScoreManager:
    
    def __init__(self, game):
        self.game = game
        self.player = game.player

        self.score = 0
        self.scorePerSecond = 50
        self.scorePerAsteriod = 250

        self.margin = 10
        self.x = Config.game_right - self.margin
        self.y = Config.game_top + self.margin

        self.font = pygame.font.SysFont("UbuntuMono", 24)


    def update(self, _dt):
        if self.player.isAlive:
            self.score += self.scorePerSecond * _dt/1000

    def addScoreFromAsteriod(self):
        if self.player.isAlive:
            self.score += self.scorePerAsteriod

    def draw(self, window):
        text = self.font.render('score: ' + str(math.floor(self.score)), True, Colors.WHITE)
        text_rect = text.get_rect()
        text_rect.right = self.x
        text_rect.top = self.y
        window.blit(text, text_rect)
        pass
