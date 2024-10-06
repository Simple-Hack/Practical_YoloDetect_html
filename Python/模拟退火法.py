import math
import random


# 温度变化函数
def T_update(t,T0):  # t 为推移时间，即每需要更新一次，t+1，表示冷却一次
    T=T0/math.log(1+t)
    return T

# 计算路径长函数
def path_len(path):
    path_dis = 0
    for i in range(len(path) - 1):
        two_dis = abs(path[i + 1] - path[i])  # 两点距离
        path_dis += two_dis

    path_dis += abs(path[-1] - path[0])
    return path_dis

# 得到新路径函数
def change_path(path, i, j):
    path_new=[]
    for t in path:
        path_new.append(t)

    c = path_new[i]
    path_new[i] = path_new[j]
    path_new[j] = c
    return path_new

# metropolis 准则
def metropolis(path_old,path_new,T):
    len_new=path_len(path_new)
    len_old=path_len(path_old)
    detE=len_new-len_old
    if detE<=0:
        p=1
    else:
        p=math.pow(math.e,-detE/T)
    return p

# 退火法函数
def disfire(path,T=20000,T_end=0.0001,iteration=10000):
    # 参数： 初始路径，初始温度，结束温度，每个温度下的迭代次数
    n=len(path)
    t=0
    while T>=T_end:
        t +=1
        count=0  # 计数
        while count < iteration:
            count += 1
            i=random.randint(0,n-1)
            j=random.randint(0,n-1)
            path_new=change_path(path,i,j)
            p=metropolis(path,path_new,T)
            p_random=random.random()

            if p_random <= p: # 当 path_new 更优时，p=1 , p_random<=p必成立, 若path_new不优，则以一定概率p变成path_new
                path=path_new
        print('温度',T,'下的优解：',path)
        T=T_update(t,T)

    best=path_len(path)
    print('最优解为：',path)
    print('最优解长度：',best)
path=[i for i in range(1,114)]
random.shuffle(path)
disfire(path)