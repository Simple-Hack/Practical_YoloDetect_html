from 熵权法 import Positiveization,Standardization,print_data,Probability_matrix,Entropy_weight
import pandas as pd
import math as ma

def Topsis_distance(data:list[list[int]]):
    copy_data = data.copy()
    for i in range(len(data[0])):
        max_x=max(data[:,i])
        min_x=min(data[:,i])
        bottom=max_x-min_x
        for row in range(len(data)):
            copy_data[row][i]=(copy_data[row][i]-min_x)/bottom
    
    return copy_data
            
def Topsis_GoodAndBad(data:list[list[int]],weight:list[list[int]]):
    max_z=[]
    min_z=[]
    res=[]
    for col in range(len(data[0])):
        max_z.append(max(data[:,col]))
        min_z.append(min(data[:,col]))
    
    for row in range(len(data)):
        positive_d=0
        negative_d=0
        for col in range(len(data[0])):
            positive_d+=(data[row][col]-max_z[col])**2 * weight[col]
            negative_d+=(data[row][col]-min_z[col])**2 * weight[col]
        res.append(ma.sqrt(negative_d)/(ma.sqrt(positive_d)+ma.sqrt(negative_d)))
    return res


#0：极大，1：极小，2：中间型(best)，3：区间型([a,b])
data_xlsx=pd.read_excel(r"D:\onedrive\电脑桌面\练习.xlsx",engine='openpyxl')
data=data_xlsx.values
init_data=data[1:,1:-1]

weight=[1,1]
flags=[0,1]
values=[[],[]]

positive_data=Positiveization(init_data,flags,values)
standard_data=Standardization(positive_data)
ans=Topsis_GoodAndBad(standard_data,weight)
print(ans)
a=sum(ans)
for i,da in enumerate(ans):
    ans[i]=da/a
    print(f'{ans[i]:.4f}',end=' ')
