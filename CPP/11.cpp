#include<bits/stdc++.h>
#define pi acos(-1.0)
using namespace std;
struct node{
    double x,y;
}a[200005];
int n;
double ans=1e15;//初始化答案

bool cmp(node a,node b){
    return a.x<b.x;//按照横坐标排序 
}
double dis(node a,node b){
    return sqrt((a.x-b.x)*(a.x-b.x)+(a.y-b.y)*(a.y-b.y));//计算两点之间距离 
}
void calc(){
    for (int i=1;i<=n;i++)
        for (int j=i+1;j<=i+5&&j<=n;j++)
            ans=min(ans,dis(a[i],a[j]));
}
void around(double ds){
    ds=ds/180.0*pi;//角度转换为弧度 
    for (int i=1;i<=n;i++){
        double x=a[i].x,y=a[i].y;//旋转前的点 
        double xn,yn;//旋转后的点 
        double xyu=0.0,yyu=0.0;  //旋转中心 
        xn=(x-xyu)*cos(ds)-(y-yyu)*sin(ds)+xyu;
        yn=(x-xyu)*sin(ds)+(y-yyu)*cos(ds)+yyu;
        a[i].x=xn,a[i].y=yn;
    }
    sort(a+1,a+1+n,cmp);//排序 
    calc();//计算 
}

int main(){
    srand(time(NULL));
    scanf("%d",&n);
    for (int i=1;i<=n;i++){
        scanf("%lf%lf",&a[i].x,&a[i].y);
    }
    around(0);//将原图像进行排序并枚举每个点与其后五个点比较 
    around(rand()%360);//将图像随机（0°~359°）旋转  并排序 计算 
    around(rand()%360);//将图像随机（0°~359°）旋转  并排序 计算 
    printf("%.4lf\n",ans);
    return 0;
}