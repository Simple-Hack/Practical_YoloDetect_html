f=[-40;-30];
A=[1 -1 0 240;1 0 -1 120]'
b=[6;-1;-1;1200]
lb=[0;0]
ub=[+inf;+inf];
[x,val]=linprog(f,A,b,[],[],lb,ub)
disp(x)
disp(val)

