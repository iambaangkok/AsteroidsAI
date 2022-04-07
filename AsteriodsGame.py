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


    player = Player()

    gameState = 1

    def setup(self):
        pygame.display.set_caption("AsteriodsAI")

    def run(self):
        self.setup()

        while(self.gameState != 0):
            self.getInput()
            self.update()
            self.draw()    
                    
        pygame.quit()


    def getInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameState = 0

    def update(self):
        self.player.update()
        pass

    def draw(self):
        self.window.fill(Colors.BLACK)
        #pygame.draw.circle(self.WINDOW, Colors.GREEN_JUNGLE, (Config.SCREEN_WIDTH/2, Config.SCREEN_HEIGHT/2), 20, 1)

        playerPolygon = self.player.getPolygonAtPoint(Vector2(Config.screen_width/2, Config.screen_height/2))
        pygame.draw.polygon(self.window, Colors.GREEN_JUNGLE, playerPolygon, 1)
        
        pygame.display.update()





###########################

if __name__ == "__main__":
    main()

###########################