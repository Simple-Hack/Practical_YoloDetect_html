#include <iostream>
#include <fstream>
#include <sys/stat.h>
#include <fcntl.h>

// 使用 read 和 write 实现文件复制
void copyFileWithReadWrite(const std::string& source, const std::string& destination, int buffer_size) {
    int src_fd = open(source.c_str(), O_RDONLY);
    if (src_fd == -1) {
        std::cerr << "Error opening source file: " << source << std::endl;
        return;
    }

    int dest_fd = open(destination.c_str(), O_WRONLY | O_CREAT, S_IRUSR | S_IWUSR);
    if (dest_fd == -1) {
        std::cerr << "Error opening or creating destination file: " << destination << std::endl;
        close(src_fd);
        return;
    }

    char* buffer = new char[buffer_size];
    ssize_t bytes_read;

    while ((bytes_read = read(src_fd, buffer, buffer_size)) > 0) {
        ssize_t bytes_written = write(dest_fd, buffer, bytes_read);
        if (bytes_written != bytes_read) {
            std::cerr << "Error writing to destination file" << std::endl;
            break;
        }
    }

    delete[] buffer;
    close(src_fd);
    close(dest_fd);
}

// 使用 fread 和 fwrite 实现文件复制
void copyFileWithFreadFwrite(const std::string& source, const std::string& destination, size_t buffer_size) {
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

int main() {
    const std::string source_path = "D:\\hello.txt";
    const std::string destination_path_read = "D:\\copy_read.txt";
    const std::string destination_path_fread = "D:\\copy_fread.txt";
    const int buffer_size = 4096; // 可以根据需要调整缓冲区大小

    std::cout << "Copying with read/write..." << std::endl;
    copyFileWithReadWrite(source_path, destination_path_read, buffer_size);

    std::cout << "\nCopying with fread/fwrite..." << std::endl;
    copyFileWithFreadFwrite(source_path, destination_path_fread, buffer_size);

    return 0;
}