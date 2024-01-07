#include <iostream>
#define MAXSIZE 20
#define MAX 65535
int length=0;
int root=0;
int rootDist[MAXSIZE];
bool visit[MAXSIZE];

typedef struct{
    char vertex[MAXSIZE];
    int weight[MAXSIZE][MAXSIZE];
}Graph;

Graph G;

void InputVertex(Graph& G){
    int i;
    char ch;
    std::cout<<"InputVertex: "<<G.vertex<<std::endl;
    
    ch='A';
    for(i=0;i<9 && ch!='\0';i++){
        G.vertex[i]=ch;
        ch++;
    }
    length=9;
}

void GraphWeightInit(Graph& G){
    for(int i=0;i<length;i++){
        for(int j=0;j<length;j++){
            if(i==j){
                G.weight[i][j]=0;
            }
            else{
                G.weight[i][j]=MAX;
            }
        }
    }
}

int FindIndex(char ch){
    int i;
    for(i=0;i<length;i++){
        if(G.vertex[i]==ch){
            return i;
        }
    }
    return -1;
}

void CreatGraph(){
    int i,j,index,weight;
    char ch;
    for(i=0;i<length;i++){
        std::cout<<"输入"<<G.vertex[i]<<"的邻接矩阵的顶点和权值（空格分隔，换行结束）"<<std::endl;
        std::cin>>ch;
        while (ch != '\n'){
            while(ch==' '){
                std::cin>>ch;
                //continue;
            }
            index=FindIndex(ch);
            std::cin>>weight;
            while(weight==' '){
                std::cin>>weight;
                //
                continue;
            }
            G.weight[i][index]=weight;
            std::cin>>ch;
        }
    }

}


void Init(){
    int i;
    std::cout<<"输入根节点"<<std::endl;
    std::cin>>root;
    for(i=0;i<length;i++){
        rootDist[i]=G.weight[root][i];
        visit[i]=false;
    }
}

int GetMinInVisit(){
    int i,min=0;
    for(i=0;i<length;i++){
        if(!visit[i]){
            if(rootDist[min]>rootDist[i] || rootDist[min]==0){
                min=i;
            }
        }
    }
    return min;
}

bool IsNull(){
    bool flag=true;
    for(int i=0;i<length;i++){
        if(!visit[i]){
            flag=false;
        }
    }
    return flag;
}

void Dijkstra(int index){
    int i;
    visit[index]=true;
    std::cout<<G.vertex[index]<<rootDist[index]<<std::endl;
    for(i=0;i<length;i++){
        if(rootDist[i]>(rootDist[index]+G.weight[index][i])){
            rootDist[i]=rootDist[index]+G.weight[index][i];
        }
    }
    if(IsNull()){
        return ;
    }
    index=GetMinInVisit();
    Dijkstra(index);
}
void print(){
    for(int i=0;i<length;i++){
        std::cout<<G.vertex[i]<<"邻接节点："<<std::endl;
        for(int j=0;j<length;j++){
            if(G.weight[i][j]!=0 && G.weight[i][j]!=MAX){
                std::cout<<G.vertex[j]<<G.weight[i][j]<<std::endl;      
            }
        }
    }
}

int main(){
    InputVertex(G);
    GraphWeightInit(G);
    CreatGraph();
    Init();
    Dijkstra(root);

    print();
    return 0;
}