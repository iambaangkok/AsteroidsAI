import numpy as np
import pygame
from pygame import Vector2

import Config
import Colors
from Utility import flip, normalize, sigmoid

class NeuralNetwork:
    
    def __init__(self, game):
        self.game = game
        self.player = self.game.player
        self.raycaster = self.game.raycaster

        self.window = self.game.window

        self.nLayers = 2 # only input and output
        
        self.inputInd = 0
        self.outputInd = self.nLayers-1
        
        self.inputLayer = [[]]
        for i in range(0, len(self.raycaster.distance)):
            self.inputLayer[0].append(self.raycaster.distance[i] )
        # self.inputLayer[0].append(self.player.rotation)
        self.inputLayer = np.array(self.inputLayer)
        
        self.outputLayer = np.array([[ 0, 0, 0, 0 ]]).T

        self.nodes = np.array([
            self.inputLayer,
            self.outputLayer
        ], dtype="object")

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

    def computeOutput(self):
        # get input
        self.inputLayer = [[]]
        for i in range(0, len(self.raycaster.distance)):
            self.inputLayer[0].append(flip(normalize(self.raycaster.distance[i], 0, self.game.raycaster.lengthLimit), 0 , 1))
        # self.inputLayer[0].append(normalize(self.player.rotation, 0, 360))

        self.inputLayer = np.array(self.inputLayer)

        self.outputLayer = np.array( sigmoid(np.dot(self.inputLayer, self.weights)) )