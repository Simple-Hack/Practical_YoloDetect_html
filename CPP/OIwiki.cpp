#include<bits/stdc++.h> 

using namespace std;
const int N=114;
int a[N];
int ans[N];
int sum=0;
bool vis[N]={false};
int cnt=0;
int read(){
    int w=1,x=0;
    char c=0;
    while(!isdigit(c)){
        if(c=='-'){
            w=-1;
        }
        c=getchar();
    }
    while(isdigit(c)){
        x=x*10+c-48;
        c=getchar();
    }
    return w*x;
}
int main( )
{   
    a[0]=1e9+10;
    int out=0;
    int n;
    n=read();
    a[n+1]=1e9+10;

    for(int i=1;i<=n;i++) a[i]=read();
    int index=1;
    while(index<=n+1){
        while(a[index]<a[index-1] && index<=n) index++;
        int head=index-1,tail=index;
        while(a[tail]>a[head]){
            if(vis[head]){
                head--;continue;
            }
            sum+=tail-head-1;
            vis[head]=1;
            head--;
            if(++cnt>=n) break;
        }
        index++;
    }
    cout<<sum<<endl;
    return 0;
}