import numpy as np
import pygame
from pygame import Vector2

import Config
import Colors
from Utility import flip, normalize, sigmoid

class NeuralNetwork:
    
    def __init__(self, game):
        self.game = game

        self.nLayers = 4
        
        self.inputInd = 0
        self.outputInd = self.nLayers-1
        
        self.inputLayer = [[]]
        for i in range(0, len(self.game.raycaster.distance)):
            self.inputLayer[0].append(self.game.raycaster.distance[i] )
        # self.inputLayer[0].append(self.game.player.rotation)
        self.inputLayer = np.array(self.inputLayer)

        self.hiddenLayer1 = [[]]
        for i in range(0, 10):
            self.hiddenLayer1[0].append(0)
        self.hiddenLayer1 = np.array(self.hiddenLayer1)

        self.hiddenLayer2 = [[]]
        for i in range(0, 10):
            self.hiddenLayer2[0].append(0)
        self.hiddenLayer2 = np.array(self.hiddenLayer1)
        
        self.outputLayer = np.array([[ 0, 0, 0, 0 ]]).T

        self.nodes = [
            self.inputLayer,
            self.hiddenLayer1,
            self.hiddenLayer2,
            self.outputLayer
        ]
        
        self.weights = []
        self.weights.append(2 * np.random.random((len(self.nodes[self.inputInd][0]), len(self.nodes[1][0]))) -1)
        self.weights.append(2 * np.random.random((len(self.nodes[1][0]), len(self.nodes[2][0]))) -1)
        self.weights.append(2 * np.random.random((len(self.nodes[1][0]), len(self.nodes[self.outputInd]))) -1)

        # print(self.game.id, ' Random starting weights: ')
        # print(self.weights)

        # self.computeOutput()
        # print('Inputs: ')
        # print(self.inputLayer)
        # print('Outputs: ')
        # print(self.outputLayer)

        ##### User interface

        # nodes
        self.nodepanelX = Config.infopanel_left+10
        self.nodePanelRight = Config.infopanel_right-10
        self.nodepanelY = 280
        self.nodeRadius = 8
        self.layerGap = 100
        self.nodeGap = 6
        self.nodeColor0 = Colors.WHITE
        self.nodeColor1 = Colors.GREEN
        self.weightColor0 = Colors.WHITE_85
        self.weightColorPositive = Colors.BLUE
        self.weightColorNegative = Colors.RED

        self.activationThreshold = 0.8

        self.nodeCoords = [[], [], [], []]

        for i in range(len(self.nodes[self.inputInd][0])):
            self.nodeCoords[self.inputInd].append(Vector2(self.nodepanelX + self.nodeRadius*(1),
                                                        self.nodepanelY + i*(self.nodeRadius*2 + self.nodeGap)))
        
        for i in range(len(self.nodes[1][0])):
            self.nodeCoords[1].append(Vector2(self.nodepanelX + self.nodeRadius*(1) + self.layerGap*1,
                                                        60+ self.nodepanelY + i*(self.nodeRadius*2 + self.nodeGap)))
        for i in range(len(self.nodes[2][0])):
            self.nodeCoords[2].append(Vector2(self.nodepanelX + self.nodeRadius*(1) + self.layerGap*2,
                                                        60+ self.nodepanelY + i*(self.nodeRadius*2 + self.nodeGap)))

        for i in range(len(self.nodes[self.outputInd])):
            self.nodeCoords[self.outputInd].append(Vector2(self.nodePanelRight - self.nodeRadius*(1),
                                                        95+ self.nodepanelY + i*(self.nodeRadius*2 + self.nodeGap)))

    def computeOutput(self):
        # get input
        self.inputLayer = [[]]
        for i in range(0, len(self.game.raycaster.distance)):
            self.inputLayer[0].append(flip(normalize(self.game.raycaster.distance[i], 0, self.game.raycaster.lengthLimit), 0 , 1))
        # self.inputLayer[0].append(normalize(self.game.player.rotation, 0, 360))
        self.inputLayer = np.array(self.inputLayer)

        self.hiddenLayer1 = np.array( sigmoid(np.dot(self.inputLayer, self.weights[0])) )

        self.hiddenLayer2 = np.array( sigmoid(np.dot(self.hiddenLayer1, self.weights[1])) )

        self.outputLayer = np.array( sigmoid(np.dot(self.hiddenLayer2, self.weights[2])) )

        self.nodes = [
            self.inputLayer,
            self.hiddenLayer1,
            self.hiddenLayer2,
            self.outputLayer
        ]
        # print(self.inputLayer.shape, " ", self.hiddenLayer1.shape, " " , self.outputLayer.shape)
        # print(self.weights[0].shape, " ", self.weights[1].shape)