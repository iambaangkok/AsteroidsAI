from copy import deepcopy
import math
import numpy as np
import pygame
from pygame import Vector2
from pygame import Rect
from AsteriodManager import AsteriodManager

import Colors
import Config
from NeuralNetwork import NeuralNetwork
from TextObject import TextObject
from Utility import flip, normalize, sigmoid
from AsteriodsGame import AsteriodsGame


def main():
    astAI = AsteriodAI()
    astAI.run()

class AsteriodAI:
    def __init__(self):
        np.random.seed(1)

        self.simulatorState = 1

        ##### Genetic Algorithm

        self.agentPerGeneration = Config.genetic_agentpergeneration

        self.games = []
        self.astManager = AsteriodManager(self.games)
        for i in range(0, self.agentPerGeneration):
            self.games.append(AsteriodsGame(self))
            if i != 0:
                (self.games[i]).astManager.asteriods = deepcopy((self.games[0]).astManager.asteriods)

        

        self.generation = 1
        self.bestScore = 0

        self.simulationTime = 20 # x seconds
        self.frameLimit = self.simulationTime * Config.frame_rate
        self.frameCount = 0

        ##### Neural Network

        self.neuralNetworks = []
        for i in range(0, self.agentPerGeneration):
            self.neuralNetworks.append(NeuralNetwork(self.games[i]))
        
        self.bestNeuralNetwork = self.neuralNetworks[0]
        self.bestGame = self.bestNeuralNetwork.game

        # user interface
        self.infopanelRect = Rect(Config.infopanel_left, Config.infopanel_top, Config.infopanel_width, Config.infopanel_height)

        self.textGeneration = TextObject('generation: ' + str(self.generation),
                                    Config.infopanel_left + 10, Config.infopanel_top + 10, 
                                    "UbuntuMono", 16, Colors.WHITE, "left", "top"
                                )
        
        self.textBestScore = TextObject('best score: ' + str(self.bestScore),
                                    Config.infopanel_left + 10, Config.infopanel_top + 26, 
                                    "UbuntuMono", 16, Colors.WHITE, "left", "top"
                                )

        self.textFrameCount = TextObject('simulation time: ' + str(self.simulationTime) + '   frame: ' + str(self.frameCount) + '/' + str(self.frameLimit),
                                    Config.game_left + 10, Config.game_top + 10, 
                                    "UbuntuMono", 16, Colors.WHITE, "left", "top"
                                )



    def run(self):
        while(self.simulatorState != 0):
            keys=pygame.key.get_pressed()
            
            if keys[pygame.K_r] and keys[pygame.K_LCTRL]: # reset
                for i in range(0, self.agentPerGeneration):
                    game = self.games[i]
                    game.setup()
                self.frameCount = 0

            if keys[pygame.K_q] and keys[pygame.K_LCTRL]: # quit
                self.simulatorState = 0

            ##### GOING TO NEXT GENERATION CHECK
            self.frameCount += 1*Config.speedmultiplier
            isAlive = 0
            for i in range(0, self.agentPerGeneration):
                if self.games[i].player.isAlive:
                    isAlive += 1

            if(self.frameCount >= self.frameLimit or isAlive <= 0):
                for i in range(0, self.agentPerGeneration):
                    self.checkBestScore(i)     
                    game = self.games[i]
                    game.setup()
                self.frameCount = 0
                self.generation += 1

            ##### UPDATE

            for i in range(0, self.agentPerGeneration):
                game = self.games[i]
                neural = self.neuralNetworks[i]                

                # neural network
                neural.computeOutput()
                inputs = []
                for i in range(0, len(neural.outputLayer[0])):
                    inputs.append(neural.outputLayer[0][i] > neural.activationThreshold)
                
                # game step
                _dt = game.clock.tick(Config.frame_rate)*Config.speedmultiplier
                game.update(_dt, inputs)

            ##### DRAW

            # draw black bg
            self.bestGame.window.fill(Colors.BLACK)

            for i in range(0, self.agentPerGeneration): # game draw
                game = self.games[i]
                updateDisplay = False
                drawRay = False
                drawPlayer = True
                drawAsteriods = True
                drawBullets = False
                drawCoverUp = False
                drawWindowBorder = False
                drawScore = False
                drawBg = False
                game.player.playerWidth = 1

                if game == self.bestGame: # best game
                    drawRay = True
                    drawAsteriods = True
                    drawBullets = True
                    drawScore = True
                    game.player.playerWidth = 0

                if i == self.agentPerGeneration-1: # last game
                    drawCoverUp = True
                    drawWindowBorder = True

                game.draw(updateDisplay,drawRay,drawPlayer,drawAsteriods
                ,drawBullets,drawCoverUp,drawWindowBorder,drawScore,drawBg )

            # user interface
            self.updateUI()
            self.drawUI(self.bestGame.window)

        pygame.quit()

    def checkBestScore(self, i):
        if math.floor(self.games[i].scoreManager.score) > self.bestScore:
            self.bestScore = math.floor(self.games[i].scoreManager.score)
            self.bestNeuralNetwork = self.neuralNetworks[i]
            self.bestGame = self.games[i]

    def updateUI(self):
        self.textBestScore.text = 'best score: ' + str(self.bestScore)
        self.textGeneration.text = 'generation: ' + str(self.generation)
        self.textFrameCount.text = 'simulation time: ' + str(math.floor(self.simulationTime/Config.speedmultiplier)) + '   frame: ' + str(self.frameCount) + '/' + str(self.frameLimit)
        

    def drawUI(self, window):
        
        neural = self.bestNeuralNetwork

        # nodes & weights
        for i in range(0, len(neural.inputLayer[0])):
            # node
            coordL = deepcopy(neural.nodeCoords[neural.inputInd][i])
            color = neural.nodeColor0.lerp(neural.nodeColor1, neural.inputLayer[0][i])
            width = 1
            if neural.inputLayer[0][i] >= neural.activationThreshold:
                width = 0
            pygame.draw.circle(window, color, coordL, neural.nodeRadius, width)

            # weight
            coordL.x += neural.nodeRadius

            for j in range(0, len(neural.outputLayer[0])):
                # node
                coordR = deepcopy(neural.nodeCoords[neural.outputInd][j])
                color = neural.nodeColor0.lerp(neural.nodeColor1, neural.outputLayer[0][j])
                width = 1
                if neural.outputLayer[0][j] >= neural.activationThreshold:
                    width = 0
                pygame.draw.circle(window, color, coordR, neural.nodeRadius, width)

                # weight
                coordR.x -= neural.nodeRadius
                weight = neural.weights[i][j]
                color = neural.weightColor0.lerp(neural.weightColor1, weight)
                if neural.inputLayer[0][i] >= neural.activationThreshold and neural.outputLayer[0][j] >= neural.activationThreshold:
                    color = neural.weightColor0.lerp(neural.nodeColor1, weight)
                pygame.draw.line(window, color, coordL, coordR)

                

        # info panel

        self.textBestScore.draw(window)
        self.textGeneration.draw(window)
        self.textFrameCount.draw(window)

        pygame.draw.rect(self.bestGame.window, Colors.WHITE_52, self.infopanelRect, 1)

        pygame.display.update()


###########################

if __name__ == "__main__":
    main()

###########################