import pygame
from pygame import Vector2
from pygame import Rect

import Colors
import Config
from AsteriodManager import AsteriodManager
from BulletManager import BulletManager
from Player import Player
from Raycaster import Raycaster
from ScoreManager import ScoreManager


class AsteriodsGame:
    
    currentId = 0

    def __init__(self, astAI):
        self.astAI = astAI
        self.id = self.currentId
        self.currentId += 1
        self.setup()

    def setup(self):
        pygame.init()
        self.window = pygame.display.set_mode((Config.screen_width, Config.screen_height))
        self.clock = pygame.time.Clock()

        self.gameWindow = Rect(Config.game_x, Config.game_y, Config.game_width, Config.game_height)

        self.player = Player(self)
        self.scoreManager = ScoreManager(self)

        self.astManager = self.astAI.astManager
        self.bulletsManager = BulletManager(self)

        self.raycaster = Raycaster(self)

        self.gameState = 1

        pygame.display.set_caption("AsteriodsAI")

    def run(self):
        self.setup()
        while(self.gameState != 0):
            keys=pygame.key.get_pressed()
            if keys[pygame.K_r] and keys[pygame.K_LCTRL]: # reset
                self.setup()

            #####

            _dt = self.clock.tick(Config.frame_rate)
            if(_dt < Config.frame_time_millis):
                pygame.time.wait(Config.frame_time_millis - _dt)

            self.update(_dt)
            self.draw()    
                    
        pygame.quit()

    def quit(self):
        pygame.quit()

    def update(self, _dt, inputs = []):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameState = 0
                self.astAI.simulationState = 0

        self.player.update(_dt, inputs)

        self.astManager.update(_dt)
        self.bulletsManager.update(_dt)

        self.scoreManager.update(_dt)

    def draw(self, updateDisplay = True, drawRay = True, drawPlayer = True, drawAsteriods = True,
        drawBullets = True, drawCoverUp = True, drawWindowBorder = True, drawScore = True,
        drawBg = True
        ):

        if Config.game_draw_bg and drawBg:
            self.window.fill(Colors.BLACK)
        
        # game elements
        if drawRay:
            self.raycaster.draw(self.window)

        if drawPlayer:
            self.player.draw(self.window)
        
        if drawAsteriods:
            self.astManager.draw(self.window)

        if drawBullets:
            self.bulletsManager.draw(self.window)

        # cover up
        if drawCoverUp:
            pygame.draw.rect(self.window, Colors.BLACK, Rect(0, 0, Config.game_x, Config.screen_height))
            pygame.draw.rect(self.window, Colors.BLACK, Rect(Config.game_x, 0, Config.game_width, Config.game_y))
            pygame.draw.rect(self.window, Colors.BLACK, Rect(Config.game_right, 0, Config.screen_width-Config.game_right, Config.screen_height))
            pygame.draw.rect(self.window, Colors.BLACK, Rect(Config.game_x, Config.game_bottom, Config.game_width, Config.screen_height-Config.game_height))

        # game window border
        if drawWindowBorder:
            pygame.draw.rect(self.window, Colors.WHITE, self.gameWindow, 1)
        
        if drawScore:
            self.scoreManager.draw(self.window)

        if updateDisplay:
            pygame.display.update()





