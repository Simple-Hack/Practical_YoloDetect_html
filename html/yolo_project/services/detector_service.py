from collections import defaultdict
from models.model_loader import get_model, map_class_name
from config import DEBUG_MODE
import traceback

def process_image_detection(image_path):
    """
    处理图像检测任务
    :param image_path: 图像路径
    :return: 检测结果字典
    """
    try:
        # 获取模型
        model = get_model()
        if model is None:
            return {'error': '模型加载失败'}, False
        
        # 使用模型进行预测
        results = model(image_path, conf=0.25, iou=0.45)
        
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
        
        # 统计信息
        statistics = {
            'total_count': total_count,
            'class_count': len(class_stats),  # 检测到的类别数量
            'avg_confidence': avg_conf,
            'max_confidence': max_conf,
            'class_details': class_details  # 各类别详细统计
        }
        
        # 保存图像结果
        for r in results:
            im_array = r.plot()  # 获取绘制后的图像数组
            return {
                'detections': detections,
                'statistics': statistics,
                'plot_array': im_array
            }, True
            
    except Exception as e:
        if DEBUG_MODE:
            print(f"图像检测处理出错: {e}")
            traceback.print_exc()
        return {'error': f'图像检测处理出错: {str(e)}'}, False
