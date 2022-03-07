import gurobipy as grb
from gurobipy import *

model = grb.Model()

# vars = ["vtype=GRB.BINARY, name='y'","vtype=GRB.BINARY, name='z'"]
# cstrs = ["x + y <= 1, name='c1'","x + y >= 0.1, name='c2'"]
# y = model.addVar(vars[0])
# c1 = model.addConstr(cstrs[0])
# c2 = model.addConstr(cstrs[1])
kwargs_x = {"vtype": GRB.BINARY, "name": 'y'}
kwargs_y = {"vtype": GRB.BINARY, "name": 'y'}
x = model.addVar(**kwargs_x)
y = model.addVar(**kwargs_y)

# kwargs_cstr_1 = {"constraints": x + y <= 0.9, "name": 'c1'}
kwargs_cstr = [x + y <= 1, x + y >= 0.1]
kwargs_cstr_1 = [x + y <= 0.9]
kwargs_cstr_2 = [x + y >= 0.1]

# c1 = model.addConstr(**kwargs_cstr_1)
# c1 = model.addConstr(kwargs_cstr_1[0])
# c2 = model.addConstr(kwargs_cstr_2[0])

for i in kwargs_cstr:
    model.addConstr(i)



model.setObjective(x + y, GRB.MAXIMIZE)

model.optimize()



print(model.Status)