import pandas as pd
import math as ma
#正向化
def Positiveization(data:list[list[int]],flags:list[int],values:list[list[int]]) ->list[list[int]]:
    copy_data=data.copy()
    for i in range(len(flags)):
        cur_data = data[:,i]
        if flags[i] == 0:
            continue
        elif flags[i] == 1:
            max_data = max(cur_data)
            for row in range(len(cur_data)):
                copy_data[row][i]=max_data-copy_data[row][i]
        elif flags[i] == 2:
            mid=[]
            best=values[i][0]
            for row in range(len(cur_data)):
                mid.append(abs(copy_data[row][i]-best))
            M=max(mid)
            for row in range(len(cur_data)):
                copy_data[row][i]=1-(abs(copy_data[row][i]-best)/M)
        elif flags[i] == 3:
            min_x=min(cur_data)
            max_x=max(cur_data)
            left,right=values[i]
            M=max(left-min_x,max_x-right)
            for row in range(len(cur_data)):
                x=copy_data[row][i]
                if x < left:
                    copy_data[row][i]=1-(left-x)/M
                elif x>=left and x<=right:
                    copy_data[row][i]=1
                else:
                    copy_data[row][i]=1-(x-right)/M
    return copy_data
#标准化
def Standardization(data:list[list[int]]):
    copy_data = data.copy()
    for col in range(len(data[0])):
        sum_x=0
        for row in range(len(data)):
            sum_x+=data[row][col]*data[row][col]
        bottom=ma.sqrt(sum_x)
        for row in range(len(data)):
            copy_data[row][col]=copy_data[row][col]/bottom
    return copy_data
#打印数据
def print_data(data:list[list[int]]):
    for row in range(len(data)):
        for col in range(len(data[0])):
            print(f'{data[row][col]:.4f}',end=' ')
        print('\n')
    print('\n')
#概率结果
def Probability_matrix(data:list[list[int]]):
    copy_data=data.copy()
    for col in range(len(data[0])):
        x_sum=0
        for row in range(len(data)):
            x_sum+=data[row][col]
        for row in range(len(data)):
            copy_data[row][col]=copy_data[row][col]/x_sum
    return copy_data
#熵权结果
def Entropy_weight(data:list[list[int]]):
    e_list=[]
    for col in range(len(data[0])):
        sum_p=0
        for row in range(len(data)):
            if data[row][col]==0:
                continue
            else:
                sum_p+=data[row][col]*ma.log(data[row][col])
        e_list.append(sum_p*(-1/ma.log(len(data))))
    d_list=e_list.copy()
    for i,d in enumerate(d_list):
        d_list[i] = 1-d
    ans=[]
    for d in d_list:
        ans.append(d/sum(d_list))
    return ans

def calculate_weight():
    data_xlsx=pd.read_excel(r"D:\onedrive\电脑桌面\练习.xlsx",engine='openpyxl')
    data=data_xlsx.values
    init_data=data[:,1:]
    print(data)
    flags=[1,2,3,0,0]
    values=[[],[180],[80,90],[],[]]
    positive_data=Positiveization(init_data,flags,values)
    standard_data=Standardization(positive_data)
    probal_data=Probability_matrix(standard_data)
    weight_data=Entropy_weight(probal_data)
    for i,data in enumerate(weight_data):
        print(f'{data:.4f}',end=' ')
        weight_data[i]=float(f'{data:.4f}')
    return weight_data

# calculate_weight()




