#include <time.h>
#include <iostream>

double calTime() {
    int a[100000] = { 0 };
    clock_t start = clock();
    for (int i = 0; i < 100000; i++) {
        a[i] += 1;
    }
    clock_t end = clock();
    return (double)(end - start) / CLOCKS_PER_SEC;
}

int main() {
    double timeTaken = calTime();
    std::cout << "Time taken: " << timeTaken << " seconds" << std::endl;
    return 0;
}