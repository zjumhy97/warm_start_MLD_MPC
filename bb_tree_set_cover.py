# bb_tree_set_cover.py
# author: Haoyu Miao
# date: 2022/03/02

# import gurobipy
import gurobipy as grb
import copy
from heapq import *
import numpy as np
import itertools
counter = itertools.count() # create a iterator from 0

class BBTree():
    def __init__(self, root_nodes=set(), tolerance=1e-3, treeUB=float('inf'), treeLB=-float('inf')):
        # 按照 paper 中的说法，frontier，其中每个集合的下界，以及 treeUB，这三个是必须的
        # 【重要！！！】 frontier 中每个 node 的下界应该是 parent node 对应对偶问题的界
        self.frontier = root_nodes
        self.tolerance = tolerance
        self.treeUB = treeUB
        self.treeLB = treeLB
        self.bestnode = None

    def selectSubproblem(self, heap):
        # 从 heap 中选取一个 node，
        # 选取的规则是：best-first，哪个下界最小，选哪个
        # such that UB-LB > self.tolerance
        node = BBTreeNode()
        return node

    def branch(self):
        return [1, 2]

    def bbtreeSolve(self):
        # 堆 heap 是用来控制循环的机制，heap 不为空意味着还有可以进行分枝的节点，算法仍要继续
        # 但是 heap 为空意味着所有的节点都被剪枝剪掉了，不需要
        # 构建 heap 的时候应该把 frontier 中的节点都纳入进来
        heap = []
        for node in self.frontier:
            heappush(heap, node)
        print(heap)
        # Q: 根节点需要求解吗？
        # Q: 需要更新B&B树上界和最新节点吗？
        nodecount = 0
        while len(heap) > 0: # 这个循环是边界 frontier 迭代的循环，第0次，frontier就是根节点
            # 用 len(heap) 作为循环条件的缺点——每次求解bb树都要求解完，而不是中途求到feasible的解也可以退出
            nodecount += 1
            print("Heap Size: ", len(heap))
            # solve the subproblem chosen by selectSubproblem function, get relaxation value \theta(V^{i})
            # 满足条件的话，从边界中选一个节点求解, 2:optimal 3:infeasible 5:unbounded
            node = self.selectSubproblem(heap) # 从 frontier 中还是 heap 中？
            # 选择一个节点后，应该把节点从 heap 中弹出
            heap.remove(node) # heap 中移除，但是 frontier 中不移除
            prob = node.buildProblem()
            prob.optimize()
            if prob.Status == 2: # the status is optimal, not infeasible (3) or unbounded (5)
                res = prob.objVal
                if res >= self.treeUB - self.tolerance: # pruning
                    print("Relaxed Problem Stinks. Killing this branch.")
                    node.LB = res
                    pass
                elif node.isIntegral(): # solution update
                    print("New Best Integral solution.")
                    self.treeUB = res
                    node.LB = res
                    self.bestnode = node
                else: # branching
                    newnodes = node.branch()
                    self.frontier.remove(node)
                    for newnode in newnodes:
                        heappush(self.frontier, newnode)
                        heappush(heap, newnode)
        print("Nodes searched: ", nodecount)
        return self.treeUB, self.bestnode, self.frontier
        # 每次求解完需要返回哪些东西传给下一个B&B树？
        # 每次求解完后不需要的节点所占的内存如何释放？


class BBTreeNode():
    def __init__(self, vars=set(), bool_vars=set(), objective=0, constraints=[], UB=float('inf'), LB=-float('inf')):
        self.vars = vars
        self.bool_vars = bool_vars
        self.objective = objective
        self.constraints = constraints
        self.UB = UB
        self.LB = LB
        self.children = [] # Q: what is the use of children?

    def buildProblem(self):
        # 所以这里实际要求的是原问题 P 的松弛问题 P(V) 的对偶问题 D(V)
        # 如果满足强对偶性的要求，求解得到的 D(V) 的最优值和 P(V)的最优值，也就是节点的下界 node.LB
        prob = grb.Model('subproblem')
        # 添加对偶变量（对偶乘子），目标函数，约束
        # 正常的应该是 x = model.addVar(vtype=GRB.BINARY, name='x')
        prob.addVars(self.vars)
        prob.addVars(self.bool_vars)
        # 正常的应该是 model.setObjective(x + y, GRB.MAXIMIZE)
        prob.setObjective(self.objective)
        # 正常的应该是 model.addConstr(x + y <= 1, name='c1')
        prob.addConstrs(self.constraints)
        return prob

    def isIntegral(self):
        # 求解对偶问题怎么知道原变量是多少？从而如何判断是不是整数解？
        # 判断整数与否针对的是当前求解的特定的问题中的整数变量，因此因当先完成 buildProblem 函数
        pass


# 主代码
# tree = BBTree()
# tree.bbtreeSolve()














































