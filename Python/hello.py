g=[0 for i in range(11451)]
color=[0 for i in range(11451)]
vis=[1 for i in range(11451)]
stack=[0 for i in range(11451)]
dfn=[0 for i in range(11451)]
low=[0 for i in range(11451)]
cnt=[0 for i in range(11451)]

#deep:节点编号 top：栈顶  sum：强连通分量数目
deep=0
summ=0
top=0
res=0

def tarjan(v :int):
    deep+=1
    dfn[v]=deep
    vsi[v]=True
    top+=1
    stack[top]=v


    for i in range(0,g[v].size()):
        id=g[v][i]

        if not dfn[id]:
            tarjan(id)
            low[v]=min(low[v],low[id])

        else:
            if vis[id]:
                low[v]=min(low[v],low[id])

    if low[v]==dfn[v]:
        summ+=1
        color[v]=summ
        vis[v]=0
        while stack[top]!=v:
            color[stack[top]]=summ
            
            vis[stack[top]]=0
            top-=1
        top-=1


    