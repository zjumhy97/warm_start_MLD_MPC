import gurobipy as grb
from gurobipy import *
import numpy as np
import time
# 需求：找到第一个不为 0 也不为 1 的元素，输出其位置
# 输入：[[a0, a1, a2], [b0, b1, b2], [c0, c1, c2]]
# 输出：(a, b),

# 实例：
# 输入：[[0,0,1], [1,0,1], [0.1, 0.2, 1]]
# 输出：(2, 0)
# time_start = time.time()
# a = [[0.00001,0,0.999999], [1,0,1], [0.1, 0.2, 1]]
# a = [0.3, 0.19999999999999996, 0.09999999999999998, 0.0]
# a = np.array(a)
# a[a<=1e-3] = 0
# a[a>=1-1e-3] = 0
# print(a)
# b = np.nonzero(a)
# print(b)
# print(b[0][0])
# print(b[1][0])
# for i in range(100):
#     a = [[0,0,1], [1,0,1], [0.1, 0.2, 1]]
#     a = np.array(a)
#     a[a==1] = 0
#
# time_end = time.time()
# time_avg = (time_end-time_start)/100
# print('time average = ', time_avg)

bool_vars = np.array([0.3, 0.19999999999999996, 0.09999999999999998, 0.0])
bool_vars[bool_vars <= 1e-3] = 0
bool_vars[bool_vars >= 1 - 1e-3] = 0
non_integral = np.nonzero(bool_vars)

if 1:  # T=1
    non_integral_d = non_integral[0][0]
    print(non_integral_d)
else:  # T>1
    non_integral_t, non_integral_d = non_integral[0][0], non_integral[1][0]
    print(non_integral_t, non_integral_d)
print(bool_vars)



























