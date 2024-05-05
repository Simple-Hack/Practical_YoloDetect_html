#include<iostream>
#include<algorithm>
#include<cmath>
const int MAXN=1e6+114;
int array[MAXN],cnt[MAXN],belong[MAXN];
int n,m,size,bnum,now,ans[MAXN];

class query{
    public:
        int l,r,id;
}q[MAXN];

int cmp(query q1, query q2){
    return (belong[q1.l] ^ belong[q2.l]) ? belong[q1.l]<belong[q2.l] 
     :((belong[q1.l] & 1) ? q1.l<q2.l : q1.l>q2.l);
}

int read(){
    int x=0,w=1;
    char ch=getchar();
    while(ch < '0' || ch >'9'){
        if(ch == '-') w=-1;
        ch=getchar();
    }
    while('0'<= ch && ch<= '9'){
        x=x*10+ch-'0';
        ch=getchar();
    }
    return x*w;
}

void write(int x){
    static int sta[35];
    int top=0;
    do{
        sta[top++]=x%10;
        x /= 10;
    }while(x);
    while(top){
        putchar(sta[--top]+'0');
    }
}

void add(int pos){
    if(!(cnt[array[pos]]++)) now++;
}

void del(int pos){
    cnt[array[pos]]--;
    if(!cnt[array[pos]]) now--;
}

int main(void){
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    std::cin>>n;
    size=std::sqrt(n);
    bnum=int((n+size-1)/size);
    for(int i=1;i<=n;i++){
        for(int j=(i-1)*size+1;j<=i*size;j++){
            belong[j]=i;
        }
    }
    for(int i=1;i<=n;i++){
        array[i]=read();
    }
    m=read();
    for(int i=1;i<=m;i++){
        q[i].l=read();
        q[i].r=read();
        q[i].id=i;
    }
    std::sort(q+1,q+1+m,cmp);
    int l=1,r=0;
    for(int i=1;i<=m;i++){
        int ql=q[i].l,qr=q[i].r;
        while(l<ql) del(l++);
        while(l>ql) add(--l);
        while(r<qr) add(++r);
        while(r>qr) del(r--);
        ans[q[i].id]=now;
    }
    for(int i=1;i<=m;i++){
        write(ans[i]);
        putchar('\n');
    }
    return 0;
}