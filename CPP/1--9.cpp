#include<stack>
#include<vector>
#include<iostream>

int main(void){


    std::vector<int> vec = {1, 2, 3, 4, 5};
    int last_element = vec.back(); // last_element 现在是 5
    vec.back() = 6; // 修改容器最后一个元素为 6，vec 现在是 {1, 2, 3, 4, 6}
    for(int i=0; i<vec.size();i++){
        printf("%d\n",vec[i]);
    }
    return 0;

}