#include<iostream>
#include<algorithm>
#include<vector>
const int MAXN=1e6+10;
#define Ri register int 
int a[MAXN],last[MAXN],ans[MAXN];
struct Tree{
    int l,r,sum;
}tr[MAXN<<2];

struct Node{
    int l,r,id;
    bool operator<(const Node& a) {return r<a.r;}

}q[MAXN];

inline void pushup(int x){
    tr[x].sum=tr[x<<1].sum+tr[x<<1 | 1].sum;
}

inline void build(int x,int l,int r){
    tr[x]={l,r,1};
    if(l==r) return;
    int mid=(l+r)>>1;
    build(x<<1,l,mid);
    build(x<<1 | 1,mid+1,r);
    pushup(x);
}

inline void update(int x,int index){
    if(tr[x].l==tr[x].r){
        tr[x].sum=0;
        return;
    }
    int mid=(tr[x].l+tr[x].r)>>1;
    if(index<=mid) update(x<<1,index);
    else if(index>mid) update(x<<1 | 1,index);
    pushup(x);
}

inline int query(int x,int l,int r){
    if(l>tr[x].r || r<tr[x].l) return 0;
    if(tr[x].l>=l && tr[x].r<=r){
        return tr[x].sum;
    }
    int res=0,mid;
    mid=(tr[x].l+tr[x].r)>>1;
    if(l<=mid) res+=query(x<<1,l,r);
    if(r> mid) res+=query(x<<1 | 1,l,r);
    return res;
}


int read(){
    int x=0,w=1;
    char ch=0;
    while(ch<'0' || ch>'9'){
        if(ch=='-'){
            w=-1;
        }
        ch=getchar();
    }
    while(ch>='0' && ch<='9'){
        x=x*10+(ch-'0');
        ch=getchar();
    }
    return x*w;
}

inline void write(int x){
    int sta[35];
    int top=0;
    do{
        sta[top++]=x%10;
        x/=10;
    }while(x);
    while(top) putchar(sta[--top]+'0');
}

int main(void){
    int n,m;
    n=read();
    for(register int i=1;i<=n;i++){
        a[i]=read();
    }
    m=read();
    for(register int i=1;i<=m;i++){
        q[i].l=read();
        q[i].r=read();
        q[i].id=i;
    }
    std::sort(q+1,q+m+1);

    build(1,1,n);
    int index=1;
    for(register int  i=1;i<=n;i++){
        if(last[a[i]]){
            update(1,last[a[i]]);
        }
        last[a[i]]=i;
        while(q[index].r==i){
            ans[q[index].id]=query(1,q[index].l,q[index].r);
            index++;
        }
    }
    for(register int i=1;i<=m;i++){
        write(ans[i]);
        putchar('\n');
    }
    return 0;
}