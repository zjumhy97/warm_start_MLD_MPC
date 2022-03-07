# test for warm_start
import numpy as np
import gurobipy as gp
from gurobipy import *

try:
    # 参数
    prob_Q = np.identity(4)  # Q^TQ=Q
    prob_x0 = np.array([0.3, 0.4, 0.5, 0.6])
    prob_A = np.identity(4)
    prob_B = np.array([[0.1, 0.2, 0.3, 1, 0, 0, 0],
                       [0.1, 0.2, 0.3, 0, 1, 0, 0],
                       [0.1, 0.2, 0.3, 0, 0, 1, 0],
                       [0.1, 0.2, 0.3, 0, 0, 0, 1]])
    prob_BT = np.transpose(prob_B)
    prob_F = np.identity(4)
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
    prob_h = np.array([1, 1, 1.5, 1])

    #     # Primal
    #     model = gp.Model('miqp')
    #
    #     prob_x = model.addMVar((4, 2), vtype=GRB.CONTINUOUS, name='x',lb=-1e20,ub=1e20)
    #     prob_u = model.addMVar(7, vtype=GRB.CONTINUOUS, name='u',lb=-1e20,ub=1e20)
    #
    #     model.setObjective(sum(prob_x[:, i] @ prob_Q @ prob_x[:, i] for i in range(2)), GRB.MINIMIZE)
    #
    #     model.addConstr(prob_x[:, 0] == prob_x0, name='c1')
    #     model.addConstr(prob_x[:, 1] == prob_A @ prob_x[:, 0] + prob_B @ prob_u, name='c2')
    #     model.addConstr(prob_F @ prob_x[:, 0] + prob_G @ prob_u <= prob_h, name='c3')
    #     model.addConstr(prob_V @ prob_u >= prob_v_underline, name='c4')
    #     model.addConstr(prob_V @ prob_u <= prob_v_bar, name='c5')
    #
    #     # model.setParam('outPutFlag', 0)  # 不输出求解日志
    #
    #     # 限制模型用 dual simplex method 求解
    #     model.setParam('Method', 1)
    #     model.optimize()
    #
    #     print(model.getAttr("D"))
    #
    #     # print('obj=', model.objVal)
    #     # for v in model.getVars():
    #     #     print(v.varName, ':', v.x)
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

    prob_lambda_d = model.addMVar((4, 2), vtype=GRB.CONTINUOUS, name='lambda_d', lb=-1e20, ub=1e20)
    prob_mu_d = model.addMVar(4, vtype=GRB.CONTINUOUS, name='mu_d', lb=0, ub=1000)
    prob_nu_d = model.addMVar((4, 2), vtype=GRB.CONTINUOUS, name='nu_d', lb=0, ub=1e20)
    prob_z_d = model.addMVar(4, vtype=GRB.CONTINUOUS, name='z_d', lb=-1e20, ub=1e20)

    model.setObjective(-0.25 * (prob_z_d @ prob_z_d)
                       - 0.25 * (prob_lambda_d[:, 1] @ prob_lambda_d[:, 1]) - prob_lambda_d[:, 0] @ prob_x0
                       - prob_mu_d @ prob_h + prob_nu_d[:, 0] @ prob_v_underline - prob_nu_d[:, 1] @ prob_v_bar
                       , GRB.MAXIMIZE)

    model.addConstr(prob_z_d == prob_lambda_d[:, 0] - prob_A @ prob_lambda_d[:, 1] + prob_F @ prob_mu_d, name='d1')
    model.addConstr(
        -prob_BT @ prob_lambda_d[:, 1] + prob_GT @ prob_mu_d + prob_VT @ prob_nu_d[:, 1] - prob_VT @ prob_nu_d[:,
                                                                                                     0] == 0, name='d2')

    # model.setParam('outPutFlag', 0)  # 不输出求解日志
    model.setParam('Method', 1)
    model.optimize()





    # model.write('test.sol')
    # print('obj=', model.objVal)
    # for v in model.getVars():
    #     print(v.varName, ':', v.x)
    #
    # prob_vars = model.getVars()
    #
    # print(1)

    # 现在要做的事情是如何将 上面 model 最后的 solution 作为 start 输入到下面的 model_new 中？


    # model_new = gp.Model('miqp_dual_new')
    #
    # prob_lambda_d_new = model_new.addMVar((4, 2), vtype=GRB.CONTINUOUS, name='lambda_d', lb=-1e20, ub=1e20)
    # prob_mu_d_new = model_new.addMVar(4, vtype=GRB.CONTINUOUS, name='mu_d', lb=0, ub=1000)
    # prob_nu_d_new = model_new.addMVar((4, 2), vtype=GRB.CONTINUOUS, name='nu_d', lb=0, ub=1e20)
    # prob_z_d_new = model_new.addMVar(4, vtype=GRB.CONTINUOUS, name='z_d', lb=-1e20, ub=1e20)
    #
    # model_new.update()
    # model_new.read('test.sol')
    #
    # model_new.setObjective(-0.25 * (prob_z_d_new @ prob_z_d_new)
    #                    - 0.25 * (prob_lambda_d_new[:, 1] @ prob_lambda_d_new[:, 1])
    #                    - prob_lambda_d_new[:, 0] @ prob_x0
    #                    - prob_mu_d_new @ prob_h
    #                    + prob_nu_d_new[:, 0] @ prob_v_underline
    #                    - prob_nu_d_new[:, 1] @ prob_v_bar, GRB.MAXIMIZE)
    #
    # model_new.addConstr(prob_z_d_new == prob_lambda_d_new[:, 0] - prob_A @ prob_lambda_d_new[:, 1] + prob_F @ prob_mu_d_new, name='d1')
    # model_new.addConstr(
    #     -prob_BT @ prob_lambda_d_new[:, 1] + prob_GT @ prob_mu_d_new + prob_VT @ prob_nu_d_new[:, 1] - prob_VT @ prob_nu_d_new[:,
    #                                                                                                  0] == 0, name='d2')
    #
    # # model.setParam('outPutFlag', 0)  # 不输出求解日志
    # model_new.setParam('Method', 1)
    # prob_vas_new = model_new.getVars()
    # model_new.optimize()
    # model_new.update()
    # print('obj=', model_new.objVal)
    # # for v in model_new.getVars():
    # #     print(v.varName, ':', v.x)
    # #
    # # print(1)

except GurobiError as e:
    print('Error code ' + str(e.errno) + ':' + str(e))

except AttributeError:
    print('Encountered an attribute error')







