import numpy as np
import matplotlib.pyplot as plt # 导入 Matplotlib 工具包
import networkx as nx  # 导入 NetworkX 工具包

# 3. 最小费用最大流问题（Minimum Cost Maximum Flow，MCMF）
# 创建有向图
G3 = nx.DiGraph()  # 创建一个有向图 DiGraph
G3.add_edges_from([('s','v1',{'capacity': 15, 'weight': 8}),
                  ('s','v2',{'capacity': 10, 'weight': 10}),
                  ('s','v3',{'capacity': 20, 'weight': 15}),
                  ('v1','v4',{'capacity': 7, 'weight': 9}),
                  ('v1','v5',{'capacity': 10, 'weight': 11}),
                  ('v2','v5',{'capacity': 8, 'weight': 8}),
                  ('v2','v6',{'capacity': 2, 'weight': 6}),
                  ('v3','v6',{'capacity': 18, 'weight': 14}),
                  ('v4','t',{'capacity': 6, 'weight': 8}),
                  ('v5','t',{'capacity': 16, 'weight': 9}),
                  ('v6','t', {'capacity': 20, 'weight': 10})
                ]) # 添加边的属性 'capacity', 'weight'

# 求最小费用最大流
minCostFlow = nx.max_flow_min_cost(G3, 's', 't')  # 求最小费用最大流
minCost = nx.cost_of_flow(G3, minCostFlow)  # 求最小费用的值
maxFlow = sum(minCostFlow['s'][j] for j in minCostFlow['s'].keys())  # 求最大流量的值

# # 数据格式转换
edgeLabel1 = nx.get_edge_attributes(G3,'capacity')  # 整理边的标签，用于绘图显示
edgeLabel2 = nx.get_edge_attributes(G3,'weight')
edgeLabel={}
for i in edgeLabel1.keys():
    edgeLabel[i]=f'({edgeLabel1[i]:},{edgeLabel2[i]:})'  # 边的(容量，成本)
edgeLists = []
for i in minCostFlow.keys():
    for j in minCostFlow[i].keys():
        edgeLabel[(i, j)] += ',f=' + str(minCostFlow[i][j])  # 将边的实际流量添加到 边的标签
        if minCostFlow[i][j]>0:
            edgeLists.append((i,j))

# 绘制图形
pos = nx.spring_layout(G3,k=1)  # 设置节点的位置布局
# 绘制节点
nx.draw_networkx_nodes(G3, pos, node_color='lightblue', node_size=500)
# 绘制边
nx.draw_networkx_edges(G3, pos, edgelist=edgeLists, edge_color='gray')
# 绘制节点标签
nx.draw_networkx_labels(G3, pos, font_size=10, font_family='sans-serif')
# 绘制边的标签，包含容量、重量和实际流量
edge_labels={}
for k, v in minCostFlow.items():
    for kk, vv in v.items():
        if (k, kk) in edge_labels:
            edge_labels[k, kk] = str(edge_labels[k, kk]) + f', f={vv}'
        else:
            edge_labels[k, kk] = f'({G3.edges[k, kk]["capacity"]},{G3.edges[k, kk]["weight"]}), f={vv}'

nx.draw_networkx_edge_labels(G3, pos, edge_labels=edge_labels, rotate=False, font_size=8)
plt.axis('off')  # 不显示坐标轴
plt.title(f'Minimum Cost Maximum Flow Visualization\nminCost={minCost} maxFlow={maxFlow}')
plt.show()
