import openpyxl
import math

workbook = openpyxl.Workbook()
worksheet = workbook.active

distance = [0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1]
for i in range(len(distance)):
    distance[i] = distance[i] * 1852
angle = [0, math.pi / 4, math.pi / 2, math.pi * 3 / 4, math.pi, math.pi * 5 / 4, math.pi * 3 / 2, math.pi * 7 / 4]
original_D = 120
alpha = 1.5 * math.pi / 180
beta = 120 * math.pi / 180
sei_ta = 2 * math.pi / 3

def cal_gama(alp, bet):
    gama = math.atan(math.tan(alp) * math.sin(bet))
    return gama

row = 1
for ang in angle:
    col = 1
    for dis in distance:
        gama = cal_gama(alpha, ang)
        D = original_D + dis * math.tan(alpha) * math.cos(ang)
        W = D * math.sin(sei_ta / 2) * (1 / math.cos(sei_ta / 2 + gama) + 1 / math.cos(sei_ta / 2 - gama))
        worksheet.cell(row=row, column=col).value = f'{W:.2f}'
        col += 1
    row += 1

workbook.save("output.xlsx")