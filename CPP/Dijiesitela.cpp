#include <iostream>
#include<cstring>
#include <cstdio>
#define MAXSIZE 20
#define MAX 65535

// 定义全局变量，表示顶点数量和根节点索引，以及距离数组和访问标志数组
int length = 0;
int root = 0;
int rootDist[MAXSIZE];
bool visit[MAXSIZE];

// 定义图结构体，包含顶点数组和权值矩阵
typedef struct {
    char vertex[MAXSIZE]; // 存储顶点字符的数组
    int weight[MAXSIZE][MAXSIZE]; // 权重矩阵，用于存储顶点之间的权值
} Graph;

Graph G; // 图G实例

// 输入顶点函数，从用户处获取并存储顶点信息
void InputVertex(Graph& G) {
    int i;
    char ch;
    int len;
    
    std::cout << "InputVertex nums:" << std::endl;
    std::cin >> len;
    
    std::cout << "输入图的顶点" << std::endl;
    for (i = 0; i < len; i++) {
        std::cout << "第" << i + 1 << "个：" << std::endl;
        std::cin >> ch;
        if (ch == ' ') { // 如果读取到空格，则结束输入顶点
            break;
        }
        G.vertex[i] = ch; // 将读取的字符存入顶点数组
    }
    length = i; // 更新实际顶点数
}

// 初始化图的权重矩阵，将对角线设置为0，其余位置初始化为最大值
void GraphWeightInit(Graph& G) {
    for (int i = 0; i < length; i++) {
        for (int j = 0; j < length; j++) {
            if (i == j) {
                G.weight[i][j] = 0; // 自环权重设为0
            } else {
                G.weight[i][j] = MAX; // 非自环权重初始设为最大值
            }
        }
    }
}

// 查找指定字符对应的顶点在数组中的索引
int FindIndex(char ch) {
    int i;
    for (i = 0; i < length; i++) {
        if (G.vertex[i] == ch) {
            return i;
        }
    }
    return -1; // 若未找到，则返回-1
}

// 创建邻接矩阵，从用户处获取边及其权值
void CreatGraph() {
    int i, j, index, weight;
    char ch;

    for (i = 0; i < length; i++) {
        std::cout << "输入" << G.vertex[i] << "的邻接矩阵的顶点和权值（空格分隔，换行结束）" << std::endl;
        std::cin >> ch;
        
        while (ch != '\n') {
            while (ch == ' ') {
                std::cin >> ch;
                // continue; // 不需要继续，因为已经在循环中处理了空格
            }
            
            index = FindIndex(ch);
            std::cin >> weight;
            while (weight == ' ') {
                std::cin >> weight;
                // continue; // 不需要继续，因为已经在循环中处理了空格
            }
            
            G.weight[index][i]=G.weight[i][index] = weight; // 无向图，所以双向赋值
            
            ch = getchar(); // 获取下一个字符，跳过换行符
        }
    }
}

// 初始化最短路径算法所需的数据结构，包括根节点的距离数组和访问标志数组
void Init() {
    int i;
    
    std::cout << "输入根节点" << std::endl;
    std::cin >> root;
    
    for (i = 0; i < length; i++) {
        rootDist[i] = G.weight[root][i]; // 计算所有顶点到根节点的初始距离
        visit[i] = false; // 初始化所有顶点为未访问状态
    }
}

// 获取未访问顶点中具有最小距离的顶点索引
int GetMinInVisit() {
    int i, min = 0;
    
    for (i = 0; i < length; i++) {
        if (!visit[i]) {
            if (rootDist[min] > rootDist[i] || rootDist[min] == 0) {
                min = i;
            }
        }
    }
    return min;
}

// 检查所有顶点是否已被访问
bool IsNull() {
    bool flag = true;
    for (int i = 0; i < length; i++) {
        if (!visit[i]) {
            flag = false;
        }
    }
    return flag;
}

// 使用迪杰斯特拉算法计算以root为起点的最短路径
void Dijkstra(int index) {
    int i;
    
    visit[index] = true; // 标记当前顶点已访问
    std::cout << G.vertex[index] << "   " << rootDist[index] << std::endl; // 输出当前顶点及其距离
    
    // 更新相邻顶点的距离
    for (i = 0; i < length; i++) {
        if (rootDist[i] > (rootDist[index] + G.weight[index][i])) {
            rootDist[i] = rootDist[index] + G.weight[index][i];
        }
    }
    
    // 如果所有顶点都被访问，则结束算法
    if (IsNull()) {
        return;
    }

    // 选择未访问顶点中距离最小的顶点进行下一轮迭代
    index = GetMinInVisit();
    Dijkstra(index);
}

// 打印邻接矩阵的所有非零权值
void print() {
    for (int i = 0; i < length; i++) {
        std::cout << G.vertex[i] << "邻接节点：" << std::endl;
        for (int j = 0; j < length; j++) {
            if (G.weight[i][j] != 0 && G.weight[i][j] != MAX) {
                std::cout << G.vertex[j] << G.weight[i][j] << std::endl;
            }
        }
    }
}

int main() {
    InputVertex(G); // 输入顶点
    GraphWeightInit(G); // 初始化图的权重矩阵
    CreatGraph(); // 创建邻接矩阵
    Init(); // 初始化最短路径算法数据
    Dijkstra(root); // 运行迪杰斯特拉算法

    print(); // 打印邻接矩阵非零权值

    return 0;
}