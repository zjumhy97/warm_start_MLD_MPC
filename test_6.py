import numpy as np
import gurobipy as gp
from gurobipy import *

try:
    # 参数
    T = 2 # time horizon
    u_dimension = 7 # input dimension
    prob_x0 = np.array([0.3, 0.4, 0.5, 0.6])
    prob_Q = np.identity(4) # Q^TQ=Q
    prob_QT = np.transpose(prob_Q)
    prob_R = np.zeros((7,7))
    prob_R[0][0] = 1
    prob_RT = np.transpose(prob_R)
    prob_A = np.identity(4)
    prob_AT = np.transpose(prob_A)
    prob_B = np.array([[0.1, 0.2, 0.3, 1, 0, 0, 0],
                  [0.1, 0.2, 0.3, 0, 1, 0, 0],
                  [0.1, 0.2, 0.3, 0, 0, 1, 0],
                  [0.1, 0.2, 0.3, 0, 0, 0, 1]])
    prob_BT = np.transpose(prob_B)
    prob_F = np.identity(4)
    prob_FT = np.transpose(prob_F)
    prob_G = np.array([[0, 0, 0, 1, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0],
                  [0, 0, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0, 1]])
    prob_GT = np.transpose(prob_G)
    prob_V = np.array([[0, 0, 0, 1, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0],
                  [0, 0, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0, 1]])
    prob_VT = np.transpose(prob_V)
    prob_v_bar = np.array([1, 1, 1, 1])
    prob_v_underline = np.array([0, 0, 0, 0])
    prob_h = np.array([100, 100, 100, 100])

#     # Primal
#     model = gp.Model('miqp')
#
#     prob_x = model.addMVar((4, T+1), vtype=GRB.CONTINUOUS, name='x',lb=-1e20,ub=1e20)
#     prob_u = model.addMVar((7, T), vtype=GRB.CONTINUOUS, name='u',lb=-1e20,ub=1e20)
#
#     model.setObjective(sum(prob_x[:, i] @ prob_Q @ prob_x[:, i] for i in range(T+1))
#                        + sum(prob_u[:, i] @ prob_R @ prob_u[:, i] for i in range(T)) , GRB.MINIMIZE)
#
#     model.addConstr(prob_x[:, 0] == prob_x0, name='c1')
#     for t in range(T):
#         model.addConstr(prob_x[:, t+1] == prob_A @ prob_x[:, t] + prob_B @ prob_u[:, t], name='c2')
#     for t in range(T):
#         model.addConstr(prob_F @ prob_x[:, t] + prob_G @ prob_u[:, t] <= prob_h, name='c3')
#     for t in range(T):
#         model.addConstr(prob_V @ prob_u[:, t] >= prob_v_underline, name='c4')
#     for t in range(T):
#         model.addConstr(prob_V @ prob_u[:, t] <= prob_v_bar, name='c5')
#
#     # model.setParam('outPutFlag', 0)  # 不输出求解日志
#
#     # 限制模型用 dual simplex method 求解
#     model.setParam('Method', 1)
#     model.optimize()
#
#     # print(model.getAttr("D"))
#
#     print('obj=', model.objVal)
#     for v in model.getVars():
#         print(v.varName, ':', v.x)
#
# except GurobiError as e:
#     print('Error code ' + str(e.errno) + ':' + str(e))
#
# except AttributeError:
#     print('Encountered an attribute error')


    # the optimum should be 1.04750001
    # Dual part
    # 模型
    model = gp.Model('miqp_dual')

    prob_lambda_d = model.addMVar((4, T+1), vtype=GRB.CONTINUOUS, name='lambda_d',lb=-1e20,ub=1e20)
    prob_mu_d = model.addMVar((4, T), vtype=GRB.CONTINUOUS, name='mu_d', lb=0, ub=1000)
    prob_nu_underline_d = model.addMVar((4, T), vtype=GRB.CONTINUOUS, name='nu_underline_d', lb=0,ub=1e20)
    prob_nu_bar_d = model.addMVar((4, T), vtype=GRB.CONTINUOUS, name='nu_bar_d', lb=0, ub=1e20)
    prob_rou_d = model.addMVar((4, T+1), vtype=GRB.CONTINUOUS, name='rou_d',lb=-1e20,ub=1e20)
    prob_delta_d = model.addMVar((7, T), vtype=GRB.CONTINUOUS, name='delta_d', lb=-1e20, ub=1e20)

    model.setObjective(-0.25 * sum(prob_rou_d[:, t] @ prob_rou_d[:, t] for t in range(T+1))
                       - sum(0.25 * (prob_delta_d[:, t] @ prob_delta_d[:, t]) + prob_mu_d[:, t] @ prob_h
                       + prob_nu_bar_d[:, t] @ prob_v_bar - prob_nu_underline_d[:, t] @ prob_v_underline
                       for t in range(T)) - prob_lambda_d[:, 0] @ prob_x0, GRB.MAXIMIZE)

    for t in range(T):
        model.addConstr(prob_QT @ prob_rou_d[:, t] + prob_lambda_d[:, t] - prob_AT @ prob_lambda_d[:, t+1]
                        + prob_FT @ prob_mu_d[:, t] == 0, name='d1')

    model.addConstr(prob_QT @ prob_rou_d[:, T] + prob_lambda_d[:, T] == 0, name='d2')

    for t in range(T):
        model.addConstr(prob_RT @ prob_delta_d[:, t] - prob_BT @ prob_lambda_d[:, t+1]
                        + prob_GT @ prob_mu_d[:, t] + prob_VT @ prob_nu_bar_d[:, t]
                        - prob_VT @ prob_nu_underline_d[:, t] == 0, name='d3')

    # model.setParam('outPutFlag', 0)  # 不输出求解日志
    model.setParam('Method', 1)
    model.optimize()


    print('obj=', model.objVal)
    for v in model.getVars():
        print(v.varName, ':', v.x)

    prob_vars = model.getVars()

    # 获取 shadow price，Primal问题原变量的最优值
    d = model.getConstrs()
    dualArray = []
    print(model.getAttr(GRB.Attr.NumConstrs))
    for i in range(model.getAttr(GRB.Attr.NumConstrs)):
        dualArray.append(d[i].getAttr(GRB.Attr.Pi))
    print('pi:', dualArray)

    # 打印输入变量
    print(dualArray[-u_dimension:])
    for i in range(1, T):
        print(dualArray[-(i+1) * u_dimension:-i * u_dimension])

except GurobiError as e:
    print('Error code ' + str(e.errno) + ':' + str(e))

except AttributeError:
    print('Encountered an attribute error')







