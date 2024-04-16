#include<iostream>

const int N=1e5+10;

struct node{
    long long l,r,sum,add,mul;
}tr[4*N];

int a[N];
int n,p,m;

void pushup(int x){
    tr[x].sum=(tr[x*2].sum+tr[x*2+1].sum)%p;
}

void eval(int x,long long add,long long  mul){

    tr[x].sum=(tr[x].sum*mul +add*(tr[x].r-tr[x].l+1))%p;
    tr[x].mul=(tr[x].mul*mul)%p;
    tr[x].add=(tr[x].add*mul+add)%p;
}

void pushdown(int x){
    eval(x*2,tr[x].add,tr[x].mul);
    eval(x*2+1,tr[x].add,tr[x].mul);
    tr[x].mul=1;
    tr[x].add=0;
}

void build(long long  x,long long  l,long long  r){
    tr[x].l=l;
    tr[x].r=r;
    tr[x].add=0;
    tr[x].mul=1;
    if(l==r){
        tr[x].sum=a[l];
        return ;
    }
    long long mid=(r+l)/2;
    build(x*2,l,mid);
    build(x*2+1,mid+1,r);
    pushup(x);
}


void change(int x,long long  l,long long  r,long long add,long long  mul){
    if(l<=tr[x].l && r>=tr[x].r){
        eval(x,add,mul);
    }else{
        pushdown(x);//asdfdasffasdfds
        long long  mid=(tr[x].r+tr[x].l)/2;
        if(l<=mid){
            change(x*2,l,r,add,mul);
        }
        if(r>mid){
            change(x*2+1,l,r,add,mul);
        }
        //这里如果eval之后不能执行这个哦
        pushup(x);
    }
    
}

long long query(int x,long  long l,long long  r){
    if(l<=tr[x].l && tr[x].r<=r){
        return tr[x].sum;
    }
    pushdown(x);
    long long  s=0;
    int mid=(tr[x].r+tr[x].l)/2;
    if(l<=mid){
        s+=query(x*2,l,r);
    }
    if(r>mid){
        s+=query(x*2+1,l,r);
    }
    return s;
}

int main(){
    int t,g,c,ch;
    std::cin>>n>>m>>p;
    for(int i=1;i<=n;i++){
        std::cin>>a[i];
    }
    build(1,1,n);
    while(m--){
        std::cin>>ch>>t>>g;
        if(ch==1){
            std::cin>>c;
            change(1,t,g,0,c);
        }
        else if(ch==2){
            std::cin>>c;
            change(1,t,g,c,1);
        }else{
            std::cout<<query(1,t,g)%p<<std::endl;
        }
    }
    return 0;
}