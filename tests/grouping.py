__author__ = "Zack Snyder"
__date__ = "1/25/19"

import threading
import time

run_time = 1
max_nodes_per_group = 4

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

    def all_nodes(self):
        return self._all_nodes
    
    def all_dict(self):
        return self._node_dict

    def description(self):
        return {node: self._node_dict[node] for node in self.nodes}

    def __init__(self, node_id, dictionary=dict(), max_size=0):

        self.node_id = node_id
        self._node_dict = dictionary
        self.max_size = max_size

        # _nodes contains a list of node addresses ordered by shortest distance
        self._all_nodes = list(node for node, value in sorted(dictionary.items(), key=lambda kv: kv[1]) )
        self.nodes = self._all_nodes[:] #[self.node_id]

    def merge(self, group):

        if self.node_id in group.all_nodes()[:self.max_size + 1]:
            if group.node_id not in self.nodes: 
                self.nodes.append(group.node_id)
            if len(group.all_nodes()) < self.max_size:
                self.max_size = len(group.all_nodes())
        elif group.node_id in self.nodes:
            self.nodes.remove(group.node_id)

        self.nodes = self.nodes[:self.max_size]


def create_group(node, max_nodes):

    current_group = Group(node, signal_strength_table[node], max_nodes)
    t_end = time.time() + run_time
    while time.time() < t_end: 

        # Make a copy of the group structure before changes
        before = signal_strength_table.copy()

        # Merge group with other groups nearby
        for n in current_group.nodes[:current_group.max_size + 1]:
            if n != node: 
                neighbor_group = Group(n, signal_strength_table[n], max_nodes)
                current_group.merge(neighbor_group)
            

        # Update global storage
        signal_strength_table[node] = current_group.description()
        # Print resulting group
        print(str(node) + ": " + str(current_group.nodes))
        time.sleep(0.2)

        after = signal_strength_table
        if before == after: break


for node, _ in signal_strength_table.items():
    create_group(node, max_nodes_per_group)
    # time.sleep(0.1)
    # break

t2_end = time.time() + run_time
while time.time() < t2_end: pass

print(signal_strength_table)
