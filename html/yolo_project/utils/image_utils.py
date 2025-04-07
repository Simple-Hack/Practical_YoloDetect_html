import cv2
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from config import FONT_PATHS, DEBUG_MODE

def get_color_for_class(class_name):
    """
    根据类别名生成唯一的颜色
    :param class_name: 类别名称
    :return: BGR颜色元组
    """
    # 使用类名的哈希值来确保相同类名总是得到相同颜色
    hash_value = hash(class_name) % 0xFFFFFF
    # 转换为BGR颜色格式
    r = hash_value & 0xFF
    g = (hash_value >> 8) & 0xFF
    b = (hash_value >> 16) & 0xFF
    # 确保颜色不会太暗
    r = max(r, 100)
    g = max(g, 100)
    b = max(b, 100)
    return (b, g, r)  # OpenCV使用BGR格式

def draw_text_with_background(frame, text, position, font_size=36, color=None):
    """
    在图像上绘制带背景的文本，支持中文
    :param frame: OpenCV图像
    :param text: 要绘制的文本
    :param position: 文本位置(x, y)
    :param font_size: 字体大小
    :param color: 文本颜色(BGR格式)，默认为None则使用白色
    :return: 绘制文本后的图像
    """
    if color is None:
        color = (255, 255, 255)  # 默认白色
    
    try:
        # 将OpenCV图像转换为PIL图像以支持中文
        img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        
        # 尝试加载中文字体
        font = None
        for path in FONT_PATHS:
            try:
                if os.path.exists(path):
                    font = ImageFont.truetype(path, font_size)
                    if DEBUG_MODE:
                        print(f"成功加载字体: {path}")
                    break
            except Exception as e:
                if DEBUG_MODE:
                    print(f"加载字体 {path} 失败: {e}")
                continue
        
        if font is None:
            # 如果没有找到系统字体，尝试使用PIL默认字体
            font = ImageFont.load_default()
            if DEBUG_MODE:
                print("使用PIL默认字体")
        
        # 计算文本区域大小，为背景绘制做准备
        text_bbox = draw.textbbox(position, text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # 绘制半透明背景
        background_color = (0, 0, 0, 128)  # 黑色半透明
        background_position = (position[0] - 5, position[1] - 5, 
                              position[0] + text_width + 5, position[1] + text_height + 5)
        draw.rectangle(background_position, fill=background_color)
        
        # 首先绘制黑色边框使文本更清晰
        for offset_x, offset_y in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            draw.text((position[0] + offset_x, position[1] + offset_y), text, 
                    fill=(0, 0, 0), font=font)
        
        # 然后绘制彩色文本
        draw.text(position, text, fill=color[::-1], font=font)  # PIL使用RGB而非BGR
        
        # 将PIL图像转回OpenCV格式
        return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        
    except Exception as e:
        if DEBUG_MODE:
            print(f"绘制中文文本出错: {e}")
            import traceback
            traceback.print_exc()
        
        # 如果中文渲染失败，退回到OpenCV的英文渲染
        cv2.putText(
            frame, 
            text, 
            position, 
            cv2.FONT_HERSHEY_SIMPLEX, 
            font_size / 30,  # 调整OpenCV字体大小比例 
            color, 
            2
        )
        return frame
