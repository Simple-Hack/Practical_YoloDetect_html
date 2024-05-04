//牛马题,数据最大能到2的100次方.
#include<vector>
#include<iostream>
#include<string>
#include<algorithm>
const int N =1e6+10;
int a[N];

struct node {
	long long add,after_number;
	long long l,r;
	long long max_number;
}tr[N*4];


inline void pushup(int x){
	tr[x].max_number = std::max(tr[x*2].max_number,tr[x*2+1].max_number);
}

void build(int x,long long l,long long r){
	tr[x].l = l;
	tr[x].r = r;
	tr[x].add=0;
	if(l<=tr[x].l && tr[x].r<=r){
		tr[x].after_number = a[l];
		tr[x].max_number = a[l];
		return;
	}
	long long mid=(l+r)/2;
	build(x*2,l,mid);
	build(x*2+1,mid+1,r);
	pushup(x);
}

void update(int x,long long l,long long r,long long after_number,long long add){
		if(l<=tr[x].l && tr[x].r<=r){
			tr[x].max_number+=add;
			
			return ;
		}
		long long mid=(tr[x].r+tr[x].l)/2;
		if(l<=mid) update(x*2,l,r,after_number,add);
		if(r>mid)  update(x*2+1,l,r,after_number,add);
		pushup(x);
}
int main(void){

	return 0;
}