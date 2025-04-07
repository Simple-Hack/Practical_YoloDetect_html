import cv2
import os
import socket
from collections import defaultdict
from config import DEBUG_MODE

def is_port_available(port):
    """
    检查指定端口是否可用
    :param port: 端口号
    :return: 可用返回True，否则返回False
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('0.0.0.0', port))
        available = True
    except:
        available = False
    finally:
        sock.close()
    return available

def find_available_port(start_port, max_attempts=100):
    """
    从start_port开始查找可用端口
    :param start_port: 起始端口号
    :param max_attempts: 最大尝试次数
    :return: 可用端口号，未找到返回None
    """
    for port in range(start_port, start_port + max_attempts):
        if is_port_available(port):
            return port
    return None

def create_video_writer_with_quality(output_path, width, height, fps, quality='high'):
    quality_settings = {
        'high': {'codec': 'avc1', 'params': [cv2.VIDEOWRITER_PROP_QUALITY, 100]},
        'medium': {'codec': 'mp4v', 'params': [cv2.VIDEOWRITER_PROP_QUALITY, 80]},
        'low': {'codec': 'xvid', 'params': []}
    }
    
    setting = quality_settings.get(quality, quality_settings['medium'])
    fourcc = cv2.VideoWriter_fourcc(*setting['codec'])
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    if setting['params']:
        out.set(*setting['params'])
    
    return out

def create_video_writer(output_path, width, height, fps):
    """
    创建视频写入器的简化版本，使用中等质量设置
    :param output_path: 输出视频路径
    :param width: 视频宽度
    :param height: 视频高度
    :param fps: 帧率
    :return: 视频写入器对象
    """
    return create_video_writer_with_quality(output_path, width, height, fps, quality='medium')

def normalize_path(path):
    """
    规范化文件路径，确保路径分隔符一致
    :param path: 原始路径
    :return: 规范化后的路径
    """
    # 处理特殊情况 - 如果以相对路径 '../static/outputs' 开头
    if path.startswith('../static/outputs') or path.startswith('..\\static\\outputs'):
        # 使用绝对路径替换
        base_path = os.path.normpath('D:\\VsFile\\static\\outputs')
        rel_path = path.replace('../static/outputs', '').replace('..\\static\\outputs', '')
        rel_path = rel_path.lstrip('/\\')  # 移除开头的斜杠
        path = os.path.join(base_path, rel_path)
        
    # 确保是绝对路径
    if not os.path.isabs(path):
        # 要么是项目内的路径，要么直接使用绝对路径
        if os.path.exists(path) or path.startswith('static/') or path.startswith('static\\'):
            # 如果是项目内静态资源，使用正确的绝对路径
            base_dir = 'D:\\VsFile\\html'
            path = os.path.join(base_dir, path)
        else:
            # 其他情况，尝试从当前目录解析
            path = os.path.abspath(path)
    
    # 将正斜杠和反斜杠统一为系统标准路径分隔符
    normalized_path = os.path.normpath(path)
    
    # 确保目录存在
    dir_path = os.path.dirname(normalized_path)
    if dir_path and not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path, exist_ok=True)
            if DEBUG_MODE:
                print(f"创建目录: {dir_path}")
        except Exception as e:
            if DEBUG_MODE:
                print(f"创建目录失败: {dir_path}, 错误: {e}")
    
    if DEBUG_MODE:
        print(f"规范化路径: {path} -> {normalized_path}")
        print(f"文件是否存在: {os.path.exists(normalized_path)}")
    
    return normalized_path

def convert_video_format(input_path, output_path, target_format='mp4'):
    """
    使用OpenCV直接转换视频格式，不依赖ffmpeg
    :param input_path: 输入视频路径
    :param output_path: 输出视频路径
    :param target_format: 目标格式，支持mp4和webm
    :return: 成功返回True和输出路径，失败返回False和原始路径
    """
    try:
        # 规范化路径
        input_path = normalize_path(input_path)
        output_path = normalize_path(output_path)
        
        if target_format.lower() not in ['mp4', 'webm']:
            if DEBUG_MODE:
                print(f"不支持的目标格式: {target_format}，目前支持MP4和WebM")
            return False, input_path
            
        # 读取输入视频
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            if DEBUG_MODE:
                print(f"无法打开输入视频: {input_path}")
            return False, input_path
            
        # 获取视频属性
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # 为不同格式选择编码器
        codecs = []
        if target_format.lower() == 'mp4':
            codecs = ['avc1', 'h264', 'mp4v', 'xvid']
        elif target_format.lower() == 'webm':
            codecs = ['VP80', 'VP90', 'vp80', 'vp90']
        
        success = False
        
        for codec in codecs:
            try:
                fourcc = cv2.VideoWriter_fourcc(*codec)
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                
                if not out.isOpened():
                    if DEBUG_MODE:
                        print(f"编码器 {codec} 初始化失败，尝试下一个")
                    out.release()
                    continue
                
                # 逐帧复制视频
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    out.write(frame)
                
                # 释放资源
                cap.release()
                out.release()
                
                # 检查输出文件是否创建成功
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    success = True
                    if DEBUG_MODE:
                        print(f"使用编码器 {codec} 成功转换视频为{target_format.upper()}")
                    break
                else:
                    if DEBUG_MODE:
                        print(f"编码器 {codec} 创建的文件无效")
            except Exception as e:
                if DEBUG_MODE:
                    print(f"使用编码器 {codec} 转换视频时出错: {e}")
                continue
        
        if not success:
            if DEBUG_MODE:
                print(f"所有{target_format.upper()}编码器都失败，返回原始视频")
            return False, input_path
            
        return True, output_path
            
    except Exception as e:
        if DEBUG_MODE:
            print(f"转换视频格式时出错: {e}")
            import traceback
            traceback.print_exc()
        return False, input_path

def check_video_validity(video_path):
    try:
        # 规范化文件路径
        video_path = normalize_path(video_path)
        
        # 首先检查文件是否存在
        if not os.path.exists(video_path):
            if DEBUG_MODE:
                print(f"视频文件不存在: {video_path}")
            return False
            
        # 检查文件大小是否为0
        if os.path.getsize(video_path) == 0:
            if DEBUG_MODE:
                print(f"视频文件大小为0: {video_path}")
            return False
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            if DEBUG_MODE:
                print(f"无法打开视频: {video_path}")
            return False
            
        # 检查基本属性
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        codec_int = int(cap.get(cv2.CAP_PROP_FOURCC))
        codec = chr(codec_int & 0xFF) + chr((codec_int >> 8) & 0xFF) + chr((codec_int >> 16) & 0xFF) + chr((codec_int >> 24) & 0xFF)
        
        if DEBUG_MODE:
            print(f"视频信息 - 宽: {width}, 高: {height}, FPS: {fps}, 帧数: {frame_count}, 编码器: {codec}")
        
        if width <= 0 or height <= 0 or fps <= 0 or frame_count <= 0:
            if DEBUG_MODE:
                print(f"视频属性无效: {video_path}")
            return False
            
        # 采样检查多个关键帧
        check_points = [0, frame_count//2, frame_count-1] if frame_count > 2 else [0]
        for point in check_points:
            cap.set(cv2.CAP_PROP_POS_FRAMES, point)
            ret, frame = cap.read()
            if not ret:
                if DEBUG_MODE:
                    print(f"无法读取视频帧 {point}/{frame_count}: {video_path}")
                return False
        
        if DEBUG_MODE:
            print(f"视频检查通过: {video_path}")
        return True
    except Exception as e:
        if DEBUG_MODE:
            print(f"检查视频有效性时出错: {e}")
            import traceback
            traceback.print_exc()
        return False
    finally:
        if 'cap' in locals() and cap is not None:
            cap.release()
