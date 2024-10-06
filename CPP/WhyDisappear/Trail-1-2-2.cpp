#include<iostream>
#include<string>

int main( ) {
    std::string s;
    std::cin >> s;
    int len = s.size( );
    int DFA[4][3] = { {1,2,0},{1,3,0},{2,2,0},{3,3,3} };
    int curState = 0;
    
    for (int ind = 0;ind < len;ind++) {
        if(s[ind]>='0' and s[ind]<='9'){
            curState=DFA[curState][0];
        }
        else if ((s[ind] >= 'a' and s[ind] <= 'z') or (s[ind] >= 'A' and s[ind] <= 'Z')) {
            curState=DFA[curState][1];
        }
        else if(s[ind]==' '){
            curState=DFA[curState][2];
        }
        else {
            curState = 3;
            break;
        }
    }
    if (curState != 3) {
        std::cout << "Accepted" << std::endl;
    }
    else {
        std::cout << "Rejected" << std::endl;
    }

}
