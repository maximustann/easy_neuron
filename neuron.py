#!/bin/env python
import random
import math
class Neuron(object):
    def __init__(self):
        self.value = 0
        self.input_list = []
        self.output_node_dict = {}
        self.intput_node_dict = {}
        self.back_propogate_dict = {}
        self.delta_weight = 0
    def set_desired_value(self, output_node, value):
        self.back_propogate_dict[output_node] = value #output_node, consist of output and beta
    def set_learning_rate(self, rate):
        self.learning_rate = rate
    def init_input_node(self, input_node):
        self.input_node_dict[input_node] = None
    def input(self, input_node, value):
        self.input_node_dict[input_node] = value
        if not None in self.input_node_dict.values():
            output_value = self.sigmoid(self.input_node_dict.values())
        self.output(output_value)
    def set_none(self):
        for node in self.input_node_dict.keys():
            self.input_node_dict[node] = None
    def output(self):
        for output_node, weight in self.output_node_dict.items():
            output_node.input(self.value * weight)
    def sigmoid(self, value_list):
        for value in value_list:
            summ += value
        return 1.0 / (1.0 + math.exp(-summ))
    def setup(self, output_node_list):
        for node in output_not_list:
            self.output_node_dict[node] = random.uniform(-1, 1)
    def back_propogation(self, ):



class Input_neuron(Neuron):
    def __init__(self):
        super(Input_neuron, self).__init__(weight)
        self.value = None
    def input(self, value):
        pass

class Output_neuron(Neuron):
    def __init__(self):
        super(Output_neuron, self).__init__(weight)
        self.value = None
    def set_desired_value(self, value):


def construct_network(number_input, number_hidden, number_output):
    input_nodes = [Input_neuron() for i in range(number_input)] #generate input nodes
    hidden_neurons = [Neuron() for i in range(number_hidden)]   #generate hidden nodes
    out_neurons = [Output_neuron() for i in range(number_output)] #generate output nodes
    #it's a one layer network, don't expect too much
    for node in input_nodes:
        node.setup(hidden_neurons) #connect input nodes with hidden nodes
    for node in hidden_neurons:     #connect hidden nodes with output nodes
        node.setup(output_neurons)


if __name__ == "__main__":
    construct_network(2, 1, 1)
