#include<iostream>

const int N = 1e6;

struct node{
    int l,r;
    long long sum;
    int add;
}tr[N*4];

int a[N];

inline void pushup(int x){
    tr[x].sum=tr[x*2].sum+tr[x*2+1].sum;
}

void pushdown(int x){
    if(tr[x].add){
        tr[x*2].add+=tr[x].add;
        tr[x*2+1].add+=tr[x].add;
        tr[x*2].sum+=tr[x].add*(tr[x*2].r-tr[x*2].l+1);
        tr[x*2+1].sum+=tr[x].add*(tr[x*2+1].r-tr[x*2+1].l+1);

        tr[x].add=0;
    }

}
void build(int x,int l,int r){
    tr[x].r=r;
    tr[x].l=l;
    tr[x].add=0;
    if(r==l){
        tr[x].sum=a[l];
        return ;
    }
    int mid=(l+r)/2;
    build(2*x,l,mid);
    build(2*x+1,mid+1,r);
    pushup(x);
}

long long query(int x,int l,int r){
    if(tr[x].l>=l && tr[x].r<=r){
        return tr[x].sum;
    }
    pushdown(x);
    long long s=0;
    int mid=(tr[x].l+tr[x].r)/2;
    if(l<=mid){
        s+=query(x*2,l,r);
    }
    if(r>mid){
        s+=query(x*2+1,l,r);
    }
    return s;
}

void update(int now,int l,int r,int k){
    if(tr[now].l>=l && tr[now].r<=r){
        //一定要先修改再标记！！！
        tr[now].sum+=k*(tr[now].r-tr[now].l+1);
        tr[now].add+=k;
        return;
    }
    pushdown(now);
    int mid=(tr[now].r+tr[now].l)/2;

    if(l<=mid){
        update(now*2,l,r,k);
    }
    if(r>mid){
        update(now*2+1,l,r,k);
    }
    pushup(now);
}

int n,q;
int main(void){
    std::cin>>n>>q;
    for(int i=1;i<=n;i++){
        std::cin>>a[i];
    }
    build(1,1,n);
    while(q--){
        int s,l,r;
        std::cin>>s>>l>>r;
        if(s==1){
            int k;
            std::cin>>k;
            update(1,l,r,k);
        }else{
            std::cout<<query(1,l,r)<<std::endl;
        }
    }

    return 0;
}