#include<iostream>
#include<string>
#include<memory>
#include <string.h>
#define MAN 114
int a[10][10];

void find_largest_number_of_two_strings(const std::string& s1, const std::string& s2) {
    int len_s1 = s1.size();
    int len_s2 = s2.size();

    memset(a, 0, sizeof(a));

    for (int i = 1; i <= len_s1; i++) { 
        for (int j = 1; j <= len_s2; j++) { 
            if (i > len_s1 || j > len_s2) { 
                continue;
            }
            if (s1[i] == s2[j]) {
                a[i][j] = a[i - 1][j - 1] + 1;
            } else {
                a[i][j] = std::max(a[i - 1][j], a[i][j - 1]);
            }
        }
    }
}

int main() {

    std::string s1, s2;
    std::cin >> s1;
    std::cin >> s2;
    find_largest_number_of_two_strings(s1, s2);
    std::cout << a[s1.size()][s2.size()] << std::endl;
    for(auto it :a){
        std::cout<<*it<<std::endl;
    }

    return 0;
}