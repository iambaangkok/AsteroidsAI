import pygame
import Colors



def main():
    game = AsteriodsGame()
    game.run()

class AsteriodsGame:
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280,720
    WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

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
        pass

    def draw(self):
        self.WINDOW.fill(Colors.WHITE)





###########################

if __name__ == "__main__":
    main()

###########################