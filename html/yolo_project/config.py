import os

# 文件夹配置
UPLOAD_FOLDER = 'uploads'
# 使用绝对路径以确保一致性
OUTPUT_FOLDER = 'D:\\VsFile\\html\\static\\outputs'  # 使用绝对路径避免相对路径混淆
TEMP_FOLDER = 'temp'

# 检测配置
CONSECUTIVE_THRESHOLD = 3  # 需要连续检测的次数才确认类别
FRAME_PROCESSING_INTERVAL = 50  # 帧处理周期，每 FRAME_PROCESSING_INTERVAL 帧处理一帧

# 视频处理配置
MAX_FILES_PER_FOLDER = 5  # 设置每个文件夹保留的最大文件数量
FFMPEG_PATH = r"D:\ffmsg\ffmpeg-2025-03-31-git-35c091f4b7-full_build\ffmpeg-2025-03-31-git-35c091f4b7-full_build\bin\ffmpeg.exe"  # FFMPEG路径

# 字体配置
FONT_PATHS = [
    'C:\\Windows\\Fonts\\simhei.ttf',  # 黑体
    'C:\\Windows\\Fonts\\simsun.ttc',  # 宋体
    'C:\\Windows\\Fonts\\simkai.ttf',  # 楷体
    'C:\\Windows\\Fonts\\msyh.ttc',    # 微软雅黑
]

# 调试配置
DEBUG_MODE = True  # 临时启用调试模式用于排查问题

# 创建必要的目录
for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, TEMP_FOLDER]:
    os.makedirs(folder, exist_ok=True)
