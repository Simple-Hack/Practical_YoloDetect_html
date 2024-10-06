import math


D=[-800,-600,-400,-200,0,200,400,600,800]

def cal_depth(x):
    former_D=70
    return former_D-x*math.sin(1.5*math.pi/180)

def cal_width(x):
    alpha=1.5*math.pi/180
    sei_ta=2*math.pi/3
    return cal_depth(x)*math.sin(sei_ta/2)*(1/math.cos(sei_ta/2 + alpha) + 1/math.cos(sei_ta/2 - alpha))

def cal_eta(x,i,D):
    alpha=1.5*math.pi/180
    sei_ta=2*math.pi/3
    former_W2=cal_depth(D[i-1])*math.sin(sei_ta/2)/math.cos(sei_ta/2 - alpha)
    cur_W1=cal_depth(x)*math.sin(sei_ta/2)/math.cos(sei_ta/2 + alpha)
    up=cur_W1+former_W2-200/math.cos(alpha)
    down=cal_width(D[i-1])
    return up/down

depth=[]
width=[]
eta=[-100]
for i,x in enumerate(D):
    depth.append(cal_depth(x))
    width.append(cal_width(x))
    if i==0:
        continue
    else:
        eta.append(cal_eta(x,i,D))
for data in depth:
    print(f'{data:.2f}',end=' ')

print('\n')
for data in width:
    print(f'{data:.2f}',end=' ')
print('\n')
for data in eta:
    print(f'{data*100:.2f}',end=' ')


