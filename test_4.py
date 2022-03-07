import gurobipy as gp
from gurobipy import GRB
import copy
from heapq import *
import numpy as np
import itertools
counter = itertools.count() # create a iterator from 0

class node():
    def __init__(self, vector):
        self.vector = vector
    def show(self):
        print("My name is", self.name)
    def branch(self):
        children = []
        a = node(self.vector + np.array([1,1,1,1]))
        b = node(self.vector - np.array([1,1,1,1]))
        children.append(a)
        children.append(b)
        return children

root = node(vector = np.array([100,100,100,100]))

heap = [(next(counter),root)]
# for i in range(3):
#     new_nodes = root.branch()
#     for j in new_nodes:
#         heappush(heap, (next(counter), j))
new_nodes = root.branch()
for j in new_nodes:
    heappush(heap, (next(counter), j))

h, h_node = heappop(heap)

# 一个疑问，heappop的时候，如果heap是一个tuple，tuple的第一个元素是标量，会根据这个排序弹出最小的吗？
heap1 = [(0.1, root), (0.01, root), (0.2, root)]
h1, h_node1 = heappop(heap1)

print(1)



