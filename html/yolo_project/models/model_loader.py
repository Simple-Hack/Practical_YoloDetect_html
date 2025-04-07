from ultralytics import YOLO
from config import DEBUG_MODE

# 全局模型变量
model_car_inside_detection = None

def load_model(model_path='./models/car_inside_detect.pt'):
    """
    加载YOLO模型
    :param model_path: 模型路径
    :return: 成功返回True，失败返回False
    """
    global model_car_inside_detection
    try:
        # 使用ultralytics库加载YOLO模型
        model_car_inside_detection = YOLO(model_path)
        if DEBUG_MODE:
            print(f"成功加载模型: {model_path}")
        return True
    except Exception as e:
        print(f"模型加载失败: {e}")
        return False

def get_model():
    """
    获取已加载的模型
    :return: 已加载的模型实例，如果未加载则返回None
    """
    global model_car_inside_detection
    if model_car_inside_detection is None:
        load_model()
    return model_car_inside_detection

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
