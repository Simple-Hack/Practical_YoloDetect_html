from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import torch
import base64
import os
import uuid
import socket
import argparse
import sys
from PIL import Image, ImageDraw, ImageFont
import io
from ultralytics import YOLO  # 导入YOLO库
from collections import defaultdict
import cv2
import numpy as np
import tempfile
import shutil

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 设置上传和输出目录
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/outputs'
TEMP_FOLDER = 'temp'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

# 设置每个文件夹保留的最大文件数量
MAX_FILES_PER_FOLDER = 5

# 在文件顶部添加一个配置变量
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"  # 替换为您实际的ffmpeg路径

# 添加一个全局字典来存储文件处理进度
processing_progress = {}

# 清理文件夹，只保留最新的N个文件
def cleanup_folder(folder_path, max_files=MAX_FILES_PER_FOLDER):
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
                    print(f"已删除旧文件: {f}")
                except Exception as e:
                    print(f"删除文件时出错: {f}, 错误: {e}")
    except Exception as e:
        print(f"清理文件夹 {folder_path} 时出错: {e}")

# 加载YOLO模型
model_car_inside_detection = None

def load_model():
    global model_car_inside_detection
    try:
        # 使用ultralytics库加载YOLO模型
        model_car_inside_detection = YOLO(r'.\models\car_inside_detect.pt')  # 加载车内检测模型
        # 设置模型参数（如果需要的话）
        # 在新版YOLO中，这些参数通常在预测时设置
        return True
    except Exception as e:
        print(f"模型加载失败: {e}")
        return False

# 添加检查端口是否可用的函数
def is_port_available(port):
    """检查指定端口是否可用"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('0.0.0.0', port))
        available = True
    except:
        available = False
    finally:
        sock.close()
    return available

# 查找可用端口
def find_available_port(start_port, max_attempts=100):
    """从start_port开始查找可用端口"""
    for port in range(start_port, start_port + max_attempts):
        if is_port_available(port):
            return port
    return None

# 添加一个类别映射函数，用于合并特定类别
def map_class_name(cls_name):
    """
    合并特定类别到指定类别
    :param cls_name: 原始类别名称
    :return: 映射后的类别名称
    """
    # 检查类别名称是否以"与乘客交谈"开头
    if cls_name.startswith("与乘客交谈"):
        return "安全驾驶"
    return cls_name

@app.route('/progress', methods=['GET'])
def get_progress():
    """获取文件处理进度"""
    filename = request.args.get('filename', '')
    if not filename:
        return jsonify({'error': '未提供文件名'}), 400
    
    # 返回处理进度，如果文件不在进度字典中则返回0
    progress = processing_progress.get(filename, 0)
    return jsonify({'progress': progress})

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': '没有上传图片'}), 400
    
    try:
        file = request.files['file']
        
        # 创建唯一文件名
        file_id = str(uuid.uuid4())
        input_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.jpg")
        output_path = os.path.join(OUTPUT_FOLDER, f"{file_id}_result.jpg")
        
        # 保存上传的图片
        file.save(input_path)
        
        # 确保模型已加载
        global model_car_inside_detection
        if model_car_inside_detection is None:
            if not load_model():
                return jsonify({'error': '模型加载失败'}), 500
        
        model = model_car_inside_detection
        print("使用车内物品检测模型")
        
        # 使用模型进行预测
        results = model(input_path, conf=0.25, iou=0.45)  # 将参数传递给预测函数
        
        # 保存标注后的图片
        for r in results:
            im_array = r.plot()  # 获取绘制后的图像数组
            im = Image.fromarray(im_array[..., ::-1])  # RGB to BGR
            im.save(output_path)
        
        # 提取检测结果
        detections = []
        total_count = 0
        confidence_sum = 0
        max_conf = 0
        
        # 分类别统计
        class_stats = defaultdict(lambda: {
            'count': 0,
            'conf_sum': 0,
            'max_conf': 0,
            'min_conf': 1.0
        })
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0].tolist()  # 获取边界框坐标
                conf = float(box.conf)     # 获取置信度
                cls = int(box.cls)         # 获取类别索引
                cls_name = model.names[cls]  # 获取类别名称
                
                # 应用类别映射
                mapped_cls_name = map_class_name(cls_name)
                
                detections.append({
                    'class': mapped_cls_name,
                    'confidence': conf,
                    'bbox': [b[0], b[1], b[2], b[3]]  # xmin, ymin, xmax, ymax
                })
                
                # 计算总体统计信息
                total_count += 1
                confidence_sum += conf
                max_conf = max(max_conf, conf)
                
                # 计算各类别统计信息 - 使用映射后的类别名称
                cls_stat = class_stats[mapped_cls_name]
                cls_stat['count'] += 1
                cls_stat['conf_sum'] += conf
                cls_stat['max_conf'] = max(cls_stat['max_conf'], conf)
                cls_stat['min_conf'] = min(cls_stat['min_conf'], conf)
        
        # 计算平均可信度
        avg_conf = confidence_sum / total_count if total_count > 0 else 0
        
        # 处理类别统计信息
        class_details = []
        for cls_name, stats in class_stats.items():
            avg_cls_conf = stats['conf_sum'] / stats['count'] if stats['count'] > 0 else 0
            class_details.append({
                'name': cls_name,
                'count': stats['count'],
                'avg_confidence': avg_cls_conf,
                'max_confidence': stats['max_conf'],
                'min_confidence': stats['min_conf']
            })
        
        # 按检测数量排序类别
        class_details.sort(key=lambda x: x['count'], reverse=True)
        
        # 总体统计信息
        statistics = {
            'total_count': total_count,
            'class_count': len(class_stats),  # 检测到的类别数量
            'avg_confidence': avg_conf,
            'max_confidence': max_conf,
            'class_details': class_details  # 各类别详细统计
        }
        
        # 确保返回正确的图像URL路径
        image_url = f"/static/outputs/{file_id}_result.jpg"
        
        # 清理文件夹，只保留最新的N个文件
        cleanup_folder(UPLOAD_FOLDER)
        cleanup_folder(OUTPUT_FOLDER)
        
        return jsonify({
            'success': True,
            'detections': detections,
            'image_url': image_url,
            'statistics': statistics
        })
    
    except Exception as e:
        return jsonify({'error': f'处理过程中出错: {str(e)}'}), 500

@app.route('/predict_video', methods=['POST'])
def predict_video():
    if 'file' not in request.files:
        return jsonify({'error': '没有上传视频文件'}), 400
    
    try:
        file = request.files['file']
        
        # 创建唯一文件名
        file_id = str(uuid.uuid4())
        input_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.mp4")
        output_path = os.path.join(OUTPUT_FOLDER, f"{file_id}_result.mp4")
        
        # 保存上传的视频
        file.save(input_path)
        
        # 在全局进度字典中初始化此文件的进度
        file_name = file.filename
        processing_progress[file_name] = 0
        
        # 确保模型已加载
        global model_car_inside_detection
        if model_car_inside_detection is None:
            if not load_model():
                return jsonify({'error': '模型加载失败'}), 500
        
        model = model_car_inside_detection
        print("使用车内物品检测模型处理视频")
        
        # 创建临时目录存储处理的帧
        temp_dir = os.path.join(TEMP_FOLDER, file_id)
        os.makedirs(temp_dir, exist_ok=True)
        
        # 打开视频文件
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            return jsonify({'error': '无法打开视频文件'}), 500
        
        # 获取视频属性
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # 创建视频写入器 - 尝试使用更兼容的编码器
        try:
            # 尝试使用 H.264 编码 (avc1)
            fourcc = cv2.VideoWriter_fourcc(*'avc1')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            # 检查是否成功创建
            if not out.isOpened():
                # 回退到 mp4v
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                print("警告: 使用回退编码器 mp4v")
        except Exception as e:
            print(f"创建视频写入器时出错: {e}，使用默认编码器")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # 处理统计信息
        all_detections = []
        frame_count = 0
        
        # 分类别统计
        class_stats = defaultdict(lambda: {
            'count': 0,
            'conf_sum': 0,
            'max_conf': 0,
            'min_conf': 1.0
        })
        
        total_count = 0
        confidence_sum = 0
        max_conf = 0
        
        # 用于存储连续检测的类别历史记录
        class_history = []
        # 需要连续检测的次数才确认类别
        consecutive_threshold = 8
        # 当前确认的类别
        current_confirmed_class = None
        
        # 存储所有帧的处理结果
        frame_results = {}
        
        # 跟踪每个类别在每一帧的出现情况
        class_frame_tracker = defaultdict(list)
        
        # 处理视频帧 - 增加采集密度，每帧都处理
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # 更新处理进度
            current_progress = frame_count / total_frames if total_frames > 0 else 0
            processing_progress[file_name] = current_progress
            
            # 保存当前帧为临时图像
            temp_frame_path = os.path.join(temp_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(temp_frame_path, frame)
            
            # 使用YOLO模型进行预测
            results = model(temp_frame_path, conf=0.25, iou=0.45)
            
            # 提取当前帧中最可能的类别（置信度最高的）
            current_frame_classes = {}
            
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    b = box.xyxy[0].tolist()  # 获取边界框坐标
                    conf = float(box.conf)     # 获取置信度
                    cls = int(box.cls)         # 获取类别索引
                    cls_name = model.names[cls]  # 获取类别名称
                    
                    # 应用类别映射
                    mapped_cls_name = map_class_name(cls_name)
                    
                    # 记录当前帧中这个类别的最高置信度
                    if mapped_cls_name not in current_frame_classes or conf > current_frame_classes[mapped_cls_name]['conf']:
                        current_frame_classes[mapped_cls_name] = {'conf': conf, 'bbox': b}
            
            # 确定当前帧的主要类别（置信度最高的类别）
            main_class = None
            max_conf_in_frame = 0
            for cls_name, info in current_frame_classes.items():
                if info['conf'] > max_conf_in_frame:
                    max_conf_in_frame = info['conf']
                    main_class = cls_name
            
            # 更新类别历史
            if main_class:
                class_history.append(main_class)
            else:
                # 如果当前帧没有检测到任何类别，则视为"未知"
                class_history.append("未知")
            
            # 只保留最近 consecutive_threshold 个检测结果
            if len(class_history) > consecutive_threshold:
                class_history.pop(0)
            
            # 检查是否连续检测到相同类别
            if len(class_history) == consecutive_threshold:
                # 检查是否所有元素都相同
                if all(cls == class_history[0] for cls in class_history) and class_history[0] != "未知":
                    current_confirmed_class = class_history[0]
                
                # 如果连续检测不到确定的类别，保持最后确认的类别
                # 注意：此处不会将当前确认的类别重置为None
            
            # 存储当前帧的处理结果
            frame_results[frame_count] = {
                'frame': frame.copy(),  # 存储原始帧
                'confirmed_class': current_confirmed_class,  # 当前确认的类别
                'detections': [
                    {
                        'class': cls_name,
                        'confidence': info['conf'],
                        'bbox': info['bbox']
                    } 
                    for cls_name, info in current_frame_classes.items()
                ],
                'main_detection': {
                    'class': main_class,
                    'confidence': max_conf_in_frame if main_class else 0
                } if main_class else None
            }
            
            # 更新统计信息
            for cls_name, info in current_frame_classes.items():
                detection = {
                    'class': cls_name,
                    'confidence': info['conf'],
                    'bbox': info['bbox'],
                    'frame': frame_count
                }
                all_detections.append(detection)
                

                # 计算统计信息
                total_count += 1
                confidence_sum += info['conf']
                max_conf = max(max_conf, info['conf'])
                
                # 计算各类别统计信息
                cls_stat = class_stats[cls_name]
                cls_stat['count'] += 1
                cls_stat['conf_sum'] += info['conf']
                cls_stat['max_conf'] = max(cls_stat['max_conf'], info['conf'])
                cls_stat['min_conf'] = min(cls_stat['min_conf'], info['conf'])
            
            # 对于每个确认的类别，记录它出现的帧
            if current_confirmed_class:
                class_frame_tracker[current_confirmed_class].append(frame_count)
            
            # 打印进度
            if frame_count % 50 == 0:
                print(f"已处理 {frame_count}/{total_frames} 帧，进度: {(frame_count/total_frames)*100:.2f}%")
                if current_confirmed_class:
                    print(f"当前确认的类别: {current_confirmed_class}")
            
            frame_count += 1
            
            # 为了减轻内存压力，可以定期处理帧并写入视频
            if frame_count % 100 == 0 or frame_count == total_frames - 1:
                # 处理并写入视频文件
                for i in range(max(0, frame_count-100), frame_count):
                    if i in frame_results:
                        # 获取当前帧信息
                        frame_data = frame_results[i]
                        annotated_frame = frame_data['frame'].copy()
                        
                        # 在帧上标注确认的类别
                        confirmed_class = frame_data['confirmed_class']
                        if confirmed_class:
                            # 创建类别到颜色的映射，为不同类别提供不同颜色
                            class_colors = {
                                "安全驾驶": (0, 255, 0),  # 绿色
                                "疲劳驾驶": (0, 0, 255),  # 红色
                                "分心驾驶": (255, 0, 0),  # 蓝色
                                "玩手机": (255, 255, 0),  # 青色
                                "抽烟": (0, 255, 255),    # 黄色
                                "打电话": (255, 0, 255),  # 紫色
                                "喝水": (255, 165, 0),    # 橙色
                                "疲劳": (128, 0, 128),    # 深紫色
                                "注意力分散": (0, 128, 128),  # 深青色
                            }
                            
                            # 获取类别对应的颜色，如果没有预定义则使用白色
                            color = class_colors.get(confirmed_class, (255, 255, 255))
                            
                            # 解决中文显示问题
                            try:
                                # 将OpenCV图像转换为PIL图像以支持中文
                                img_pil = Image.fromarray(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))
                                draw = ImageDraw.Draw(img_pil)
                                
                                # 尝试加载中文字体，如果失败则使用默认字体
                                font_paths = [
                                    'C:\\Windows\\Fonts\\simhei.ttf',  # 黑体
                                    'C:\\Windows\\Fonts\\simsun.ttc',  # 宋体
                                    'C:\\Windows\\Fonts\\simkai.ttf',  # 楷体
                                    'C:\\Windows\\Fonts\\msyh.ttc',    # 微软雅黑
                                ]
                                
                                font = None
                                for path in font_paths:
                                    try:
                                        if os.path.exists(path):
                                            font = ImageFont.truetype(path, 36)
                                            break
                                    except:
                                        continue
                                        
                                if font is None:
                                    # 如果没有找到系统字体，尝试使用PIL默认字体
                                    font = ImageFont.load_default()
                                    
                                # 绘制文本，添加黑色轮廓使文本更清晰
                                # 首先绘制黑色边框
                                for offset_x, offset_y in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                                    draw.text((10 + offset_x, 30 + offset_y), f"类别: {confirmed_class}", 
                                             fill=(0, 0, 0), font=font)
                                
                                # 然后绘制彩色文本
                                draw.text((10, 30), f"类别: {confirmed_class}", 
                                         fill=color[::-1], font=font)  # PIL使用RGB而非BGR
                                
                                # 将PIL图像转回OpenCV格式
                                annotated_frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
                                
                            except Exception as e:
                                print(f"绘制中文文本出错: {e}")
                                # 如果中文渲染失败，退回到OpenCV的英文渲染
                                cv2.putText(
                                    annotated_frame, 
                                    f"Class: {confirmed_class}", 
                                    (10, 30), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 
                                    1, 
                                    color, 
                                    2
                                )
                        
                        # 绘制所有检测框
                        for detection in frame_data['detections']:
                            bbox = detection['bbox']
                            cls_name = detection['class']
                            conf = detection['confidence']
                            
                            # 绘制边界框
                            cv2.rectangle(
                                annotated_frame, 
                                (int(bbox[0]), int(bbox[1])), 
                                (int(bbox[2]), int(bbox[3])), 
                                (0, 255, 0), 
                                2
                            )
                            
                            # 添加类别和置信度标签
                            label = f"{cls_name}: {conf:.2f}"
                            cv2.putText(
                                annotated_frame, 
                                label, 
                                (int(bbox[0]), int(bbox[1])-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                0.5, 
                                (0, 255, 0), 
                                2
                            )
                        
                        # 写入处理后的帧
                        out.write(annotated_frame)
                        
                        # 从字典中移除已写入的帧，释放内存
                        del frame_results[i]
        
        # 表示处理已完成
        processing_progress[file_name] = 1.0
        
        # 计算每个类别的连续帧段
        class_segments = {}
        for cls_name, frames in class_frame_tracker.items():
            if not frames:
                continue
                
            # 按帧排序
            frames.sort()
            
            # 找出连续的帧段
            segments = []
            segment_start = frames[0]
            prev_frame = frames[0]
            
            for frame in frames[1:]:
                # 如果与前一帧不连续(差距大于1)，则创建新段
                if frame > prev_frame + 1:
                    segments.append((segment_start, prev_frame))
                    segment_start = frame
                prev_frame = frame
            
            # 添加最后一个段
            segments.append((segment_start, prev_frame))
            
            # 计算所有段的总帧数
            total_segment_frames = sum(end - start + 1 for start, end in segments)
            class_segments[cls_name] = {
                'segments': segments,
                'total_frames': total_segment_frames
            }
        
        # 计算每个类别的持续时间（秒）
        class_durations = {}
        for cls_name, segment_data in class_segments.items():
            duration_seconds = (segment_data['total_frames'] / fps) if fps > 0 else 0
            class_durations[cls_name] = round(duration_seconds, 2)  # 精确到两位小数
        
        # 跟踪每个类别的出现帧数
        class_frames = defaultdict(int)
        
        # 计算类别持续时间
        for cls_name, stats in class_stats.items():
            # 计算该类别在视频中的总帧数
            for i in range(total_frames):
                if i in frame_results and frame_results[i]['confirmed_class'] == cls_name:
                    class_frames[cls_name] += 1
        
        # 计算平均可信度
        avg_conf = confidence_sum / total_count if total_count > 0 else 0
        
        # 处理类别统计信息
        class_details = []
        for cls_name, stats in class_stats.items():
            avg_cls_conf = stats['conf_sum'] / stats['count'] if stats['count'] > 0 else 0
            class_details.append({
                'name': cls_name,
                'count': stats['count'],
                'avg_confidence': avg_cls_conf,
                'max_confidence': stats['max_conf'],
                'min_confidence': stats['min_conf'],
                'duration': class_durations.get(cls_name, 0)  # 使用新计算的持续时间
            })
        
        # 按检测数量排序类别
        class_details.sort(key=lambda x: x['count'], reverse=True)
        
        # 总体统计信息
        statistics = {
            'total_count': total_count,
            'class_count': len(class_stats),
            'avg_confidence': avg_conf,
            'max_confidence': max_conf,
            'class_details': class_details,
            'total_frames': total_frames,
            'fps': fps,
            'video_duration': total_frames / fps if fps > 0 else 0
        }
        
        # 释放资源
        cap.release()
        out.release()
        
        # 检查输出视频是否生成成功
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            return jsonify({'error': '视频生成失败，请检查服务器日志'}), 500
            
        print(f"视频处理完成: {output_path}, 大小: {os.path.getsize(output_path)} 字节")
        
        # 尝试使用 ffmpeg 进行格式转换以提高浏览器兼容性
        video_url = f"/static/outputs/{file_id}_result.mp4"  # 默认使用MP4
        try:
            # 首先检查ffmpeg是否可用
            ffmpeg_available = False
            try:
                # 优先使用配置的路径
                if os.path.exists(FFMPEG_PATH):
                    ffmpeg_cmd = FFMPEG_PATH
                    ffmpeg_available = True
                    print(f"使用配置的ffmpeg路径: {FFMPEG_PATH}")
                else:
                    # 尝试使用环境变量中的ffmpeg
                    import subprocess
                    result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    if result.returncode == 0:
                        ffmpeg_available = True
                        ffmpeg_cmd = 'ffmpeg'
                        print("使用环境变量中的ffmpeg")
                    else:
                        print("未检测到ffmpeg，跳过视频格式转换")
            except Exception as e:
                print(f"检查ffmpeg安装状态时出错: {e}")
            
            if ffmpeg_available:
                webm_output_path = os.path.join(OUTPUT_FOLDER, f"{file_id}_result.webm")
                
                # 使用绝对路径以确保ffmpeg命令能正确运行
                input_abs_path = os.path.abspath(output_path)
                output_abs_path = os.path.abspath(webm_output_path)
                
                # 尝试将MP4转换为WebM格式，大多数浏览器都支持
                command = [
                    ffmpeg_cmd, '-i', input_abs_path, 
                    '-c:v', 'libvpx-vp9', '-crf', '30', '-b:v', '0',
                    output_abs_path
                ]
                
                print(f"执行命令: {' '.join(command)}")
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                
                # 检查命令是否执行成功
                if result.returncode == 0 and os.path.exists(webm_output_path) and os.path.getsize(webm_output_path) > 0:
                    video_url = f"/static/outputs/{file_id}_result.webm"
                    print(f"视频转换为WebM成功: {webm_output_path}")
                else:
                    print(f"视频格式转换失败，返回原始MP4格式")
                    print(f"ffmpeg错误: {result.stderr.decode('utf-8', errors='ignore')}")
        except Exception as e:
            print(f"尝试转换视频格式时出错: {e}")
            import traceback
            print(traceback.format_exc())
        
        # 清理临时文件
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        # 清理完成后从进度字典中移除
        if file_name in processing_progress:
            del processing_progress[file_name]
        
        # 清理文件夹，只保留最新的N个文件
        cleanup_folder(UPLOAD_FOLDER)
        cleanup_folder(OUTPUT_FOLDER)
        
        return jsonify({
            'success': True,
            'detections': all_detections,
            'video_url': video_url,
            'statistics': statistics,
            'video_info': {
                'width': width,
                'height': height,
                'fps': fps,
                'total_frames': total_frames
            }
        })
    
    except Exception as e:
        # 发生错误时清除进度记录
        if 'file_name' in locals() and file_name in processing_progress:
            del processing_progress[file_name]
        
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': f'处理视频过程中出错: {str(e)}'}), 500

@app.route('/static/outputs/<path:filename>')
def serve_output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    # 添加命令行参数解析
    parser = argparse.ArgumentParser(description='车内物品检测服务器')
    parser.add_argument('-p', '--port', type=int, default=5050, help='服务器端口号(默认: 5050)')
    args = parser.parse_args()
    
    # 检查指定端口是否可用
    port = args.port
    if not is_port_available(port):
        # 如果指定端口不可用，尝试查找可用端口
        available_port = find_available_port(port + 1)
        if available_port:
            print(f"端口 {port} 已被占用，将使用端口 {available_port}")
            port = available_port
        else:
            print(f"错误：无法找到可用端口。请尝试手动指定一个端口: python {sys.argv[0]} --port <端口号>")
            sys.exit(1)
    
    print("正在加载YOLO模型...")
    load_model()
    print(f"模型加载完成，服务已启动在 http://localhost:{port}")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=port)
    except OSError as e:
        print(f"启动服务器时出错: {e}")
        print("可能的原因：")
        print("1. 端口已被占用")
        print("2. 没有足够的权限绑定到该端口")
        print(f"请尝试使用不同的端口: python {sys.argv[0]} --port <端口号>")
        sys.exit(1)
