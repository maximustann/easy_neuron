#!/bin/env python
import random
import math
class Neuron(object):
    def __init__(self):
        self.learning_rate = 0
        self.output_value = 0
        self.input_list = []
        self.output_node_dict = {}
        self.input_node_dict = {}
        self.back_propogate_dict = {}
        self.beta = 0


    def init_back_propogate_dict(self, output_node):
        self.back_propogate_dict[output_node] = None

    def set_desired_value(self, output_node, value):
        self.back_propogate_dict[output_node] = value #output_node, consist of output and beta


    def set_learning_rate(self, rate):
        self.learning_rate = rate


    def setup_input(self, input_node_list):
        for node in input_node_list:
            self.input_node_dict[node] = None


    def input(self, input_node, value):
        self.input_node_dict[input_node] = value
        if not None in self.input_node_dict.values():
            output_value = self.sigmoid(self.input_node_dict.values())
            self.output(output_value)


    def set_none(self):
        for node in self.input_node_dict.keys():
            self.input_node_dict[node] = None


    def output(self, output_value):
        for output_node, weight in self.output_node_dict.items():
            output_node.input(output_value * weight)


    def sigmoid(self, value_list):
        for value in value_list:
            summ += value
        self.output_value = 1.0 / (1.0 + math.exp(-summ))
        return self.output_value

    def setup_output(self, output_node_list):
        for node in output_node_list:
            self.output_node_dict[node] = random.uniform(-1, 1)
            self.init_back_propogate_dict(node)

    def adjust_weight(self, output_node, delta_weight):
        self.output_node_dict[output_node] += delta_weight


    def calculate_beta(self, output_node, higher_output, higher_beta):
        beta = self.output_node_dict[output_node] * higher_output * (1 - higher_output) * higher_beta
        
    def delta_rule(self, higher_output, higher_beta):
        delta_weight = self.learning_rate * self.output_value * higher_output * (1 - higher_output) * higher_beta
        return delta_weight


    def back_propogation(self):
        for input_node in self.intput_node_dict.keys():
            input_node.receive_feedback(self, self.output_value, self.beta)
        self.output_value = None

    def receive_feedback(self, output_node, higher_output, higher_beta):
        self.back_propogate_dict[output_node] = list(higher_output, higher_beta)
        if not None in self.back_propogate_dict.values():
            for output_node, context in self.back_propogate_dict.items():
                higher_output = context[0]
                higher_beta = context[1]
                self.beta += self.calculate_beta(output_node, self.output_value, higher_beta)
                self.init_back_propogate_dict(output_node)
                delta_weight = self.delta_rule(higher_output, higher_beta)
                self.adjust_weight(output_node, delta_weight)
        self.back_propogation()

class Input_neuron(Neuron):
    def __init__(self):
        super(Input_neuron, self).__init__()
        self.value = None

    def input(self, value):
        self.output(value)

    def output(self, value):
        for output_node, weight in self.output_node_dict.items():
            output_node.input(value * weight)

class Output_neuron(Neuron):
    def __init__(self):
        super(Output_neuron, self).__init__()
        self.desired_value = None

    def input(self, input_node, value):
        self.input_node_dict[input_node] = value
        if not None in self.input_node_dict.values():
            self.output = self.sigmoid(self.input_node_dict.values())

    def calculate_beta_weight(self):
        self.beta = self.desired_value - self.output

    def setup_desired_value(self, value):
        self.desired_value = value

    def back_propogation(self):
        self.calculate_beta_weight()
        for input_node in self.back_propogate_dict.keys():
            input_node.receive_feedback(self, self.output, self.beta)






def construct_network(number_input, number_hidden, number_output, learning_rate):
    input_neurons = [Input_neuron() for i in range(number_input)] #generate input nodes
    hidden_neurons = [Neuron() for i in range(number_hidden)]   #generate hidden nodes
    output_neurons = [Output_neuron() for i in range(number_output)] #generate output nodes
    #it's a one layer network, don't expect too much
    for node in input_neurons:
        node.setup_output(hidden_neurons)               #build output connection between input nodes and hidden nodes
        node.set_learning_rate(learning_rate)           #set input nodes' learning rate
    for node in hidden_neurons:
        node.setup_output(output_neurons)               #build output connection between hidden nodes and output nodes
        node.setup_input(input_neurons)                 #build input connection between input nodes and hidden nodes
        node.set_learning_rate(learning_rate)           #set hidden nodes' learning rate
    for node in output_neurons:
        node.setup_input(hidden_neurons)                #build input connection between hidden nodes and output nodes
        node.set_learning_rate(learning_rate)           #set output nodes' learning rate
    return input_neurons, hidden_neurons, output_neurons
def back_propogate(output_neurons):
    for node in output_neurons:
        node.back_propogation()

def input(input_neurons):

if __name__ == "__main__":
    input_neurons, hidden_neurons, output_neurons = construct_network(2, 1, 1, 0.2)

    for i in range(10):
        back_propogate(output_neurons)

