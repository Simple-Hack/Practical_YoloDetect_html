#include <iostream>
#include<fstream>
#include <ostream>
#define BUFFER_SIZE 1024

void fread_copy_file(const std::string& source, const std::string& destination, size_t buffer_size){
    std::ifstream file_in(source, std::ios::binary);
    std::ifstream file_out(destination, std::ios::binary);
    if(!file_in){
        std::cout<<"Error: Could not open file : "<<source<<std::endl;
    }
    if(!file_out){
        std::cout<<"Error: Could not open file : "<<destination<<std::endl;
    }

    char* buffer = new char[BUFFER_SIZE];

    while(file_in.read(buffer, BUFFER_SIZE)){
        file_out.write(buffer, BUFFER_SIZE);
    }





}
