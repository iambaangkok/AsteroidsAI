import pygame
from pygame import Vector2
from pygame import Rect

import Colors
import Config
from AsteriodManager import AsteriodManager
from BulletManager import BulletManager
from Player import Player
from Raycaster import Raycaster


def main():
    game = AsteriodsGame()
    game.run()

class AsteriodsGame:
    
    def __init__(self):
        self.setup()

    def setup(self):
        self.window = pygame.display.set_mode((Config.screen_width, Config.screen_height))
        self.clock = pygame.time.Clock()

        self.gameWindow = Rect(Config.game_x, Config.game_y, Config.game_width, Config.game_height)

        self.player = Player(self)
        self.astManager = AsteriodManager(self)
        self.bulletsManager = BulletManager(self)

        self.raycaster = Raycaster(self)

        self.gameState = 1

        pygame.display.set_caption("AsteriodsAI")

    def run(self):
        self.setup()
        while(self.gameState != 0):
            keys=pygame.key.get_pressed()
            if keys[pygame.K_r] and keys[pygame.K_LCTRL]:
                self.setup()

            #####

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
        
        # game elements
        self.raycaster.draw(self.window)

        self.player.draw(self.window)
        self.player.drawHitBox(self.window)
        
        self.astManager.draw(self.window)
        self.bulletsManager.draw(self.window)

        # cover up
        pygame.draw.rect(self.window, Colors.BLACK, Rect(0, 0, Config.game_x, Config.screen_height))
        pygame.draw.rect(self.window, Colors.BLACK, Rect(Config.game_x, 0, Config.game_width, Config.game_y))
        pygame.draw.rect(self.window, Colors.BLACK, Rect(Config.game_right, 0, Config.screen_width-Config.game_right, Config.screen_height))
        pygame.draw.rect(self.window, Colors.BLACK, Rect(Config.game_x, Config.game_bottom, Config.game_width, Config.screen_height-Config.game_height))

        # game window border
        pygame.draw.rect(self.window, Colors.WHITE, self.gameWindow, 1)

        pygame.display.update()





###########################

if __name__ == "__main__":
    main()

###########################