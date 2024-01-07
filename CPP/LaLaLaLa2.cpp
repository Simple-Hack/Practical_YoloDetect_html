#include<iostream>
#include <iomanip>
// 函数模板定义：一个通用的加法函数
template <typename T>
T add(T a, T b) {
    return a + b;
}

int main(void){
    //
    int sum_a_b=add(233,233);
    double sum_A_B=add(233.0,233.0);
    std::cout <<"基于模板实现的a+b整型结果: "<<sum_a_b << std::endl;
    std::cout <<"基于模板实现的A+B整型结果: "<< std::fixed << std::setprecision(8) <<sum_A_B << std::endl;
    

    
    //
    return 0;
}