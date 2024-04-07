import os

def get_size_type(directory):
    total_size = 0
    size_dict = {}
    type_dict = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            total_size += file_size

            file_extension = os.path.splitext(file)[1].lower()
            if file_extension not in size_dict:
                size_dict[file_extension] = file_size
                type_dict[file_extension] = 1
            else:
                size_dict[file_extension] += file_size
                type_dict[file_extension] += 1

    return total_size, size_dict, type_dict

def print_results(total_size, size_dict, type_dict):
    print(f"\nTotal size of all files: {total_size / (1024 * 1024)} MB")
    
    print("\nSize breakdown by file extension:")
    for ext, size in sorted(size_dict.items(), key=lambda x: x[1], reverse=True):
        print(f"{ext}: {size / (1024 * 1024):.2f} MB ({type_dict[ext]} files)")

def main():
    target_dir = r"D:\\"
    total_size, size_dict, type_dict = get_size_type(target_dir)
    print_results(total_size, size_dict, type_dict)

if __name__ == "__main__":
    main()