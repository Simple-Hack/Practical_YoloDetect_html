import networkx as nx
from scipy.optimize import linprog

# 目标函数系数
c = [-40, -30]
# 不等式约束，系数
A = [[1, 1],
     [-1, 0],
     [0, -1],
     [240,120]]
b = [[6], [-1], [-1],[1200]]
# 等式约束，系数
Aeq = [[1, 2]]
beq = [3.5]

res = linprog(c, A, b)
print(res)