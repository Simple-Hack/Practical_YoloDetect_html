#include <iostream>
#include <filesystem>
#include <fstream>
#include <string>


// 使用 std::filesystem 和 std::ifstream/std::ofstream 实现文件复制
void copyFileWithFstream(const std::filesystem::path& source, const std::filesystem::path& destination) {
    std::ifstream src_file(source, std::ios::binary);
    if (!src_file) {
        std::cerr << "Error opening source file: " << source << std::endl;
        return;
    }

    std::ofstream dest_file(destination, std::ios::binary);
    if (!dest_file) {
        std::cerr << "Error opening or creating destination file: " << destination << std::endl;
        src_file.close();
        return;
    }

    char buffer[4096]; // 缓冲区大小
    while (src_file.read(buffer, sizeof(buffer))) {
        dest_file.write(buffer, src_file.gcount());
    }

    if (!src_file.eof()) {
        std::cerr << "Error reading from source file" << std::endl;
    }

    src_file.close();
    dest_file.close();
}

void copyDirectory(const std::filesystem::path& source_dir, const std::filesystem::path& dest_dir) {
    if (!std::filesystem::exists(source_dir)) {
        std::cerr << "Source directory does not exist: " << source_dir << std::endl;
        return;
    }

    if (!std::filesystem::is_directory(source_dir)) {
        std::cerr << "Source path is not a directory: " << source_dir << std::endl;
        return;
    }

    std::filesystem::create_directories(dest_dir); // 创建目标目录及其所有不存在的父目录

    for (const auto& entry : std::filesystem::recursive_directory_iterator(source_dir)) {
        std::filesystem::path relative_path = entry.path().lexically_relative(source_dir);
        std::filesystem::path dest_entry_path = dest_dir / relative_path;

        if (entry.is_directory()) {
            std::filesystem::create_directories(dest_entry_path);
        } else if (entry.is_regular_file()) {
            copyFileWithFstream(entry.path(), dest_entry_path);
        } else {
            std::cerr << "Unsupported entry type: " << entry.path() << std::endl;
        }
    }
}

int main() {
    const std::filesystem::path source_dir = "/home/simple/Documents/Cfile";
    const std::filesystem::path dest_dir = "/home/simple/Documents/Copy";

    copyDirectory(source_dir, dest_dir);

    return 0;
}