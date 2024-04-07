#include<string.h>
#include<iostream>
#include <unordered_map>


int main(){
    std::unordered_map<int,std::string> map;
    map[114]="Ikun";
    map[514]="Six";
    map[1919]="HeiZi";
    std::string name =map[114];
    std::cout << "The name for key 114 is: " << name << std::endl;
    std::cout<<"\n";
    for(auto kk:map){
        std::cout<<kk.first<<" -> "<<kk.second<<std::endl;
    }
    map.erase(514);

    for(auto iter=map.begin();iter!=map.end();++iter){
        std::cout<<iter->first<<" -> "<<iter->second<<std::endl;

    }
    return 0;
}

