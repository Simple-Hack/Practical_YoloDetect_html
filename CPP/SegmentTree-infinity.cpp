#include<iostream>
#include<algorithm>

const int N=1e4+10;
struct node{
    int sum,add;
    int l,r;
}tr[N*4];

int a[N];

void pushup(int x){
    tr[x].sum=tr[x*2].sum+tr[x*2+1].sum;
}

void build(int x,int l,int r){
    tr[x].l=l;tr[x].r=r;
    if(l==r){
        tr[x].sum=a[l];
        tr[x].add=0;
        return ;
    }
    int mid=(l+r)/2;
    build(x,mid,l);
    build(x,mid+1,r);
    pushup(x);
}

void update(int x,int l,int r,int k){
    tr[x].sum+=(std::min(tr[x].r,r)-std::max(tr[x].l,l));
    if(l<=tr[x].l && tr[x].r<=r){
        tr[x].add+=k;
        return;
    }
    int mid=(tr[x].r+tr[x].l)/2;
    if(l<=mid){
        update(x*2,l,r,k);
    }
    if(r>mid){
        update(x*2+1,l,r,k);
    }
}

int query(int x,int l,int r,int k){
    if(l<=tr[x].l && tr[x].r<=r){
        int s=(tr[x].r-tr[x].l+1)*k;
        return tr[x].sum+s;
    }
    k+=tr[x].add;
    int mid=(tr[x].r+tr[x].l)/2;
    int sum=0;
    if(l<=mid){
        sum+=query(x*2,l,r,k);
    }
    if(r>mid){
        sum+=query(x*2+1,l,r,k);
    }
    return sum;
}

