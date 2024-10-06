% 定义函数shier
function xt = shier(~, x)
    k1 = 1; k2 = 0.5; b = 0.1; c = 0.02;
    xt = [x(1)*(k1 - b*x(2)); x(2)*(-k2 + c*x(1))];
end

% 清除工作空间中的变量
clear

% 设定时间范围和初始条件
ts = linspace(0, 15, 151); % 使用linspace生成等间距的时间点
x0 = [25; 2];

% 调用ode45求解微分方程
[t, x] = ode45(@shier, ts, x0);

% 创建包含两个子图的窗口
figure;
subplot(2,2,1)
% 左边子图：时域响应图
plot(t, x(:, 1), t, x(:, 2)) % 绘制两个状态变量的时间序列
grid on % 添加网格线
title('Time Domain Response') % 添加标题
xlabel('Time') % 设置x轴标签
ylabel('State Variables') % 设置y轴标签
%legend('x_1(t)', 'x_2(t)') % 添加图例
% 右边子图：相平面图
subplot(2,2,2);
plot(x(:, 1), x(:, 2)) % 绘制相平面图
grid on % 添加网格线
title('Phase Plane') % 添加标题
xlabel('x_1') % 设置x轴标签
ylabel('x_2') % 设置y轴标签

subplot(2,2,[3,4])
grid on 
x5=linspace(-2*pi,2*pi,100)
y5=cos(2*x5)
plot(x5,y5)
