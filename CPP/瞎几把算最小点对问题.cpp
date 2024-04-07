#include<iostream>
#include<math.h>
#include<bits/stdc++.h>
#include<algorithm>
double pi=std::acos(-1.0);
double ans=1e10;

struct Node{
    double x;
    double y;
}no[114514];

bool cmp(Node xn,Node yn){
    return xn.x < yn.x;
}

double dis(struct Node node_1, struct Node node_2){
    return sqrt(pow((node_1.x - node_2.x),2) + pow((node_1.y - node_2.y),2));
}
double min(double x,double y){
    if(x <= y){
        return x;
    }
    return y;
}
void calc(int n){
    for(int i=0;i<n;i++)
        for(int j=i+1;j<n && j<i+6;j++){
            ans=min(ans,dis(no[i],no[j]));
        }
}

void around(double ds,int n){
    ds=(ds/180.0) * pi;
    for (int i=1;i<=n;i++){
        double x=no[i].x,y=no[i].y;//旋转前的点 
        double xn,yn;//旋转后的点 
        double xyu=0.0,yyu=0.0;  //旋转中心 
        xn=(x-xyu)*cos(ds)-(y-yyu)*sin(ds)+xyu;
        yn=(x-xyu)*sin(ds)+(y-yyu)*cos(ds)+yyu;
        no[i].x=xn,no[i].y=yn;
    }    
    std::sort(no,no+n,cmp);
    calc(n);
}

int main(void){
    srand(time(NULL));
    int n;
    scanf("%d",&n);
    for(int i=0;i<n;i++){
        double x,y;
        scanf("%lf %lf",&x,&y);
        no[i].x=x;
        no[i].y=y;
    }
    around(0.0,n);
    around(rand()%360,n);
    around(rand()%360,n);
    printf("%f",ans);


    return 0;
}