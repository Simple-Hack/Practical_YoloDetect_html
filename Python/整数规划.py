import pulp as pl
#定义模型
mod=pl.LpProblem(name='IntModel',sense=pl.LpMaximize)

#决策变量 int,constius,binary
x=pl.LpVariable(name='x',cat=pl.LpInteger)
y=pl.LpVariable(name='y',cat=pl.LpInteger)
# # Define the decision variables
# x = {i: pl.LpVariable(name=f"x{i}", lowBound=0, cat=pl.LpInteger) for i in range(1, 9)}

#添加约束
mod+=(2*x+3*y-6>=0,'First')
mod+=(x+3*y-3==0,'Second')

#添加目标函数
mod+=x+3 * y
status=mod.solve()
# Get the results
print(f"status: {mod.status}, {pl.LpStatus[mod.status]}")
print(f"objective: {mod.objective.value()}")
 
for var in mod.variables():
    print(f"{var.name}: {var.value()}")
 
for name, constraint in mod.constraints.items():
    print(f"{name}: {constraint.value()}")