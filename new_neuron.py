#!/bin/env python
import random
import math
from scipy.stats import logistic
class Neuron(object):
    def __init__(self):
        self.learning_rate = None
        self.beta = 0
        self.output_value = 0
        self.bias = 1
        self.input_nodes_num = 0
        self.input_connection_id = []
        self.receive_value = 0
        self.count = 0
        self.back_count = 0
        self.input_connection = []
        self.output_connection = []
    def set_learning_rate(self, learning_rate):
        self.learning_rate = learning_rate
    def sigmoid(self):
        self.output_value = 1.0 / (1.0 + math.exp(-(self.receive_value + self.bias)))
        #self.output_value = 1.0 + math.e ** (-1.0 * (self.receive_value + self.bias))
        #self.output_value = logistic.cdf(self.receive_value + self.bias)
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
    def adjust_input_nodes_num(self, num):
        self.input_nodes_num = num
    def adjust_bias(self):
        delta_bias = self.learning_rate * (1 - self.output_value) * self.beta
        self.bias += delta_bias
    def notify_input(self, conn):
        if conn not in self.input_connection:
            self.input_connection.append(conn)
            self.input_nodes_num += 1
    def notify_output(self, conn):
        if conn not in self.output_connection:
            self.output_connection.append(conn)

    def receive_input(self, value):
        self.receive_value += value
        self.count += 1
        if self.count == self.input_nodes_num:
            self.sigmoid()
            self.count = 0
            self.send()

    def send(self):
        for output_conn in self.output_connection:
            output_conn.receive_send_to_output(self.output_value)

    def backpropagation(self, conn, weight, higher_output, higher_beta):
        self.cal_beta(weight, higher_output, higher_beta)
        conn.update_weight(self.cal_delta_weight(higher_output, higher_beta))
        self.back_count += 1
        if self.back_count == len(self.output_connection):
            self.adjust_bias()
            for connection in self.input_connection:
                connection.backpropagation(self.output_value, self.return_beta())
                self.output_value = 0
                self.back_count = 0

class Input_Nodes(Neuron):
    def __init__(self):
        super(Input_Nodes, self).__init__()
        self.input_value = 0
    def input(self, input_num):
        self.input_value = input_num
    def return_input(self):
        return self.input_value
    def start(self):
        self.send()
    def backpropagation(self, conn, weight, higher_output, higher_beta):
        self.cal_beta(weight, higher_output, higher_beta)
        conn.update_weight(self.cal_delta_weight(higher_output, higher_beta))
        self.back_count += 1
        if self.back_count == len(self.output_connection):
            self.input_value = 0
            self.back_count = 0
class Output_Nodes(Neuron):
    def __init__(self):
        super(Output_Nodes, self).__init__()
        self.desired = 0
    def init_desired_value(self, desired):
        self.desired = desired
    def cal_beta(self):
        self.beta = self.desired - self.output_value
    def receive_input(self, value):
        self.receive_value += value
        self.count += 1
        if self.count == self.input_nodes_num:
            self.adjust_bias()
            self.sigmoid()
            self.count = 0
    def output(self):
        return self.output_value

    def backpropagation(self):
        self.cal_beta()
        for conn in self.input_connection:
            conn.backpropagation(self.output_value, self.beta)


class Connection(object):
    def __init__(self):
        self.input_node = None
        self.output_node = None
        self.weight = 0
    def initilize_input_node(self, input_node):
        self.input_node = input_node
        self.input_node.notify_output(self)
    def initilize_output_node(self, output_node):
        self.output_node = output_node
        self.output_node.notify_input(self)
    def initilize_weight(self):
        self.weight = random.uniform(-1.0, 1.0)

    def update_weight(self, delta_weight):
        self.weight += delta_weight

    def return_weight(self):
        return self.weight

    def print_output_node(self):
        print "\t", id(self.output_node), ":", self.weight

    def receive_send_to_output(self, value):
        self.output_node.receive_input(value * self.weight)

    def backpropagation(self, higher_output, higher_beta):
        self.input_node.backpropagation(self, self.weight, higher_output, higher_beta)


class Network(object):
    def __init__(self):
        self.input_node_list = []
        self.output_node_list = []
        self.layer_num = 0
        self.hidden_layers = []
        self.temp_hidden_layers = []
    def initilize_input_nodes(self, input_num):
        self.input_node_list = [Input_Nodes() for _ in range(input_num)]
    def initilize_hidden_layer(self, layer_num):
        self.temp_hidden_layers = [[] for i in range(layer_num)]
    def initilize_hidden_nodes(self, layer, nodes_num):
        self.temp_hidden_layers[layer - 1] = [Neuron() for _ in range(nodes_num)]
    def initilize_output_nodes(self, output_num):
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
        for input_node in self.input_layer.keys():
            input_node.set_learning_rate(learning_rate)
        for layer in self.hidden_layers:
            for node in layer:
                node.set_learning_rate(learning_rate)
        for output_node in self.output_node_list:
            output_node.set_learning_rate(learning_rate)

    def learning_pattern(self, input_1, input_2, output):
        self.input_node_list[0].input(input_1)
        self.input_node_list[1].input(input_2)
        self.output_node_list[0].init_desired_value(output)

    def epoch(self, num):
        for i in range(num):
            self.learning_pattern(1,1,0)
            for input_node in self.input_node_list:
                input_node.start()
            for output_node in self.output_node_list:
                output_node.backpropagation()

            self.learning_pattern(0,0,0)
            for input_node in self.input_node_list:
                input_node.start()
            for output_node in self.output_node_list:
                output_node.backpropagation()

            self.learning_pattern(1,0,1)
            for input_node in self.input_node_list:
                input_node.start()
            for output_node in self.output_node_list:
                output_node.backpropagation()

            self.learning_pattern(0,1,1)
            for input_node in self.input_node_list:
                input_node.start()
            for output_node in self.output_node_list:
                output_node.backpropagation()

        #self.print_architecture()
    def test(self, input_1, input_2):
        self.input_node_list[0].input(input_1)
        self.input_node_list[1].input(input_2)
        for input_node in self.input_node_list:
            input_node.start()
        print "input: ", input_1, "and", input_2, "result: ", self.output_node_list[0].return_output()


if __name__ == "__main__":
    net = Network()
    net.initilize_input_nodes(2)
    net.initilize_hidden_layer(1)
    net.initilize_hidden_nodes(1, 2)
    #net.initilize_hidden_nodes(2, 5)
    net.initilize_output_nodes(1)
    net.construct()
    #net.print_architecture()
    net.initilize_learning_rate(0.2)
    net.epoch(100000)
    net.test(1,1)
    net.test(0,0)
    net.test(1,0)
    net.test(0,1)
