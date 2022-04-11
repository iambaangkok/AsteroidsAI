import numpy as np
import pygame
from pygame import Vector2
from pygame import Rect

from AsteriodsGame import AsteriodsGame


def main():
    astAI = AsteriodAI()
    astAI.run()

class AsteriodAI:
    def __init__(self):
        self.game = AsteriodsGame()
        self.player = self.game.player
        self.raycaster = self.game.raycaster
        


        ##### Neural Network

        self.nLayers = 2 # only input and output
        
        self.inputInd = 0
        self.outputInd = self.nLayers-1
        
        inputLayer = np.array([[ (self.raycaster.distance[i] for i in range(0, len(self.raycaster.distance))), 
                                self.player.rotation ]])
        outputLayer = np.array([[ 0, 0, 0, 0 ]]).T

        self.nodes = np.array([
            inputLayer,
            outputLayer
        ])

        np.random.seed(1)

        self.synaptic_weights = 2 * np.random.random((len(self.nodes[self.outputInd]), len(self.nodes[self.outputInd])))

        print('Random starting weights: ')
        print(self.synaptic_weights)

    
    def run(self):
        self.game.run()


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


###########################

if __name__ == "__main__":
    main()

###########################