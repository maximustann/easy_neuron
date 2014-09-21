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
        self.back_propagate_dict = {}
        self.beta = 0.0
        self.epoch = 0

    def increment_epoch(self):
        self.epoch += 1
    def init_back_propagate_dict(self, output_node):
        self.back_propagate_dict[output_node] = None

    def set_desired_value(self, output_node, value):
        self.back_propagate_dict[output_node] = value #output_node, consist of output and beta

    def setup_bias_node(self, bias_node):
        self.input_node_dict[bias_node] = None

    def set_learning_rate(self, rate):
        self.learning_rate = rate


    def setup_input(self, input_node_list):
        for node in input_node_list:
            self.input_node_dict[node] = None

    def input(self, input_node, value):
        #print input_node, "input value = ", value
        self.input_node_dict[input_node] = value
        if not None in self.input_node_dict.values():
            output_value = self.sigmoid(self.input_node_dict.values())
            self.output(output_value)
            self.init_input_node_dict()
    def init_input_node_dict(self):
        for input_node in self.input_node_dict.keys():
            self.input_node_dict[input_node] = None

    def output(self, output_value):
        for output_node, weight in self.output_node_dict.items():
            output_node.input(self, output_value * weight)

    def show_connection(self):
        print "I'm: ", self
        print "Input connections:"
        for node in self.input_node_dict.keys():
            print "Input Node: ", node
        print "Output connections:"
        for node in self.output_node_dict.keys():
            print "Output Node: ", node, "Weight = ", self.output_node_dict[node]
        print "***********************************************************************"


    def sigmoid(self, value_list):
        #print "Im", self
        #print value_list
        summ = 0.0
        for value in value_list:
            summ += value
        try:
            self.output_value = 1.0 / (1.0 + math.exp(-summ))
        except OverflowError, e:
            self.output_value = 1
            #print "What the hack?!: " ,summ, e
        return self.output_value

    def setup_output(self, output_node_list):
        for node in output_node_list:
            self.output_node_dict[node] = random.uniform(-1.0, 1.0)
            self.init_back_propagate_dict(node)
            #print "[First time] From", self, "To:", node, "weight: ", self.output_node_dict[node]


    def adjust_weight(self, output_node, delta_weight):
        self.output_node_dict[output_node] += delta_weight
        print "[%d] From " % self.epoch, self, "To: ", output_node, "weight: ", self.output_node_dict[output_node]


    def calculate_beta(self, output_node, higher_output, higher_beta):
        beta = self.output_node_dict[output_node] * higher_output * (1.0 - higher_output) * higher_beta
        return beta

    def delta_rule(self, higher_output, higher_beta):
        delta_weight = self.learning_rate * self.output_value * higher_output * (1.0 - higher_output) * higher_beta
        return delta_weight


    def back_propagation(self):
        for input_node in self.input_node_dict.keys():
            input_node.receive_feedback(self, self.output_value, self.beta)
        self.output_value = None
        self.increment_epoch()

    def receive_feedback(self, output_node, higher_output, higher_beta):
        self.back_propagate_dict[output_node] = [higher_output, higher_beta]
        if not None in self.back_propagate_dict.values():
            for output_node, context in self.back_propagate_dict.items():
                higher_output = context[0]
                higher_beta = context[1]
                self.beta += self.calculate_beta(output_node, higher_output, higher_beta)
                self.init_back_propagate_dict(output_node)
                delta_weight = self.delta_rule(higher_output, higher_beta)
                self.adjust_weight(output_node, delta_weight)
        self.back_propagation()

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
        print "[%d] From " % self.epoch, self, "To: ", output_node, "weight: ", self.output_node_dict[output_node]

    def receive_feedback(self, output_node, higher_output, higher_beta):
        self.back_propagate_dict[output_node] = [higher_output, higher_beta]
        if not None in self.back_propagate_dict.values():
            for output_node, context in self.back_propagate_dict.items():
                higher_output = context[0]
                higher_beta = context[1]
                self.init_back_propagate_dict(output_node)
                delta_weight = self.delta_rule(higher_output, higher_beta)
                self.adjust_weight(output_node, delta_weight)

class Output_neuron(Neuron):
    def __init__(self):
        super(Output_neuron, self).__init__()
        self.desired_value = None

    def input(self, input_node, value):
        #print input_node, "input value = ", value
        self.input_node_dict[input_node] = value
        #print "Hello: ", self.input_node_dict[input_node]
        if not None in self.input_node_dict.values():
            self.output_value = self.sigmoid(self.input_node_dict.values())
            #print self.output_value

    def calculate_beta_weight(self):
        self.beta = self.desired_value - self.output_value

    def setup_desired_value(self, value):
        self.desired_value = value

    def output(self):
        #print self.output_value
        return self.output_value

    def back_propagation(self):
        self.calculate_beta_weight()
        for input_node in self.input_node_dict.keys():
            input_node.receive_feedback(self, self.output_value, self.beta)
        self.increment_epoch()

class Bias_neuron(object):
    def __init__(self):
        self.output_value = 1
        self.learning_rate = None

    def set_learning_rate(self, learning_rate):
        self.learning_rate = learning_rate

    def output(self):
        self.output_node.input(self, self.output_value)

    def change_output_value(self, delta):
        self.output_value += delta
    def calculate_delta(self, higher_output, higher_beta):
        return self.learning_rate * 1 * (1 - higher_output) * higher_beta


    def receive_feedback(self, output_node, higher_output, higher_beta):
        delta = self.calculate_delta(higher_output, higher_beta)
        self.change_output_value(delta)


    def setup_output(self, output_node):
        self.output_node = output_node

    def show_connection(self):
        print "I'm: ", self
        print "Output connections:"
        print "Output Node: ", self.output_node
        print "***********************************************************************"


def construct_network(number_input, number_hidden, number_output, learning_rate):
    input_neurons = [Input_neuron() for i in range(number_input)] #generate input nodes
    hidden_neurons = [Neuron() for i in range(number_hidden)]   #generate hidden nodes
    output_neurons = [Output_neuron() for i in range(number_output)] #generate output nodes
    bias_neurons = []
    #it's a one layer network, don't expect too much
    for node in input_neurons:
        node.setup_output(hidden_neurons)               #build output connection between input nodes and hidden nodes
        node.set_learning_rate(learning_rate)           #set input nodes' learning rate
    for node in hidden_neurons:

        node.setup_output(output_neurons)               #build output connection between hidden nodes and output nodes
        node.setup_input(input_neurons)                 #build input connection between input nodes and hidden nodes
        node.set_learning_rate(learning_rate)           #set hidden nodes' learning rate
        bias = Bias_neuron()
        bias.setup_output(node)
        node.setup_bias_node(bias)
        bias_neurons.append(bias)
    for node in output_neurons:
        node.setup_input(hidden_neurons)                #build input connection between hidden nodes and output nodes
        node.set_learning_rate(learning_rate)           #set output nodes' learning rate
        bias = Bias_neuron()
        bias.setup_output(node)
        node.setup_bias_node(bias)
        bias_neurons.append(bias)
    for node in bias_neurons:
        node.set_learning_rate(learning_rate)
    return input_neurons, hidden_neurons, output_neurons, bias_neurons

def show_structure(input_neurons, hidden_neurons, output_neurons, bias_neurons):
    print "Input nodes: "
    for node in input_neurons:
        node.show_connection()
    print "Hidden nodes: "
    for node in hidden_neurons:
        node.show_connection()

    print "Output nodes: "
    for node in output_neurons:
        node.show_connection()

    print "Bias nodes: "
    for node in bias_neurons:
        node.show_connection()

def back_propagate(output_neurons, desired_value):
    for node in output_neurons:
        node.setup_desired_value(desired_value)
    for node in output_neurons:
        node.back_propagation()


def epoches(input_neurons, bias_neurons, hidden_neurons, output_neurons, data1, data2, target):
    #print "This is input data1 = %d, data2 = %d" % (data1, data2)
    input_neurons[0].input(data1)
    input_neurons[1].input(data2)
    for node in bias_neurons:
        node.output()
    back_propagate(output_neurons, target)
    return output_neurons[0].output()


def two_one(input_neurons, output_neurons, bias_neurons):
    print "INPUT 1 an 1"
    input_neurons[0].input(1)
    input_neurons[1].input(1)
    for node in bias_neurons:
        node.output()
    return output_neurons[0].output()

def two_zero(input_neurons, output_neurons, bias_neurons):
    print "INPUT 0 an 0"
    input_neurons[0].input(0)
    input_neurons[1].input(0)
    for node in bias_neurons:
        node.output()
    return output_neurons[0].output()

def first_one(input_neurons, output_neurons, bias_neurons):
    print "INPUT 1 an 0"
    input_neurons[0].input(1)
    input_neurons[1].input(0)
    for node in bias_neurons:
        node.output()
    return output_neurons[0].output()

def second_one(input_neurons, output_neurons, bias_neurons):
    print "INPUT 0 an 1"
    input_neurons[0].input(0)
    input_neurons[1].input(1)
    for node in bias_neurons:
        node.output()
    return output_neurons[0].output()

if __name__ == "__main__":
    input_neurons, hidden_neurons, output_neurons, bias_neurons = construct_network(2, 1, 1, 0.7)
    #show_structure(input_neurons, hidden_neurons, output_neurons, bias_neurons)
    '''
    two_one(input_neurons, output_neurons, bias_neurons)
    two_zero(input_neurons, output_neurons, bias_neurons)
    first_one(input_neurons, output_neurons, bias_neurons)
    second_one(input_neurons, output_neurons, bias_neurons)
    '''
    #epoches(input_neurons, bias_neurons, hidden_neurons, output_neurons, 1, 1, 0)
    for i in range(10):
        epoches(input_neurons, bias_neurons, hidden_neurons, output_neurons, 1, 1, 0)
        epoches(input_neurons, bias_neurons, hidden_neurons, output_neurons, 1, 0, 1)
        epoches(input_neurons, bias_neurons, hidden_neurons, output_neurons, 0, 1, 1)
        epoches(input_neurons, bias_neurons, hidden_neurons, output_neurons, 0, 0, 0)

    print "===================TESTING!!!!!===================="
    #show_structure(input_neurons, hidden_neurons, output_neurons, bias_neurons)
    print two_one(input_neurons, output_neurons, bias_neurons)
    print two_zero(input_neurons, output_neurons, bias_neurons)
    print first_one(input_neurons, output_neurons, bias_neurons)
    print second_one(input_neurons, output_neurons, bias_neurons)
    #show_structure(input_neurons, hidden_neurons, output_neurons, bias_neurons)
