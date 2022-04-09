import pygame
from pygame import Vector2

import Colors
import Config
from AsteriodManager import AsteriodManager
from BulletManager import BulletManager
from Player import Player


def main():
    game = AsteriodsGame()
    game.run()

class AsteriodsGame:
    
    def __init__(self):
        self.window = pygame.display.set_mode((Config.screen_width, Config.screen_height))
        self.clock = pygame.time.Clock()

        self.player = Player(self)
        self.astManager = AsteriodManager(self)
        self.bulletsManager = BulletManager(self)

        self.gameState = 1

    def setup(self):
        pygame.display.set_caption("AsteriodsAI")

    def run(self):
        self.setup()

        while(self.gameState != 0):
            _dt = self.clock.tick(Config.frame_rate)
            if(_dt < Config.frame_time_millis):
                pygame.time.wait(Config.frame_time_millis - _dt)

            self.update(_dt)
            self.draw()    

            
                    
        pygame.quit()

    def update(self, _dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameState = 0

        self.player.update(_dt)

        self.astManager.update(_dt)
        self.bulletsManager.update(_dt)

    def draw(self):
        self.window.fill(Colors.BLACK)

        self.player.draw(self.window)
        self.player.drawHitBox(self.window)
        
        self.astManager.draw(self.window)
        self.bulletsManager.draw(self.window)

        pygame.display.update()





###########################

if __name__ == "__main__":
    main()

###########################