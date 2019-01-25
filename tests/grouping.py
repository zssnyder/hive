__author__ = "Zack Snyder"
__date__ = "1/25/19"

import thread
import time

signal_strength_table = {
    1: {1:0,    2:5,    3:3.5,  4:4,    5:4,    6:7,    7:5.5},
    2: {1:5,    2:0,    3:5,    4:6.5,  5:10,   6:6.5,  7:4.5},
    3: {1:3.5,  2:5,    3:0,    4:4,    5:8,    6:11.5, 7:7},
    4: {1:4,    2:6.5,  3:4,    4:0,    5:6,    6:7,    7:10.5},
    5: {1:4,    2:10,   3:8,    4:6,    5:0,    6:4,    7:7},
    6: {1:7,    2:6.5,  3:11.5, 4:7,    5:4,    6:0,    7:5},
    7: {1:5.5,  2:4.5,  3:7,    4:10.5, 5:7,    6:5,    7:0}
}

class Group():

    def __init__(self, node_id, values=None, dictionary=None):

        self.node_id = node_id
        self.nodes = []

        for value in values:
            for key, v in dictionary.items():
                if value == v and key not in self.nodes:
                    self.nodes.append(key)
                    break

    def merge(self, group):
        if self.node_id in group.nodes:
            for node in reversed(self.nodes):
                # print(node)
                if node not in group.nodes:
                    # print("Node not found")
                    self.nodes.remove(node)
        else: pass
            # self.nodes.remove(group.node_id)

def create_group(node, divisor):
    sorted_strengths = sorted(signal_strength_table[node].values()) # list(map(dict.itervalues, signal_strengths))
    # print(sorted_strengths)

    current_group = Group(node, sorted_strengths[:len(sorted_strengths)//divisor], signal_strength_table[node])
    # print(group_1.nodes)

    while True: 
        for n in current_group.nodes:
            # print(n)
            if n != node: 
                n_sorted_strengths = sorted(signal_strength_table[n].values())
                # print(n_sorted_strengths)
                neighbor_group = Group(n, n_sorted_strengths, signal_strength_table[n])
                # print(group_3.nodes)
                current_group.merge(neighbor_group)
                # print(group_1.nodes)

        for k, v in signal_strength_table[node].items(): 
            if k not in current_group.nodes: 
                signal_strength_table[node].pop(k, v)
                # print("Popped " + str(k) + " from Node " + str(node))
        print(str(node) + ": " + str(current_group.nodes))

        time.sleep(1)

for node, _ in signal_strength_table.items():
    num_of_groups = len(signal_strength_table) // 2
    thread.start_new_thread(create_group, (node, 2))

while True: pass
    # break
