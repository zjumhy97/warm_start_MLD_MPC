'''
线性规划模型
max x+y+2z
s.t.
    x+2y+3z<=4
    x+y>=1
    x,y,z=0 or 1
'''

import gurobipy as grb
from gurobipy import *

# try:
#     # 模型
#     model = grb.Model('mip')
#
#     # 变量
#     x = model.addVar(vtype=GRB.BINARY, name='x')
#     y = model.addVar(vtype=GRB.BINARY, name='y')
#     z = model.addVar(vtype=GRB.BINARY, name='z')
#
#     # 目标函数
#     model.setObjective(x + y, GRB.MAXIMIZE)
#     # 约束
#     model.addConstr(x + y <= 1, name='c1')
#     model.addConstr(x + y >= 0.1, name='c2')
#     # 求解
#     model.setParam('outPutFlag', 0)  # 不输出求解日志
#     model.optimize()
#
#     # 输出
#     print('obj=', model.objVal)
#     for v in model.getVars():
#         print(v.varName, ':', v.x)
#
# except GurobiError as e:
#     print('Error code ' + str(e.errno) + ':' + str(e))
#
# except AttributeError:
#     print('Encountered an attribute error')



class BBTreeNode():
    def __init__(self, vars=set(), bool_vars=set(), objective=None, constraints=[],
                 upperbound=float('inf'), lowwerbound=float('inf')):
        self.vars = vars
        self.bool_vars = bool_vars
        self.objective = objective
        self.constraints = constraints
        self.UB = upperbound
        self.LB = lowwerbound
        self.children = [] # Q: what is the use of children?

    def buildProblem(self):
        # prob = cvx.Problem(cvx.Minimize(self.objective), self.constraints)
        # 上面这个是cvx的实现，我这里是因为想用gurobipy，所以需要搞类似的实现
        prob = grb.Model('subproblem')
        # 添加变量，目标函数，约束
        # 正常的应该是 x = model.addVar(vtype=GRB.BINARY, name='x')
        prob.addVars(self.vars)
        prob.addVars(self.bool_vars)
        # 正常的应该是 model.setObjective(x + y, GRB.MAXIMIZE)
        prob.setObjective(self.objective)
        # 正常的应该是 model.addConstr(x + y <= 1, name='c1')
        prob.addConstrs(self.constraints)
        return prob






























