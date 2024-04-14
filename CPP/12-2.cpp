#include<iostream>
#include<vector>
const int N=1e6;
int a[N];
struct Node{
    int r,l,sum;
}tr[4*N+1];

void pushup(int x){
    tr[x].sum=tr[x*2].sum+tr[x*2+1].sum;
}

void build(int x,int l, int r){
    tr[x].l=l; tr[x].r=r;
    if (tr[x].l==tr[x].r){
        tr[x].sum=a[l];
        return ;
    }
    int mid=(l+r)/2;
    build(x*2,l,mid);
    build(x*2+1,mid+1,r);
    pushup(x);
}

int query(int x,int l,int r){
    if(tr[x].l>=l && tr[x].r<=r){
        return tr[x].sum;
    }
    int sum=0;
    int mid=(tr[x].l+tr[x].r)/2;
    if(l<=mid){
        sum+=query(x*2,l,r);
    }
    if(r>mid){
        sum+=query(x*2+1,l,r);
    }
    return sum;
}

void change(int now,int x,int k){
    if (tr[now].l==tr[now].r){
        tr[now].sum+=k;
        return;
    }
    int mid=(tr[now].l+tr[now].r)/2;
    if (x<=mid){
        change(now*2,x,k);
    }else{
        change(now*2+1,x,k);
    }
    pushup(now);
}

int main(){
    int n,m;
    std::cin>>n>>m;
    build(1,1,n);
    for(int i=1;i<n+1;i++){
        std::cin>>a[i];
    }
    while(--m){
        int op,r,l;
        std::cin>>op>>r>>l;
        if(op==1){
            change(1,r,l);
        }else{
            std::cout<<query(1,r,l)<<std::endl;
        }
    }

    return 0;
}