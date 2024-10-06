function dydt = df4(x,y)
    dydt= zeros(2,1);
    dydt(1)=y(2);
    dydt(2)=-y(1)-sin(2*x);
end

df4_handle = @df4; % 创建一个函数处理程序指向df4函数
[t,y] = ode45(df4_handle,[pi,2*pi],[1,1]); % 使用函数处理程序作为ode45的第一个参数

% 绘制解的图形
plot(t,y(:,1),'r',t,y(:,2),'b')
xlabel('t')
ylabel('y')
legend('y^','y^^')
title('Solution of df4')