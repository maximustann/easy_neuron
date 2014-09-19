#!/bin/env python
import random
import math
class Neuron(object):
    def __init__(self):
        self.learning_rate = 0.0
        self.output_value = 0.0
        self.input_list = []
        self.output_node_dict = {}
        self.input_node_dict = {}
        self.back_propogate_dict = {}
        self.beta = 0.0
        self.epoch = 0

    def increment_epoch(self):
        self.epoch += 1
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
            self.init_input_node_dict()
    def init_input_node_dict(self):
        for input_node in self.input_node_dict.keys():
            self.input_node_dict[input_node] = None

    def set_none(self):
        for node in self.input_node_dict.keys():
            self.input_node_dict[node] = None


    def output(self, output_value):
        for output_node, weight in self.output_node_dict.items():
            output_node.input(self, output_value * weight)


    def sigmoid(self, value_list):
        summ = 0.0
        for value in value_list:
            summ += value
        self.output_value = 1.0 / (1.0 + math.exp(-summ))
        return self.output_value

    def setup_output(self, output_node_list):
        for node in output_node_list:
            self.output_node_dict[node] = random.uniform(-1.0, 1.0)
            self.init_back_propogate_dict(node)
            #print "[First time] From", self, "To:", node, "weight: ", self.output_node_dict[node]


    def adjust_weight(self, output_node, delta_weight):
        self.output_node_dict[output_node] += delta_weight
        #print "[%d] From " % self.epoch, self, "To: ", output_node, "weight: ", self.output_node_dict[output_node]


    def calculate_beta(self, output_node, higher_output, higher_beta):
        beta = self.output_node_dict[output_node] * higher_output * (1.0 - higher_output) * higher_beta
        return beta
        
    def delta_rule(self, higher_output, higher_beta):
        delta_weight = self.learning_rate * self.output_value * higher_output * (1.0 - higher_output) * higher_beta
        return delta_weight


    def back_propogation(self):
        for input_node in self.input_node_dict.keys():
            input_node.receive_feedback(self, self.output_value, self.beta)
        self.output_value = None
        self.increment_epoch()

    def receive_feedback(self, output_node, higher_output, higher_beta):
        self.back_propogate_dict[output_node] = [higher_output, higher_beta]
        if not None in self.back_propogate_dict.values():
            for output_node, context in self.back_propogate_dict.items():
                higher_output = context[0]
                higher_beta = context[1]
                self.beta += self.calculate_beta(output_node, higher_output, higher_beta)
                self.init_back_propogate_dict(output_node)
                delta_weight = self.delta_rule(higher_output, higher_beta)
                self.adjust_weight(output_node, delta_weight)
        self.back_propogation()

class Input_neuron(Neuron):
    def __init__(self):
        super(Input_neuron, self).__init__()
        self.output_value = None
        self.epoch = 0

    def input(self, value):
        self.output_value = value
        self.output()

    def output(self):
        for output_node, weight in self.output_node_dict.items():
            output_node.input(self, self.output_value * weight)

    def delta_rule(self, higher_output, higher_beta):
        delta_weight = self.learning_rate * self.output_value * higher_output * (1.0 - higher_output) * higher_beta
        return delta_weight

    def adjust_weight(self, output_node, delta_weight):
        self.output_node_dict[output_node] += delta_weight
        self.increment_epoch()
        #print "[%d] From " % self.epoch, self, "To: ", output_node, "weight: ", self.output_node_dict[output_node]

    def receive_feedback(self, output_node, higher_output, higher_beta):
        self.back_propogate_dict[output_node] = [higher_output, higher_beta]
        if not None in self.back_propogate_dict.values():
            for output_node, context in self.back_propogate_dict.items():
                higher_output = context[0]
                higher_beta = context[1]
                self.init_back_propogate_dict(output_node)
                delta_weight = self.delta_rule(higher_output, higher_beta)
                self.adjust_weight(output_node, delta_weight)

class Output_neuron(Neuron):
    def __init__(self):
        super(Output_neuron, self).__init__()
        self.desired_value = None

    def input(self, input_node, value):
        self.input_node_dict[input_node] = value
        if not None in self.input_node_dict.values():
            self.output_value = self.sigmoid(self.input_node_dict.values())

    def calculate_beta_weight(self):
        self.beta = self.desired_value - self.output_value

    def setup_desired_value(self, value):
        self.desired_value = value

    def output(self):
        print self.output_value

    def back_propogation(self):
        self.calculate_beta_weight()
        for input_node in self.input_node_dict.keys():
            input_node.receive_feedback(self, self.output_value, self.beta)
        self.increment_epoch()

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

def back_propogate(output_neurons, desired_value):
    for node in output_neurons:
        node.setup_desired_value(desired_value)
    for node in output_neurons:
        node.back_propogation()


def epoches(input_neurons, output_neurons, data1, data2, target):
    #print "This is input data1 = %d, data2 = %d" % (data1, data2)
    input_neurons[0].input(data1)
    input_neurons[1].input(data2)
    back_propogate(output_neurons, target)
    #output_neurons[0].output()

if __name__ == "__main__":
    input_neurons, hidden_neurons, output_neurons = construct_network(2, 1, 1, 0.2)
    for i in range(1000):
        epoches(input_neurons, output_neurons, 1, 1, 0)
        #epoches(input_neurons, output_neurons, 0, 0, 0)
        epoches(input_neurons, output_neurons, 1, 0, 1)
        #epoches(input_neurons, output_neurons, 0, 1, 1)

    print "===================TESTING!!!!!===================="

    print "INPUT 1 an 1"
    input_neurons[0].input(1)
    input_neurons[1].input(1)
    output_neurons[0].output()

    '''
    print "INPUT 0 an 0"
    input_neurons[0].input(0)
    input_neurons[1].input(0)
    output_neurons[0].output()
    '''
    print "INPUT 1 an 0"
    input_neurons[0].input(1)
    input_neurons[1].input(0)
    output_neurons[0].output()
    '''
    print "INPUT 0 an 1"
    input_neurons[0].input(0)
    input_neurons[1].input(1)
    output_neurons[0].output()
    '''
