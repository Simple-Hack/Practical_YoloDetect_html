#include<vector>
#include<iostream>
#include<string>
const long long N =1e5+10;

long long p;
long long a[N];

struct node {
	long long l,r;
	long long sum,add,mul;
}tr[4*N];

inline void pushup(long long x){
	tr[x].sum=(tr[x*2].sum+tr[x*2+1].sum)%p;
}

void pushdown(long long x){
	tr[x*2].sum=(tr[x*2].sum*tr[x].mul+tr[x].add*(tr[x*2].r-tr[x*2].l+1))%p;
	tr[x*2].mul=(tr[x*2].mul*tr[x].mul)%p;
	tr[x*2].add=(tr[x*2].add*tr[x].mul+tr[x].add)%p;

	tr[x*2+1].sum=(tr[x*2+1].sum*tr[x].mul+tr[x].add*(tr[x*2+1].r-tr[x*2+1].l+1))%p;
	tr[x*2+1].mul=(tr[x*2+1].mul*tr[x].mul)%p;
	tr[x*2+1].add=(tr[x*2+1].add*tr[x].mul+tr[x].add)%p;

	tr[x].add=0;
	tr[x].mul=1;
}

void update(long long x,long long l,long long r,long long mul,long long add){
	if(l<=tr[x].l && tr[x].r<=r){
		tr[x].sum=(tr[x].sum*mul+add*(tr[x].r-tr[x].l+1))%p;
		tr[x].mul=(tr[x].mul*mul)%p;
		tr[x].add=(tr[x].add*mul+add)%p;
	}
	else{
		pushdown(x);
		long long mid=(tr[x].r+tr[x].l)/2;
		if(l<=mid){
			update(x*2,l,r,mul,add);;
		}
		if(r>mid){
			update(x*2+1,l,r,mul,add);
		}
		pushup(x);
	}
}

long long query(long long x,long long l,long long r){
	if(tr[x].l>=l && tr[x].r<=r){
		return tr[x].sum;
	}
	pushdown(x);
	long long mid=(tr[x].r+tr[x].l)/2;
	long long s=0;
	if(l<=mid){
		s+=query(x*2,l,r)%p;
	}
	if(r>mid){
		s+=query(x*2+1,l,r)%p;
	}
	return s;
}

void build(long long x,long long l,long long r){
	tr[x].add=0;
	tr[x].l=l;
	tr[x].r=r;
	tr[x].mul=1;
	if(l==r){
		tr[x].sum=a[l];
	}else{
		long long mid=(l+r)/2;
		build(x*2,l,mid);
		build(x*2+1,mid+1,r);
		pushup(x);
	}
}

int main(void){
	long long n;
	std::cin>>n>>p;
	for(long long i=1;i<=n;i++){
		std::cin>>a[i];
	}
	build(1,1,n);
	long long m;
	std::cin>>m;
	long long q,t,g;
	while(m--){
		std::cin>>q>>t>>g;
		if(q==1){
			long long c;
			std::cin>>c;
			update(1,t,g,c,0);
		}
		else if(q==2){
			long long c;
			std::cin>>c;
			update(1,t,g,1,c);
		}
		else{
			std::cout<<query(1,t,g)%p<<std::endl;
		}
	}
	return 0;
}