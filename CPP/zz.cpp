#include<iostream>
#include<memory>
#include<algorithm>
#include<cmath>
#include<vector>

const int N=114514;
std::vector<int> prefix_function(std::string s){
    int n=static_cast<int>(s.length());
    std::vector<int> pi(n);
    for(int i=1;i<n;i++){
        for(int j=i;j>=0;j--){
            if(s.substr(0,j)==s.substr(i-(j-1),j)){
                pi[i]=j;
                break;
            }
        }
    }
    return pi;
}

void f(int&c){

}

void sub(void){
    int &a=const_cast<int&>(N);
    f(a);
    std::cout<<"N is a int number  "<<a<<std::endl;

}
int main(){
    sub();
    return 0;
}