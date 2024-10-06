import math
sei_ta = 2*math.pi/3
alpha_1=0.008471924589085633
alpha_2=0.008480735721641814
alpha_3=0.011878523269372773
alpha_4=0.002441995130245888
alpha_5=0.014037973141299983
alpha_6=0.033249036801760126
def cal_W(sei_ta,alpha,former_D,d, index):
    D = former_D - d * math.tan(alpha)
    if index == 1:
        return D * math.sin(sei_ta/2) / math.cos(sei_ta/2 + alpha)
    else:
        return D * math.sin(sei_ta/2) / math.cos(sei_ta/2 - alpha)

def cal(index1,index2,alpha1,alpha2,D1,D2,former_2,back_1,back_2,len_1,len_2):
    W2=cal_W(sei_ta,alpha1,D1,former_2*math.cos(alpha1),2)
    result_1=-(len_1/2)/math.cos(alpha1)*1852+W2+former_2
    重叠率=result_1/(cal_W(sei_ta,alpha2,D2,back_1*math.cos(alpha2),1)+cal_W(sei_ta,alpha2,D2,back_1*math.cos(alpha2),2))
    if result_1>0:
        print(f'区域{index1}未漏测,与区域{index2}重叠率为:{重叠率}')
    else:
        print(f'区域{index1}漏测{abs(result_1)}米')
    result_2=(-len_2/2/math.cos(alpha2))*1852+back_2+cal_W(sei_ta,alpha2,D2,back_2*math.cos(alpha2),2)
    if result_2>0:
        print(f'区域{index2}未漏测')
    else:
        print(f'区域{index2}漏测{abs(result_2)}米')
    return result_1,result_2


res_1,_=cal(1,2,alpha_1,alpha_2,74.99469383849981,53.381320917806065,373.96280743024556,-1732.3327140442464,1811.916036147846,0.5,2)
res_2,_=cal(2,4,alpha_2,alpha_4,53.381320917806065,24.394733893557422,1811.916036147846,-2262.95527395032,2290.417370868393,2,2.5)
#3号去最后一个
#倒数第六个
res_3,_=cal(3,5,alpha_3,alpha_5,76.91331140350877,41.74538429406851,1354.6606972844043,-1282.9127132985072,1352.7708490617877,1.5,1.5)
#倒数第四个 
res_4,_=cal(6,5,alpha_6,alpha_5,108.74402944241791,41.74538429406851,1366.0295588016102,-1282.9127132985072,1352.7708490617877,1.5,1.5)

#print(f'漏测占比为:{(((abs(res_1)/1852) * 2)/(20))*100}%')

