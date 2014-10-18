#!/bin/env python
import random
import math

class Neuron(object):
    def __init__(self):
        self.learning_rate = None
        self.beta = 0
        self.output_value = 0
    def set_learning_rate(self, learning_rate):
        self.learning_rate = learning_rate
    def sigmoid(self, value_list):
        self.output_value = 1.0 / (1.0 + math.exp(-sum(value_list)))
    def cal_beta(self, weight, higher_output, higher_beta):
        self.beta += weight * (1 - higher_output) * higher_beta
    def return_beta(self):
        temp_beta = self.beta
        self.beta = 0
        return temp_beta
    def cal_delta_weight(self, higher_output, higher_beta):
        delta_weight = self.learning_rate * self.output_value * (1 - higher_output) * higher_beta
        return delta_weight
    def return_output(self):
        return self.output_value

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
        self.desired = 0
    def init_desired_value(self, desired):
        self.desired = desired
    def cal_beta(self):
        self.beta = self.desired - self.output_value

class Connection(object):
    def __init__(self):
        self.input_node = None
        self.output_node = None
        self.Weight = 0
    def initilize_input_node(self, input_node):
        self.input_node = input_node
    def initilize_output_node(self, output_node):
        self.output_node = output_node
    def initilize_weight(self):
        self.weight = random.uniform(-1.0, 1.0)

    def update_weight(self, delta_weight):
        self.weight += delta_weight

    def return_weight(self):
        return self.weight

    def print_output_node(self):
        print "\t", id(self.output_node), ":", self.weight

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
        self.temp_hidden_layers = []
    def initilize_input_nodes(self, input_num):
        '''every input node is a list'''
        self.input_node_list = [Input_Nodes() for _ in range(input_num)]
    def initilize_hidden_layer(self, layer_num):
        '''every hidden nodes is a list, but because we don't know how 
            many nodes in each layer, in this step, the node list is empty
        '''
        self.temp_hidden_layers = [[] for i in range(layer_num)]
    def initilize_hidden_nodes(self, layer, nodes_num):
        '''each hidden node is a list
        '''
        self.temp_hidden_layers[layer - 1] = [Neuron() for _ in range(nodes_num)]
    def initilize_output_nodes(self, output_num):
        '''each output node is a list, contain two parts
            1.output node itself
            2.bias node 
        '''
        self.output_node_list = [Output_Nodes() for _ in range(output_num)]

    def built_input_connection(self):
        self.input_layer = {}
        for node in self.input_node_list:
            conns = []
            for output_node in self.temp_hidden_layers[0]:
                conn = Connection()
                conn.initilize_input_node(node)
                conn.initilize_output_node(output_node)
                conn.initilize_weight()
                conns.append(conn)
            self.input_layer[node] = conns

    def built_hidden_connection(self):
        for i in range(len(self.temp_hidden_layers) - 1):
            hidden_layer = {}
            for node in self.temp_hidden_layers[i]:
                conns = []
                for output_node in self.temp_hidden_layers[i + 1]:
                    conn = Connection()
                    conn.initilize_input_node(node)
                    conn.initilize_output_node(output_node)
                    conn.initilize_weight()
                    conns.append(conn)
                hidden_layer[node] = conns
            self.hidden_layers.append(hidden_layer)
        
        last_hidden_layer = {}
        for node in self.temp_hidden_layers[self.layer_num - 1]:
            conns = []
            for output_node in self.output_node_list:
                conn = Connection()
                conn.initilize_input_node(node)
                conn.initilize_output_node(output_node)
                conn.initilize_weight()
                conns.append(conn)
            last_hidden_layer[node] = conns
        self.hidden_layers.append(last_hidden_layer)

    def print_architecture(self):
        print "========================="
        print "Input Nodes"
        for input_node, connections in self.input_layer.items():
            print id(input_node), ":"
            print "\tOutput nodes\t:\tWeights"
            for connection in connections:
                connection.print_output_node()
        print "Hidden Nodes"
        for i, layer in enumerate(self.hidden_layers):
            print "Layer: ", i + 1
            for node, connections in layer.items():
                print id(node), ":"
                print "\tOutput nodes\t:\tWeights"
                for connection in connections:
                    connection.print_output_node()


    def construct(self):
        self.built_input_connection()
        self.built_hidden_connection()

    def initilize_learning_rate(self, learning_rate):
        pass
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
    net.initilize_output_nodes(2)
    net.construct()
    net.print_architecture()
    #net.learning_pattern(1,1,0)
    #net.learning_pattern(0,0,0)
    #net.learning_pattern(1,0,1)
    #net.learning_pattern(0,1,1)
    #net.epoch(500)
    #net.test(1,1)
