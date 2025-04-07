import os
import cv2
import shutil
import traceback
from collections import defaultdict
from PIL import Image, ImageDraw
from models.model_loader import get_model, map_class_name
from utils.image_utils import draw_text_with_background, get_color_for_class
from utils.file_utils import cleanup_folder, generate_unique_filename
from utils.video_utils import create_video_writer, convert_video_format
from config import TEMP_FOLDER, DEBUG_MODE, CONSECUTIVE_THRESHOLD, FRAME_PROCESSING_INTERVAL

# 存储处理进度的全局字典
processing_progress = {}

def process_video_detection(input_path, output_path, file_id, file_name):
    """
    处理视频检测任务
    :param input_path: 输入视频路径
    :param output_path: 输出视频路径
    :param file_id: 文件唯一标识
    :param file_name: 原始文件名
    :return: 处理结果字典
    """
    try:
        # 初始化处理进度
        processing_progress[file_name] = 0
        
        # 获取模型
        model = get_model()
        if model is None:
            return {'error': '模型加载失败'}, False
        
        # 创建临时目录存储处理的帧
        temp_dir = os.path.join(TEMP_FOLDER, file_id)
        os.makedirs(temp_dir, exist_ok=True)
        
        # 打开视频文件
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            error_msg = f"无法打开视频文件: {input_path}"
            print(error_msg)
            return {'error': error_msg}, False
        
        # 获取视频属性
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if DEBUG_MODE:
            print(f"视频信息: 宽度={width}, 高度={height}, FPS={fps}, 总帧数={total_frames}")
        
        # 创建视频写入器
        out = create_video_writer(output_path, width, height, fps)
        
        # 检查视频是否正常读取
        test_read, test_frame = cap.read()
        if not test_read:
            error_msg = "无法从视频文件读取帧，视频文件可能已损坏"
            print(error_msg)
            cap.release()
            return {'error': error_msg}, False
        
        # 将视频指针重置回起始位置
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        # 处理统计信息
        all_detections = []
        frame_count = 0
        processed_frame_count = 0
        
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
        
        # 存储每个处理周期的主要类别
        cycle_classes = []
        # 每个周期的起始帧
        cycle_start_frames = []
        
        # 用于标记帧范围的字典，记录每个帧范围应该标注的类别
        frame_labels = {}
        
        if DEBUG_MODE:
            print(f"开始处理视频，总帧数: {total_frames}, 处理间隔: {FRAME_PROCESSING_INTERVAL}")
        
        # 第一阶段：检测和分析阶段
        while True:
            ret, frame = cap.read()
            if not ret:
                if DEBUG_MODE:
                    print(f"已处理完所有帧，总计: {frame_count} 帧，有效处理: {processed_frame_count} 帧")
                break
            
            # 记录每个周期的开始帧
            if frame_count % FRAME_PROCESSING_INTERVAL == 0:
                cycle_start_frames.append(frame_count)
            
            # 根据处理周期决定是否处理当前帧
            if frame_count % FRAME_PROCESSING_INTERVAL != 0:
                frame_count += 1
                continue
            
            processed_frame_count += 1
            
            # 更新处理进度
            current_progress = frame_count / total_frames if total_frames > 0 else 0
            processing_progress[file_name] = current_progress * 0.5  # 第一阶段占总进度的一半
            
            # 保存当前帧为临时图像
            temp_frame_path = os.path.join(temp_dir, f"frame_{frame_count}.jpg")
            try:
                cv2.imwrite(temp_frame_path, frame)
                if DEBUG_MODE and processed_frame_count % 20 == 0:
                    print(f"已保存帧 {frame_count} 到 {temp_frame_path}")
            except Exception as e:
                print(f"保存帧 {frame_count} 失败: {e}")
                if DEBUG_MODE:
                    traceback.print_exc()
                # 继续处理下一帧
                frame_count += 1
                continue
            
            # 使用YOLO模型进行预测
            try:
                results = model(temp_frame_path, conf=0.25, iou=0.45)
            except Exception as e:
                print(f"处理帧 {frame_count} 时YOLO预测失败: {e}")
                if DEBUG_MODE:
                    traceback.print_exc()
                # 继续处理下一帧
                frame_count += 1
                continue
            
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
            
            # 将当前检测周期的主要类别添加到周期类别列表
            if main_class:
                cycle_classes.append(main_class)
            else:
                # 如果当前帧没有检测到任何类别，则视为"未知"
                cycle_classes.append("未知")
            
            # 只保留最近 CONSECUTIVE_THRESHOLD 个检测结果
            if len(cycle_classes) > CONSECUTIVE_THRESHOLD:
                cycle_classes.pop(0)
                cycle_start_frames.pop(0)
            
            # 检查是否连续检测到相同类别
            if len(cycle_classes) == CONSECUTIVE_THRESHOLD:
                # 检查是否所有元素都相同
                if all(cls == cycle_classes[0] for cls in cycle_classes) and cycle_classes[0] != "未知":
                    confirmed_class = cycle_classes[0]
                    # 确定此连续周期覆盖的帧范围
                    start_frame = cycle_start_frames[0]
                    end_frame = frame_count
                    
                    # 将这段帧标记为已确认的类别
                    frame_labels[(start_frame, end_frame)] = confirmed_class
                    
                    if DEBUG_MODE:
                        print(f"帧 {start_frame}-{end_frame} 确认为类别: {confirmed_class}")
            
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
            
            # 打印进度
            if frame_count % 50 == 0:
                print(f"分析阶段: 已处理 {frame_count}/{total_frames} 帧，进度: {(frame_count/total_frames)*100:.2f}%")
            
            frame_count += 1
        
        # 第二阶段：合并重叠标签并处理标签间隙
        merged_frame_labels = {}
        sorted_ranges = sorted(frame_labels.keys())
        
        if sorted_ranges:
            current_range = sorted_ranges[0]
            current_class = frame_labels[current_range]
            
            for next_range in sorted_ranges[1:]:
                next_class = frame_labels[next_range]
                
                # 检查是否有重叠或接近的区间
                if next_range[0] <= current_range[1] + FRAME_PROCESSING_INTERVAL:
                    # 如果类别相同，则合并区间
                    if next_class == current_class:
                        current_range = (current_range[0], next_range[1])
                    else:
                        # 如果类别不同，先存储当前区间，再开始新区间
                        merged_frame_labels[current_range] = current_class
                        current_range = next_range
                        current_class = next_class
                else:
                    # 如果没有重叠，存储当前区间并开始新区间
                    merged_frame_labels[current_range] = current_class
                    current_range = next_range
                    current_class = next_class
            
            # 添加最后一个区间
            merged_frame_labels[current_range] = current_class
        
        if DEBUG_MODE:
            print(f"合并后的标签区间数: {len(merged_frame_labels)}")
            for range_key, class_name in merged_frame_labels.items():
                print(f"帧 {range_key[0]}-{range_key[1]}: {class_name}")
        
        # 计算每个类别的持续时间（基于帧数和FPS）
        class_durations = defaultdict(float)
        
        for (start_frame, end_frame), class_name in merged_frame_labels.items():
            # 计算帧数
            frame_count = end_frame - start_frame + 1
            # 计算持续时间（秒）
            duration = frame_count / fps if fps > 0 else 0
            class_durations[class_name] += duration
        
        # 第三阶段：重新处理视频并添加标签
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 更新处理进度
            current_progress = frame_count / total_frames if total_frames > 0 else 0
            processing_progress[file_name] = 0.5 + current_progress * 0.5  # 第二阶段占总进度的一半
            
            # 找出当前帧应该标注的类别
            current_class = None
            for (start_frame, end_frame), class_name in merged_frame_labels.items():
                if start_frame <= frame_count <= end_frame:
                    current_class = class_name
                    break
            
            # 如果找到了类别，在帧上添加标签
            if current_class:
                # 获取类别对应的颜色
                color = get_color_for_class(current_class)
                
                # 使用工具函数添加文本
                frame = draw_text_with_background(frame, f"类别: {current_class}", (10, 30), 36, color)
            
            # 写入处理后的帧
            out.write(frame)
            
            # 打印进度
            if frame_count % 100 == 0:
                print(f"渲染阶段: 已处理 {frame_count}/{total_frames} 帧，进度: {(frame_count/total_frames)*100:.2f}%")
            
            frame_count += 1
        
        # 表示处理已完成
        processing_progress[file_name] = 1.0
        
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
                'duration': round(class_durations.get(cls_name, 0), 2)  # 使用新计算的持续时间
            })
        
        # 按检测数量排序类别
        class_details.sort(key=lambda x: x['count'], reverse=True)
        
        # 计算平均可信度
        avg_conf = confidence_sum / total_count if total_count > 0 else 0
        
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
        if not os.path.exists(output_path):
            error_msg = f"视频文件未生成: {output_path}"
            print(error_msg)
            return {'error': error_msg}, False
            
        if os.path.getsize(output_path) == 0:
            error_msg = f"生成的视频文件大小为0字节: {output_path}"
            print(error_msg)
            return {'error': error_msg}, False
            
        # 输出结果视频的绝对路径
        print(f"结果视频保存的绝对路径: {os.path.abspath(output_path)}")
        
        if DEBUG_MODE:
            print(f"视频处理完成: {output_path}, 大小: {os.path.getsize(output_path)} 字节")
        
        # 清理临时文件
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
            if DEBUG_MODE:
                print(f"已清理临时目录: {temp_dir}")
        except Exception as e:
            print(f"清理临时目录出错: {e}")
        
        # 返回结果
        return {
            'success': True,
            'detections': all_detections,
            'statistics': statistics,
            'video_info': {
                'width': width,
                'height': height,
                'fps': fps,
                'total_frames': total_frames
            },
            'output_video_path': os.path.abspath(output_path)  # 添加绝对路径到返回结果
        }, True
            
    except Exception as e:
        # 发生错误时清除进度记录
        if file_name in processing_progress:
            del processing_progress[file_name]
        
        # 记录详细的错误信息和堆栈跟踪
        error_traceback = traceback.format_exc()
        print(f"处理视频过程中出错: {str(e)}")
        if DEBUG_MODE:
            print(error_traceback)
        
        # 返回更详细的错误信息
        return {
            'error': f'处理视频过程中出错: {str(e)}',
            'details': error_traceback if DEBUG_MODE else None
        }, False

def get_processing_progress(filename):
    """
    获取指定文件的处理进度
    :param filename: 文件名
    :return: 处理进度(0-1)
    """
    return processing_progress.get(filename, 0)
