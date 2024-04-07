#include <stdio.h>


// 使用fread和fwrite复制文件并计时
int copy_by_block_with_timing(const char* dest_file_name, const char* src_file_name, double & elapsed_time) {
    FILE* fp1 = fopen(dest_file_name, "w");
    FILE* fp2 = fopen(src_file_name, "r");
    if (fp1 == NULL) {
        perror("fp1:");
        return -1;
    }
    if (fp2 == NULL) {
        perror("fp2:");
        return -1;
    }

    void* buffer = malloc(2);
    int cnt = 0;

    auto start = std::chrono::high_resolution_clock::now();

    while (1) {
        int op = fread(buffer, 1, 1, fp2);
        if (op <= 0) break;
        fwrite(buffer, 1, 1, fp1);
        cnt++;
    }

    auto end = std::chrono::high_resolution_clock::now();
    elapsed_time = std::chrono::duration<double>(end - start).count();

    free(buffer);
    fclose(fp1);
    fclose(fp2);
    return cnt;
}

// 使用read和write复制文件并计时
int copy_by_fileIO_with_timing(const char* dest_file_name, const char* src_file_name, double& elapsed_time) {
    int fd1 = open(dest_file_name, O_WRONLY | O_CREAT | O_APPEND, 0766);
    if (fd1 == -1) {
        perror("fd1:");
        return -1;
    }
    int fd2 = open(src_file_name, O_RDONLY | S_IROTH);
    if (fd2 == -1) {
        perror("fd2:");
        return -1;
    }

    char* buffer = (char*)malloc(2 * sizeof(char));
    int ans = 0;

    auto start = std::chrono::high_resolution_clock::now();

    int k;
    do {
        memset(buffer, 0, sizeof(buffer));
        k = read(fd2, buffer, 1);
        if (k <= 0) break;
        write(fd1, buffer, 1);
        ans++;
    } while (k > 0);

    auto end = std::chrono::high_resolution_clock::now();
    elapsed_time = std::chrono::duration<double>(end - start).count();

    close(fd1);
    close(fd2);
    free(buffer);
    return ans;
}

int main() {
    const char* src_file_name = "a.txt";
    const char* dest_file_name = "destination_file.txt";

    double elapsed_time_fread_fwrite = 0.0;
    double elapsed_time_read_write = 0.0;

    int result_fread_fwrite = copy_by_block_with_timing(dest_file_name, src_file_name, elapsed_time_fread_fwrite);
    std::cout << "Copied " << result_fread_fwrite << " bytes using fread/fwrite in " << elapsed_time_fread_fwrite << " seconds." << std::endl;

    int result_read_write = copy_by_fileIO_with_timing(dest_file_name, src_file_name, elapsed_time_read_write);
    std::cout << "Copied " << result_read_write << " bytes using read/write in " << elapsed_time_read_write << " seconds." << std::endl;

    return 0;
}