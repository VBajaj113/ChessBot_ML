'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
'''
from random import random
import math
import time

#IDEA: WE TAKE IN VARIOUS INPUTS FROM THE BOARD, PASS IT THROUGH FUNCTIONS and PRODUCE AN OUTPUT WHICH WILL BE THE EVALUATION FOR THAT POSITION


#FIRST DO A SMALLER PROJECT


#MAKING A SIMPLE NEURAL NETWORK,


#WE ASSUME 3 Inputs, 1 hidden layer of 3 neurons and output is a single number
#EACH neuron in a layer has a unique set of weights and the same set of inputs


ACTUAL_OUT = 0.8
eps = 0.001
step = 0.001


def funct(x):
    return 1/(1 + math.exp(x))


def grad(x):
    return funct(x) * funct(x) - funct(x)

def dotProduct(input_list, weight_list):
    ans = 0
    for x in range(len(input_list)):
        ans = ans + (input_list[x] * weight_list[x])

    return ans



class Neuron:
    def __init__(self, input_list, weight_list, bias = 0):
        self.input_list = input_list
        self.weight_list = weight_list
        self.bias = bias


    def output(self):
        return funct(dotProduct(self.input_list, self.weight_list) + self.bias)


    def adjust_weights(self):
    #ASSUMING A 2 element input, so we have a 2 element weight list, giving 1 output
        w1 = self.weight_list[0]
        w2 = self.weight_list[1]
        b = self.bias
        self.weight_list[0] = w1 + step*grad(self.output())*self.input_list[0]
        self.weight_list[1] = w2 + step*grad(self.output())*self.input_list[1]
        self.bias = b - step
    


class NeuronLayer:
    def __init__(self, Neuron_List):
        #Neuron_List is a list of Neuron objects

        self.Neuron_List = Neuron_List

    def output_list(self): #This is the output of this layer which will be feeded to the next layer
        out = []
        for neuron in self.Neuron_List:
            out.append(neuron.output())

        return out



start = time.time()
#ASSUMING THAT WE ARE ADJUSTING THE WEIGHTS FOR A SINGLE NEURON,
w1 = 0.5
w2 = 0.5

n1 = Neuron([0.7, 0.3], [w1, w2], 0.5)

while abs(n1.output() - ACTUAL_OUT) > eps:
    n1.adjust_weights()
    

end = time.time()

print(n1.output())
print(end - start)
    




        
        
