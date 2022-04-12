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
        pygame.init()
        np.random.seed(1)

        self.simulatorState = 1

        ##### Genetic Algorithm

        self.agentPerGeneration = Config.genetic_agentpergeneration

        self.games = []
        self.astManager = AsteriodManager(self.games)
        for i in range(0, self.agentPerGeneration):
            self.games.append(AsteriodsGame(self))
            self.games[i].id = i

        self.generation = 1
        self.bestScore = 0
        self.bestScoreThisGeneration = 0

        self.simulationTime = 60 # x seconds
        self.frameLimit = self.simulationTime * Config.frame_rate
        self.frameCount = 0

        ##### Neural Network

        self.neuralNetworks = []
        for i in range(0, self.agentPerGeneration):
            self.neuralNetworks.append(NeuralNetwork(self.games[i]))
        
        self.bestNeuralNetwork = self.neuralNetworks[0]
        self.bestGameId = 0

        # user interface
        self.infopanelRect = Rect(Config.infopanel_left, Config.infopanel_top, Config.infopanel_width, Config.infopanel_height)

        self.textGeneration = TextObject('generation: ' + str(self.generation),
                                    Config.infopanel_left + 10, Config.infopanel_top + 10, 
                                    "UbuntuMono", 16, Colors.WHITE, "left", "top"
                                )
        self.textAgentPerGeneration = TextObject('agent per generation: ' + str(self.agentPerGeneration),
                                    Config.infopanel_left + 10, Config.infopanel_top + 10+16*1, 
                                    "UbuntuMono", 16, Colors.WHITE, "left", "top"
                                )
        self.textBestScoreThisGeneration = TextObject('best score this generation: ' + str(self.bestScoreThisGeneration),
                                    Config.infopanel_left + 10, Config.infopanel_top + 10+16*2, 
                                    "UbuntuMono", 16, Colors.WHITE, "left", "top"       
                                ) 
        self.textBestScore = TextObject('best score: ' + str(self.bestScore),
                                    Config.infopanel_left + 10, Config.infopanel_top + 10+16*3, 
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
                self.astManager = AsteriodManager(self.games)
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
            # print("ALIVE: ", isAlive)
            if(self.frameCount >= self.frameLimit or isAlive <= 0):
                self.astManager = AsteriodManager(self.games)
                for i in range(0, self.agentPerGeneration):
                    self.checkBestScore(self.games[i].id)
                    game = self.games[i]
                    game.setup()
                self.frameCount = 0
                self.generation += 1
                self.bestScoreThisGeneration = 0

            ##### UPDATE
            # game step
            _dt = self.games[0].clock.tick(Config.frame_rate)*Config.speedmultiplier
            self.astManager.update(_dt)

            for i in range(0, self.agentPerGeneration):
                game = self.games[i]
                neural = self.neuralNetworks[i]                

                # neural network
                neural.computeOutput()
                inputs = []
                for i in range(0, len(neural.outputLayer[0])):
                    inputs.append(neural.outputLayer[0][i] > neural.activationThreshold)

                game.update(_dt, inputs)

                self.checkBestScore(game.id)

            ##### DRAW

            # draw black bg

            for i in range(0, self.agentPerGeneration): # game draw
                game = self.games[i]
                updateDisplay = False
                drawRay = False
                drawPlayer = True
                drawAsteriods = False
                drawBullets = False
                drawCoverUp = False
                drawWindowBorder = False
                drawScore = False
                drawBg = False
                game.player.playerWidth = 1

                if game.id == self.bestGameId: # best game
                    drawRay = True
                    drawAsteriods = True
                    drawBullets = True
                    drawScore = True
                    game.player.playerWidth = 0

                if i == 0: # first game
                    drawBg = True

                if i == self.agentPerGeneration-1: # last game
                    drawCoverUp = True
                    drawWindowBorder = True
                
                game.draw(updateDisplay,drawRay,drawPlayer,drawAsteriods
                ,drawBullets,drawCoverUp,drawWindowBorder,drawScore,drawBg )

            
            # user interface
            self.updateUI()
            self.drawUI(self.games[0].window)

            #pygame.time.wait(math.floor(Config.frame_time_millis/Config.speedmultiplier))

        pygame.quit()

    def checkBestScore(self, i):
        # print("CHECK: ", i , " ",math.floor(self.games[i].scoreManager.score))
        if math.floor(self.games[i].scoreManager.score) > self.bestScore:
            self.bestScore = math.floor(self.games[i].scoreManager.score)
        if math.floor(self.games[i].scoreManager.score) > self.bestScoreThisGeneration:
            self.bestScoreThisGeneration = math.floor(self.games[i].scoreManager.score)
            self.bestNeuralNetwork = self.neuralNetworks[i]
            self.bestGameId = i

    def updateUI(self):
        self.textBestScoreThisGeneration.text = 'best score this generation: ' + str(self.bestScoreThisGeneration)
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
                color = neural.weightColor0
                if weight >= 0:
                    color = neural.weightColor0.lerp(neural.weightColorPositive, weight)
                else:
                    color = neural.weightColor0.lerp(neural.weightColorNegative, -weight)
                if neural.inputLayer[0][i] >= neural.activationThreshold and neural.outputLayer[0][j] >= neural.activationThreshold:
                    color = neural.weightColor0.lerp(neural.nodeColor1, abs(weight))
                pygame.draw.line(window, color, coordL, coordR)

                

        # info panel
        self.textGeneration.draw(window)
        self.textAgentPerGeneration.draw(window)
        self.textBestScoreThisGeneration.draw(window)
        self.textBestScore.draw(window)
        self.textFrameCount.draw(window)

        pygame.draw.rect(self.games[0].window, Colors.WHITE_52, self.infopanelRect, 1)

        pygame.display.update()


###########################

if __name__ == "__main__":
    main()

###########################