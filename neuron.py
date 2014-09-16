#!/bin/env python
import random
class Neuron(object):
    def __init__(self):
        self.value = None
        self.input_list = []
        self.output_node_dict = {}
    def input(self, value):
        self.value = value
    def output(self):
        pass
    def sigma_func(self):
        pass
    def setup(self, output_node):
        self.output_node_dict[output_node] = random.uniform(-1, 1)


class Input_neuron(Neuron):
    def __init__(self):
        super(Input_neuron, self).__init__(weight)
        self.value = None
    def output(self):
        for output_node, weight in self.output_node_dict.items():
            output_node.input(self.value * weight)


class Output_neuron(Neuron):
    def __init__(self):
        super(Output_neuron, self).__init__(weight)


if __name__ == "__main__":
    input_neuron_list =  [Input_neuron(random.uniform(-1, 1)) for i in range(2)]
    hidden_neuron_list =  [Neuron(random.uniform(-1, 1)) for i in range(2)]
    output_neuron_list =  [Output_neuron(random.uniform(-1, 1)) for i in range(1)]
    for neuron in input_neuron_list:
        print "input nodes: ", id(neuron)
    print
    for neuron in hidden_neuron_list:
        print "hidden nodes: ", id(neuron)
    print
    for neuron in output_neuron_list:
        print "output nodes: ", id(neuron)
