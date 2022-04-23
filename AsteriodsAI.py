from copy import deepcopy
import math
import random
import numpy as np
import pygame
from pygame import Vector2
from pygame import Rect
from AsteriodManager import AsteriodManager

import Colors
import Config
from NeuralNetwork import NeuralNetwork
from TextObject import TextObject
from Utility import clamp, flip, normalize, sigmoid
from AsteriodsGame import AsteriodsGame


def main():
    astAI = AsteriodAI()
    astAI.run()

class AsteriodAI:
    def __init__(self):
        pygame.init()
        np.random.seed(Config.randomseed)
        random.seed(Config.randomseed)

        self.simulatorState = 1

        ##### Genetic Algorithm
        self.generation = 1
        self.bestScore = 0
        self.bestScoreThisGeneration = 0

        self.simulationTime = Config.genetic_simulationtime # x seconds
        self.frameLimit = self.simulationTime * Config.frame_rate
        self.frameCount = 0

        self.agentPerGeneration = Config.genetic_agentpergeneration
        self.mutationRate = 0.1
        self.breedThreshold = 0.5 # if score >= bestScore * breedThreshold then breed

        self.maxPossibleScore = Config.score_per_second_surving*self.simulationTime

        self.games = []
        self.astManager = AsteriodManager(self.games)
        for i in range(0, self.agentPerGeneration):
            self.games.append(AsteriodsGame(self))
            self.games[i].id = i
        
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
        self.textAgentPerGeneration = TextObject('agents: ' + str(self.agentPerGeneration),
                                    Config.infopanel_left + 10, Config.infopanel_top + 10+16*TextObject.count, 
                                    "UbuntuMono", 16, Colors.WHITE, "left", "top"
                                )
        self.textAgentAlive = TextObject('agents alive: ' + str(self.agentPerGeneration),
                                    Config.infopanel_left + 10, Config.infopanel_top + 10+16*TextObject.count, 
                                    "UbuntuMono", 16, Colors.WHITE, "left", "top"
                                )
        self.textMutationRate = TextObject('mutation rate: ' + str(self.mutationRate),
                                    Config.infopanel_left + 10, Config.infopanel_top + 10+16*TextObject.count, 
                                    "UbuntuMono", 16, Colors.WHITE, "left", "top"
                                )
        self.textMaxPossibleScore = TextObject('max possible score: ' + str(self.maxPossibleScore),
                                    Config.infopanel_left + 10, Config.infopanel_top + 10+16*TextObject.count, 
                                    "UbuntuMono", 16, Colors.WHITE, "left", "top"       
                                ) 
        self.textBestScoreThisGeneration = TextObject('score this gen: ' + str(self.bestScoreThisGeneration) + '   fitness: ' + str(math.floor((self.bestScoreThisGeneration/self.maxPossibleScore)*100)/100.0),
                                    Config.infopanel_left + 10, Config.infopanel_top + 10+16*TextObject.count, 
                                    "UbuntuMono", 16, Colors.WHITE, "left", "top"       
                                ) 
        self.textBestScore = TextObject('best score: ' + str(self.bestScore) + '   max fitness: ' + str(math.floor((self.bestScore/self.maxPossibleScore)*100)/100.0),
                                    Config.infopanel_left + 10, Config.infopanel_top + 10+16*TextObject.count, 
                                    "UbuntuMono", 16, Colors.WHITE, "left", "top"
                                )
        self.textFrameCount = TextObject('simulation time: ' + str(self.simulationTime) + '   frame: ' + str(self.frameCount) + '/' + str(self.frameLimit) + '   score: ' + str(self.bestScoreThisGeneration),
                                    Config.game_left + 10, Config.game_top + 10, 
                                    "UbuntuMono", 16, Colors.WHITE, "left", "top"
                                )
        self.textSpeedMultiplier = TextObject('speed multiplier: ' + str(math.floor(Config.speedmultiplier)),
                                    Config.game_left + 10, Config.game_top + 10+16*1, 
                                    "UbuntuMono", 16, Colors.WHITE, "left", "top"
                                )
        
        self.games[0].clock.tick(Config.frame_rate)*Config.speedmultiplier

    def run(self):
        while(self.simulatorState != 0):
            keys=pygame.key.get_pressed()
            
            if keys[pygame.K_n] and keys[pygame.K_LCTRL]: # reset game and neural network
                self.resetGames()
                self.resetNeuralNetworks()

            if keys[pygame.K_r] and keys[pygame.K_LCTRL]: # reset game
                self.resetGames()

            if keys[pygame.K_q] and keys[pygame.K_LCTRL]: # quit
                self.simulatorState = 0

            ##### GOING TO NEXT GENERATION CHECK
            self.frameCount += 1*Config.speedmultiplier
            isAlive = 0
            for i in range(0, self.agentPerGeneration):
                if self.games[i].player.isAlive:
                    isAlive += 1
            self.textAgentAlive.text = 'agents alive: ' + str(isAlive)
            # print("ALIVE: ", isAlive)
            if(self.frameCount >= self.frameLimit or isAlive <= 0):
                for i in range(0, self.agentPerGeneration):
                    self.checkBestScore(self.games[i].id)
                self.resetGames()
                self.generation += 1
                self.bestScoreThisGeneration = 0
                self.breedNextGeneration()
                self.games[0].clock.tick(Config.frame_rate)*Config.speedmultiplier

            ##### UPDATE
           
            _dt = self.games[0].clock.tick(Config.frame_rate)*Config.speedmultiplier
            self.update(_dt)

            ##### DRAW

            self.draw(self.games[0].window)

        pygame.quit()

    def update(self, _dt):
        # game step
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

    def breedNextGeneration(self):
        bNeural = self.bestNeuralNetwork
        for n in range(0, len(self.neuralNetworks)):
            neural = self.neuralNetworks[n]
            for layer in range(0, len(neural.weights)):
                bWeights = bNeural.weights[layer]
                weights = neural.weights[layer]
                for i in range(0, len(weights)):
                    for j in range(0, len(weights[i])):
                        bW = bWeights[i][j]
                        w = weights[i][j]
                        avg = w
                        
                        # breed according to fitness
                        sign = np.sign(bW-w)
                        fitness = self.bestScoreThisGeneration/self.maxPossibleScore
                        difference = abs(bW-w)
                        adjustment = sign*difference*fitness

                        weights[i][j] = w + adjustment

                        # mutate
                        mutation = (random.random() * 2 - 1) * self.mutationRate
                        weights[i][j] = clamp(avg * (1+mutation), -1, 1)

        pass

    def draw(self, window):
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
        self.drawUI(window)

    def updateUI(self):
        self.textMaxPossibleScore.text = 'max possible score: ' + str(self.maxPossibleScore)
        self.textBestScoreThisGeneration.text = 'score this gen: ' + str(self.bestScoreThisGeneration) + '   fitness: ' + str(math.floor((self.bestScoreThisGeneration/self.maxPossibleScore)*100)/100.0)
        self.textBestScore.text = 'best score: ' + str(self.bestScore) + '   max fitness: ' + str(math.floor((self.bestScore/self.maxPossibleScore)*100)/100.0)
        self.textGeneration.text = 'generation: ' + str(self.generation)
        self.textFrameCount.text = 'simulation time: ' + str(math.floor(self.simulationTime)) + '   frame: ' + str(self.frameCount) + '/' + str(self.frameLimit) + '   score: ' + str(self.bestScoreThisGeneration)
        self.textSpeedMultiplier.text = 'speed multiplier: ' + str(math.floor(Config.speedmultiplier))

    def drawUI(self, window):
        
        neural = self.bestNeuralNetwork

        for layer in range(0, len(neural.nodes)-1):
            leftLayer = layer
            rightLayer = layer+1
            # print("LEFT ", leftLayer)
            # print(neural.nodes[leftLayer])
            # print("RIGHT ", rightLayer)
            # print(neural.nodes[rightLayer])

            # nodes & weights
            for i in range(0, len(neural.nodes[leftLayer][0])):
                # node
                coordL = neural.nodeCoords[leftLayer][i]
                color = neural.nodeColor0.lerp(neural.nodeColor1, neural.nodes[leftLayer][0][i])
                width = 1
                # print(neural.nodes)
                # print(neural.nodes[leftLayer][0][i], " ", neural.activationThreshold)
                if neural.nodes[leftLayer][0][i] >= neural.activationThreshold:
                    width = 0
                pygame.draw.circle(window, color, coordL, neural.nodeRadius, width)

                # weight
                
                for j in range(0, len(neural.nodes[rightLayer][0])):
                    # node
                    coordR = neural.nodeCoords[rightLayer][j]
                    color = neural.nodeColor0.lerp(neural.nodeColor1, neural.nodes[rightLayer][0][j])
                    width = 1
                    if neural.nodes[rightLayer][0][j] >= neural.activationThreshold:
                        width = 0
                    pygame.draw.circle(window, color, coordR, neural.nodeRadius, width)

                    # weight
                    weight = neural.weights[leftLayer][i][j]
                    color = neural.weightColor0
                    if weight >= 0:
                        color = neural.weightColor0.lerp(neural.weightColorPositive, weight)
                    else:
                        color = neural.weightColor0.lerp(neural.weightColorNegative, -weight)
                    if neural.nodes[leftLayer][0][i] >= neural.activationThreshold and neural.nodes[rightLayer][0][j] >= neural.activationThreshold:
                        color = neural.weightColor0.lerp(neural.nodeColor1, abs(weight))
                    pygame.draw.line(window, color, coordL + (neural.nodeRadius, 0), coordR + (-neural.nodeRadius, 0))

        # info panel
        self.textGeneration.draw(window)
        self.textAgentPerGeneration.draw(window)
        self.textAgentAlive.draw(window)
        self.textMutationRate.draw(window)
        self.textMaxPossibleScore.draw(window)
        self.textBestScoreThisGeneration.draw(window)
        self.textBestScore.draw(window)
        self.textFrameCount.draw(window)
        self.textSpeedMultiplier.draw(window)

        pygame.draw.rect(self.games[0].window, Colors.WHITE_52, self.infopanelRect, 1)

        pygame.display.update()

    def resetGames(self):
        if Config.random_fixedseedeverygeneration:
            np.random.seed(Config.randomseed)
            random.seed(Config.randomseed)
        self.astManager = AsteriodManager(self.games)
        for i in range(0, self.agentPerGeneration):
            game = self.games[i]
            game.setup()
        self.frameCount = 0
    
    def resetNeuralNetworks(self):
        self.neuralNetworks.clear()
        for i in range(0, self.agentPerGeneration):
            self.neuralNetworks.append(NeuralNetwork(self.games[i]))

    def checkBestScore(self, i):
        # print("CHECK: ", i , " ",math.floor(self.games[i].scoreManager.score))
        if math.floor(self.games[i].scoreManager.score) > self.bestScore:
            self.bestScore = math.floor(self.games[i].scoreManager.score)
        if math.floor(self.games[i].scoreManager.score) > self.bestScoreThisGeneration:
            self.bestScoreThisGeneration = math.floor(self.games[i].scoreManager.score)
            self.bestNeuralNetwork = self.neuralNetworks[i]
            self.bestGameId = i

###########################

if __name__ == "__main__":
    main()

###########################