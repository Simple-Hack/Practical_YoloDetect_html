from flask import request, jsonify, Blueprint
import os
import uuid
import cv2
from PIL import Image
import numpy as np
from services.detector_service import process_image_detection
from utils.file_utils import cleanup_folder, generate_unique_filename
from config import UPLOAD_FOLDER, OUTPUT_FOLDER, MAX_FILES_PER_FOLDER

# 创建Blueprint
image_routes = Blueprint('image_routes', __name__)

@image_routes.route('/predict', methods=['POST'])
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
        
        # 处理图像检测
        result, success = process_image_detection(input_path)
        
        if not success:
            return jsonify(result), 500
        
        # 保存标注后的图片
        im_array = result['plot_array']
        im = Image.fromarray(im_array[..., ::-1])  # RGB to BGR
        im.save(output_path)
        
        # 确保返回正确的图像URL路径
        image_url = f"/static/outputs/{file_id}_result.jpg"
        
        # 清理文件夹，只保留最新的N个文件
        cleanup_folder(UPLOAD_FOLDER, MAX_FILES_PER_FOLDER)
        cleanup_folder(OUTPUT_FOLDER, MAX_FILES_PER_FOLDER)
        
        return jsonify({
            'success': True,
            'detections': result['detections'],
            'image_url': image_url,
            'statistics': result['statistics']
        })
    
    except Exception as e:
        return jsonify({'error': f'处理过程中出错: {str(e)}'}), 500
