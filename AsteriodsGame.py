from time import sleep
import pygame
import Colors
import Config
from Player import Player
from pygame import Vector2



def main():
    game = AsteriodsGame()
    game.run()

class AsteriodsGame:
    
    window = pygame.display.set_mode((Config.screen_width, Config.screen_height))
    clock = pygame.time.Clock()

    player = Player()

    gameState = 1

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

    def draw(self):
        self.window.fill(Colors.BLACK)
        #pygame.draw.circle(self.WINDOW, Colors.GREEN_JUNGLE, (Config.SCREEN_WIDTH/2, Config.SCREEN_HEIGHT/2), 20, 1)

        self.player.draw(self.window)
        self.player.drawHitBox(self.window)
        
        pygame.display.update()





###########################

if __name__ == "__main__":
    main()

###########################