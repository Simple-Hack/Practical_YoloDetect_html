#include<iostream>

int main(void){
    int a=4;
    a+=a-=a*a;
    std::cout<<a<<std::endl;
    return 0;
}