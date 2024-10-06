function f = fun1( x )      %f为返回结果，fun1为函数名，x为自变量（输入参数）
    f=sum(x.^2)+8               %函数
end

function [g,h] = fun2( x )              %输入参数x，fun2函数名，g为非线性不等式，h为非线性等式
    g=[-x(1)^2+x(2)-x(3)^2,x(1)+x(2)^2+x(3)^2-20];   %非线性不等式的结果矩阵g 
    h=[x(2)+2*x(3)^2-3,-x(1)-x(2)^2+2];              %非线性等式的结果矩阵h
end

clear
x0=[1,1,1];
lb=[0,0,0];
ub=[inf,inf,inf];
A=[];b=[];Aeq=[];beq=[];
[x,fval]=fmincon(@fun1,x0,A,b,Aeq,beq,lb,ub,@fun2)