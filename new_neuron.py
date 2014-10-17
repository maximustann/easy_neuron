#!/bin/env python
import random
import math

class Neuron(object):
    def __init__(self):
        self.learning_rate = 0.2
        self.beta = 0
        self.output_value = 0
    def set_learning_rate(self, learning_rate):
        self.learning_rate = learning_rate
    def sigmoid(self, value_list):
        output_value = 1.0 / (1.0 + math.exp(-sum(value_list)))
        return output_value
    def cal_beta(self, weight, higher_output, higher_beta):
        self.beta += weight * (1 - higher_output) * higher_beta
    def return_beta(self):
        temp_beta = self.beta
        self.beta = 0
        return temp_beta
    def cal_delta_weight(self, higher_output, higher_beta):
        delta_weight = self.learning_rate * self.output_value * (1 - higher_output) * higher_beta
        return delta_weight

class Input_Nodes(Neuron):
    def __init__(self):
        super(Input_Nodes, self).__init__()
        self.input_value = 0
    def input(self, input_num):
        self.input_value = input_num
    def return_input(self):
        return self.input_value

class Output_Nodes(Neuron):
    def __init__(self):
        super(Output_Nodes, self).__init__()
        self.output_value = 0
        self.desired = 0
        self.beta = 0
    def init_desired_value(self, desired):
        self.desired = desired
    def cal_beta(self):
        self.beta = self.desired - self.output_value
    def return_beta(self):
        return self.beta
    def return_output(self):
        return output_value


class Bias(object):
    def __init__(self):
        self.output_value = 1
        self.learning_rate = None
    def set_learning_rate(self, learning_rate):
        self.learning_rate = learning_rate
    def return_output(self):
        return self.output_value
    def cal_delta_weight(self, higher_output, higher_beta):
        return self.learning_rate * (1 - higher_output) * higher_beta


class Network(object):
    def __init__(self):
        self.input_node_list = []
        self.output_node_list = []
        self.layer_num = 0
        self.hidden_layers = []
    def initilize_input_nodes(self, input_num):
        self.input_node_list = [[Input_Nodes(), random.uniform(), Bias()] for _ in range(input_num)]
    def initilize_hidden_layer(self, layer_num):
        self.hidden_layers = [[] for i in range(layer_num)]
    def initilize_hidden_nodes(self, layer, nodes_num):
        self.hidden_layers[layer - 1] = [[Neuron(), random.uniform()] for _ in range(nodes_num))]
    def initilize_output_nodes(self, output_num):
        self.output_node_list = [[Output_Nodes(), Bias()] for _ in range(output_num)]
    def learning_pattern(self, input_1, input_2, output):
        pass
    def epoch(self, num):
        pass
    def test(input_1, input_2):
        pass

if __name__ == "__main__":
    net = Network()
    net.initilize_input_nodes(2)
    net.initilize_hidden_layer(2)
    net.initilize_hidden_nodes(1, 5)
    net.initilize_hidden_nodes(2, 5)
    net.initilize_output_nodes(1)
    net.learning_pattern(1,1,0)
    net.learning_pattern(0,0,0)
    net.learning_pattern(1,0,1)
    net.learning_pattern(0,1,1)
    net.epoch(500)
    net.test(1,1)
