import os
import uuid
import datetime
from config import DEBUG_MODE

def cleanup_folder(folder_path, max_files=5):
    """
    清理指定文件夹，只保留最新的max_files个文件
    :param folder_path: 文件夹路径
    :param max_files: 要保留的最大文件数
    """
    try:
        # 获取文件夹中所有文件
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        
        # 按文件修改时间排序
        files.sort(key=lambda x: os.path.getmtime(x))
        
        # 如果文件数量超过最大值，删除最旧的文件
        if len(files) > max_files:
            for f in files[:-max_files]:  # 保留最新的max_files个文件
                try:
                    os.remove(f)
                    if DEBUG_MODE:
                        print(f"已删除旧文件: {f}")
                except Exception as e:
                    print(f"删除文件时出错: {f}, 错误: {e}")
    except Exception as e:
        print(f"清理文件夹 {folder_path} 时出错: {e}")

def generate_unique_filename(original_filename, prefix="", suffix=""):
    """
    生成唯一的文件名，避免文件名冲突
    :param original_filename: 原始文件名
    :param prefix: 文件名前缀
    :param suffix: 文件名后缀
    :return: 生成的唯一文件名
    """
    # 获取文件扩展名
    _, ext = os.path.splitext(original_filename)
    
    # 生成基于时间和UUID的唯一标识符
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4().hex)[:8]  # 使用UUID的前8位作为唯一标识
    
    # 组合新的文件名
    new_filename = f"{prefix}{timestamp}_{unique_id}{suffix}{ext}"
    
    if DEBUG_MODE:
        print(f"为 {original_filename} 生成了唯一文件名: {new_filename}")
    
    return new_filename
