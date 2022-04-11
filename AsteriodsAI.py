from this import d
import numpy as np
import pygame
from pygame import Vector2
from pygame import Rect

import Colors
import Config
from TextObject import TextObject
from Utility import sigmoid
from AsteriodsGame import AsteriodsGame


def main():
    astAI = AsteriodAI()
    astAI.run()

class AsteriodAI:
    def __init__(self):
        self.game = AsteriodsGame(self)
        self.player = self.game.player
        self.raycaster = self.game.raycaster


        self.window = self.game.window

        ##### 

        self.simulationTime = 20 # x seconds
        self.frameLimit = self.simulationTime * Config.frame_rate
        self.frameCount = 0

        ##### Neural Network

        self.nLayers = 2 # only input and output
        
        self.inputInd = 0
        self.outputInd = self.nLayers-1
        
        self.inputLayer = [[]]
        for i in range(0, len(self.raycaster.distance)):
            self.inputLayer[0].append(self.raycaster.distance[i] )
        self.inputLayer[0].append(self.player.rotation)
        self.inputLayer = np.array(self.inputLayer)
        
        self.outputLayer = np.array([[ 0, 0, 0, 0 ]]).T

        self.nodes = np.array([
            self.inputLayer,
            self.outputLayer
        ])

        np.random.seed(1)

        self.synaptic_weights = 2 * np.random.random((len(self.nodes[self.inputInd][0]), len(self.nodes[self.outputInd])))

        print('Random starting weights: ')
        print(self.synaptic_weights)

        self.computeOutput()
        print('Inputs: ')
        print(self.inputLayer)
        print('Outputs: ')
        print(self.outputLayer)

        ##### User interface

        self.textFrameCount = TextObject('simulation time: ' + str(self.simulationTime) + '   frame: ' + str(self.frameCount) + '/' + str(self.frameLimit),
                                    Config.game_left + 10, Config.game_top + 10, 
                                    "UbuntuMono", 16, Colors.WHITE, "left", "top"
                                )        

    def computeOutput(self):
        # get input
        self.inputLayer = [[]]
        for i in range(0, len(self.raycaster.distance)):
            self.inputLayer[0].append(self.raycaster.distance[i] )
        self.inputLayer[0].append(self.player.rotation)

        self.inputLayer = np.array(self.inputLayer)

        self.outputLayer = np.array( sigmoid(np.dot(self.inputLayer, self.synaptic_weights)) )

    
    def run(self):
        while(self.game.gameState != 0):
            self.frameCount += 1
            if(self.frameCount >= self.frameLimit):
                self.game.setup()
                self.frameCount = 0
            

            self.computeOutput()
            print(self.outputLayer)
            
            _dt = Config.frame_time_millis
            self.game.update(_dt)
            self.game.draw(False)

            self.textFrameCount.text = 'simulation time: ' + str(self.simulationTime) + '   frame: ' + str(self.frameCount) + '/' + str(self.frameLimit)
            
            # draw ui
            
            self.draw(self.window)

            pygame.time.wait(Config.frame_time_millis)

        pygame.quit()


    def draw(self, window):
        self.textFrameCount.draw(window)
        pygame.display.update()


###########################

if __name__ == "__main__":
    main()

###########################