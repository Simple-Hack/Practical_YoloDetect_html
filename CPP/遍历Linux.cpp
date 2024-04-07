#include <dirent.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <iostream>
#include <fstream>

// 使用 fread 和 fwrite 实现文件复制
void copyFileWithReadWrite(const std::string& source, const std::string& destination, size_t buffer_size) {
    std::ifstream src_file(source, std::ios::binary);
    if (!src_file) {
        std::cerr << "Error opening source file: " << source << std::endl;
        return;
    }

    std::ofstream dest_file(destination, std::ios::binary | std::ios::trunc);
    if (!dest_file) {
        std::cerr << "Error opening or creating destination file: " << destination << std::endl;
        src_file.close();
        return;
    }

    char* buffer = new char[buffer_size];

    while (true) {
        src_file.read(buffer, buffer_size);
        size_t bytes_read = src_file.gcount();

        if (bytes_read == 0) {
            break; // End of file
        }

        dest_file.write(buffer, bytes_read);
        if (!dest_file) {
            std::cerr << "Error writing to destination file" << std::endl;
            break;
        }
    }

    delete[] buffer;
    src_file.close();
    dest_file.close();
}

// 使用 read 和 write 实现文件复制的函数（同前）

void copyDirectory(const std::string& source_dir, const std::string& dest_dir, int buffer_size) {
    struct stat source_stat;
    if (stat(source_dir.c_str(), &source_stat) != 0 || !S_ISDIR(source_stat.st_mode)) {
        std::cerr << "Source directory does not exist or is not a directory: " << source_dir << std::endl;
        return;
    }

    mkdir(dest_dir.c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

    DIR* dir = opendir(source_dir.c_str());
    if (!dir) {
        std::cerr << "Failed to open source directory: " << source_dir << std::endl;
        return;
    }

    struct dirent* entry;
    while ((entry = readdir(dir)) != nullptr) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
            continue; // Skip "." and ".."
        }

        std::string source_entry_path = source_dir + "/" + entry->d_name;
        std::string dest_entry_path = dest_dir + "/" + entry->d_name;

        struct stat entry_stat;
        if (stat(source_entry_path.c_str(), &entry_stat) != 0) {
            std::cerr << "Failed to get information for entry: " << source_entry_path << std::endl;
            continue;
        }

        if (S_ISDIR(entry_stat.st_mode)) {
            copyDirectory(source_entry_path, dest_entry_path, buffer_size);
        } else {
            copyFileWithReadWrite(source_entry_path, dest_entry_path, buffer_size);
        }
    }

    closedir(dir);
}

int main() {
    const std::string source_dir = "/home/simple/Documents/Cfile";
    const std::string dest_dir = "/home/simple/Documents/Copy";
    const int buffer_size = 4096; // 可以根据需要调整缓冲区大小

    copyDirectory(source_dir, dest_dir, buffer_size);

    return 0;
}