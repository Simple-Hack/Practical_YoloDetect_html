#include <iostream>
#include <map>
#include <string>

int main() {
    std::multimap<std::string, int> phoneBook {
        { "Alice", 1234 },
        { "Bob", 5678 },
        { "Charlie",9012 },
        { "Alice", 3456 },  // Alice有两个电话号码
    };

    // 使用equal_range查找所有键值为"Alice"的键值对
    auto range = phoneBook.equal_range("Alice");

    std::cout << "Alice's phone numbers:" << std::endl;
    for (auto it = range.first; it != range.second; ++it) {
        std::cout << it->second << " ";
    }
    std::cout << std::endl;

    // 使用erase删除所有键值为"Charlie"的键值对
    phoneBook.erase("Charlie");

    std::cout << "Phone book after removing Charlie:" << std::endl;
    for (const auto& entry : phoneBook) {
        std::cout << entry.first << ": " << entry.second << std::endl;
    }

    return 0;
}