from copy import deepcopy
import numpy as np
import pygame
from pygame import Vector2
from pygame import Rect

import Colors
import Config
from TextObject import TextObject
from Utility import flip, normalize, sigmoid
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

        ##### Genetic Algorithm

        self.generation = 1

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
        ], dtype="object")

        np.random.seed(1)

        self.weights = 1 * np.random.random((len(self.nodes[self.inputInd][0]), len(self.nodes[self.outputInd])))

        print('Random starting weights: ')
        print(self.weights)

        self.computeOutput()
        print('Inputs: ')
        print(self.inputLayer)
        print('Outputs: ')
        print(self.outputLayer)

        ##### User interface

        # nodes
        self.nodepanelX = Config.infopanel_left+10
        self.nodePanelRight = Config.infopanel_right-10
        self.nodepanelY = 200
        self.nodeRadius = 8
        self.layerGap = 100
        self.nodeGap = 6
        self.nodeColor0 = Colors.WHITE
        self.nodeColor1 = Colors.GREEN
        self.weightColor0 = Colors.WHITE_85
        self.weightColor1 = Colors.BLUE

        self.activationThreshold = 0.8

        self.nodeCoords = [[], []]

        for i in range(len(self.nodes[self.inputInd][0])):
            self.nodeCoords[self.inputInd].append(Vector2(self.nodepanelX + self.nodeRadius*(1), self.nodepanelY + i*(self.nodeRadius*2 + self.nodeGap)))
        
        for i in range(len(self.nodes[self.outputInd])):
            self.nodeCoords[self.outputInd].append(Vector2(self.nodePanelRight - self.nodeRadius*(1), 120+ self.nodepanelY + i*(self.nodeRadius*2 + self.nodeGap)))
        
        # user interface
        self.infopanelRect = Rect(Config.infopanel_left, Config.infopanel_top, Config.infopanel_width, Config.infopanel_height)

        self.textGeneration = TextObject('generation: ' + str(self.generation),
                                    Config.infopanel_left + 10, Config.infopanel_top + 10, 
                                    "UbuntuMono", 16, Colors.WHITE, "left", "top"
                                )        

        self.textFrameCount = TextObject('simulation time: ' + str(self.simulationTime) + '   frame: ' + str(self.frameCount) + '/' + str(self.frameLimit),
                                    Config.game_left + 10, Config.game_top + 10, 
                                    "UbuntuMono", 16, Colors.WHITE, "left", "top"
                                )        

    def computeOutput(self):
        # get input
        self.inputLayer = [[]]
        for i in range(0, len(self.raycaster.distance)):
            self.inputLayer[0].append(flip(normalize(self.raycaster.distance[i], 0, self.game.raycaster.lengthLimit), 0 , 1))
        self.inputLayer[0].append(normalize(self.player.rotation, 0, 360))

        self.inputLayer = np.array(self.inputLayer)

        self.outputLayer = np.array( sigmoid(np.dot(self.inputLayer, self.weights)) )

    def run(self):
        while(self.game.gameState != 0):

            keys=pygame.key.get_pressed()
            if keys[pygame.K_r] and keys[pygame.K_LCTRL]: # reset
                self.game.setup()
                self.player = self.game.player
                self.raycaster = self.game.raycaster
                self.frameCount = 0
            
            # genetic algorithm
            self.frameCount += 1
            if(self.frameCount >= self.frameLimit or not self.player.isAlive):
                self.game.setup()
                self.player = self.game.player
                self.raycaster = self.game.raycaster
                self.frameCount = 0
                self.generation += 1

            # neural network
            self.computeOutput()
            inputs = []
            for i in range(0, len(self.outputLayer[0])):
                inputs.append(self.outputLayer[0][i] > self.activationThreshold)
            
            # game step
            _dt = Config.frame_time_millis
            self.game.update(_dt, inputs)
            self.game.draw(False)

            # user interface
            self.updateUI()
            self.drawUI(self.window)

            pygame.time.wait(Config.frame_time_millis)

        pygame.quit()

    def updateUI(self):
        self.textGeneration.text = 'generation: ' + str(self.generation)
        self.textFrameCount.text = 'simulation time: ' + str(self.simulationTime) + '   frame: ' + str(self.frameCount) + '/' + str(self.frameLimit)
        

    def drawUI(self, window):

        # nodes & weights
        for i in range(0, len(self.inputLayer[0])):
            # node
            coordL = deepcopy(self.nodeCoords[self.inputInd][i])
            color = self.nodeColor0.lerp(self.nodeColor1, self.inputLayer[0][i])
            width = 1
            if self.inputLayer[0][i] >= self.activationThreshold:
                width = 0
            pygame.draw.circle(window, color, coordL, self.nodeRadius, width)

            # weight
            coordL.x += self.nodeRadius

            for j in range(0, len(self.outputLayer[0])):
                # node
                coordR = deepcopy(self.nodeCoords[self.outputInd][j])
                color = self.nodeColor0.lerp(self.nodeColor1, self.outputLayer[0][j])
                width = 1
                if self.outputLayer[0][j] >= self.activationThreshold:
                    width = 0
                pygame.draw.circle(window, color, coordR, self.nodeRadius, width)

                # weight
                
                coordR.x -= self.nodeRadius
                weight = self.weights[i][j]
                color = self.weightColor0.lerp(self.weightColor1, weight)
                if self.inputLayer[0][i] >= self.activationThreshold and self.outputLayer[0][j] >= self.activationThreshold:
                    color = self.weightColor0.lerp(self.nodeColor1, weight)
                pygame.draw.line(window, color, coordL, coordR)

                

        # info panel

        self.textGeneration.draw(window)
        self.textFrameCount.draw(window)

        pygame.draw.rect(self.window, Colors.WHITE_52, self.infopanelRect, 1)

        pygame.display.update()


###########################

if __name__ == "__main__":
    main()

###########################