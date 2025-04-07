from flask import request, jsonify, Blueprint, send_file, send_from_directory, current_app
import os
import uuid
from services.video_service import process_video_detection, get_processing_progress
from utils.file_utils import cleanup_folder, generate_unique_filename
from utils.video_utils import convert_video_format, check_video_validity
from config import UPLOAD_FOLDER, OUTPUT_FOLDER, MAX_FILES_PER_FOLDER, DEBUG_MODE

# 创建Blueprint
video_routes = Blueprint('video_routes', __name__)

@video_routes.route('/progress', methods=['GET'])
def get_progress():
    """获取文件处理进度"""
    filename = request.args.get('filename', '')
    if not filename:
        return jsonify({'error': '未提供文件名'}), 400
    
    # 返回处理进度
    progress = get_processing_progress(filename)
    return jsonify({'progress': progress})

@video_routes.route('/predict_video', methods=['POST'])
def predict_video():
    if 'file' not in request.files:
        return jsonify({'error': '没有上传视频文件'}), 400
    
    try:
        file = request.files['file']
        file_name = file.filename
        
        # 创建唯一文件名
        file_id = str(uuid.uuid4())
        input_path = os.path.normpath(os.path.join(UPLOAD_FOLDER, f"{file_id}.mp4"))
        output_path = os.path.normpath(os.path.join(OUTPUT_FOLDER, f"{file_id}_result.mp4"))
        
        # 保存上传的视频
        file.save(input_path)
        
        if DEBUG_MODE:
            print(f"已保存上传的视频到 {input_path}, 大小: {os.path.getsize(input_path)} 字节")
        
        # 处理视频检测
        result, success = process_video_detection(input_path, output_path, file_id, file_name)
        
        if not success:
            return jsonify(result), 500
        
        # 设置默认视频URL - 使用绝对URL路径而非相对路径
        video_url = f"/direct_video/{file_id}_result.mp4"  # 使用direct_video路由
        
        # 检查原始MP4是否有效
        mp4_valid = check_video_validity(output_path)
        
        if not mp4_valid:
            if DEBUG_MODE:
                print("生成的MP4视频无效，尝试使用其他编码方法重新生成")
            
            # 尝试重新编码成更通用的MP4
            fallback_mp4_path = os.path.normpath(os.path.join(OUTPUT_FOLDER, f"{file_id}_result_mpeg4.mp4"))
            mp4_success, fallback_path = convert_video_format(output_path, fallback_mp4_path, 'mp4')
            
            if mp4_success and check_video_validity(fallback_path):
                video_url = f"/direct_video/{file_id}_result_mpeg4.mp4"
                if DEBUG_MODE:
                    print(f"使用重编码后的MP4格式: {fallback_path}")
        
        # 无论原始MP4是否有效，都尝试生成WebM版本作为备用
        webm_output_path = os.path.normpath(os.path.join(OUTPUT_FOLDER, f"{file_id}_result.webm"))
        webm_success, webm_path = convert_video_format(output_path, webm_output_path, 'webm')
        
        # 如果WebM转换成功，优先使用WebM
        if webm_success and check_video_validity(webm_path):
            video_url = f"/direct_video/{file_id}_result.webm"
            if DEBUG_MODE:
                print(f"使用WebM格式视频: {webm_path}")
        
        # 清理文件夹，只保留最新的N个文件
        cleanup_folder(UPLOAD_FOLDER, MAX_FILES_PER_FOLDER)
        cleanup_folder(OUTPUT_FOLDER, MAX_FILES_PER_FOLDER)
        
        # 添加视频URL和原始视频URL到结果中 - 使用绝对路径格式
        result['video_url'] = video_url
        # 添加多种格式作为备用
        result['video_formats'] = {
            'mp4': f"/direct_video/{file_id}_result.mp4",
            'mpeg4': f"/direct_video/{file_id}_result_mpeg4.mp4" if mp4_success else None,
            'webm': f"/direct_video/{file_id}_result.webm" if webm_success else None,
        }
        
        # 添加视频文件相对URL用于前端直接嵌入
        result['embed_url'] = f"/static/outputs/{file_id}_result.mp4"
        
        # 输出HTML加载结果视频的绝对路径
        base_url = request.host_url.rstrip('/')
        html_video_path = f"{base_url}{video_url}"
        print(f"HTML加载结果视频的绝对路径: {html_video_path}")
        
        # 验证所有视频文件是否确实存在 - 使用绝对路径检查
        if DEBUG_MODE:
            for format_key, url in result['video_formats'].items():
                if url:
                    # 获取文件名部分
                    filename = url.split('/')[-1]
                    file_path = os.path.join(OUTPUT_FOLDER, filename)
                    exists = os.path.exists(file_path)
                    print(f"检查视频文件: {file_path}, 存在: {exists}, 大小: {os.path.getsize(file_path) if exists else 0} 字节")
        
        return jsonify(result)
    
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"处理视频过程中出错: {str(e)}")
        if DEBUG_MODE:
            print(error_traceback)
        
        return jsonify({
            'error': f'处理视频过程中出错: {str(e)}',
            'details': error_traceback if DEBUG_MODE else None
        }), 500

@video_routes.route('/direct_video/<path:filename>')
def serve_video_with_mime(filename):
    """
    提供视频文件下载，并设置正确的MIME类型
    """
    # 使用规范化的路径处理
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    file_path = os.path.normpath(file_path)
    
    if DEBUG_MODE:
        print(f"尝试提供视频文件: {file_path}")
        print(f"文件是否存在: {os.path.exists(file_path)}")
        if os.path.exists(file_path):
            print(f"文件大小: {os.path.getsize(file_path)} 字节")
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return jsonify({'error': f'视频文件不存在: {filename}'}), 404
    
    # 根据扩展名设置正确的MIME类型
    mime_type = 'video/mp4'  # 默认
    if filename.endswith('.webm'):
        mime_type = 'video/webm'
    elif filename.endswith('.ogg'):
        mime_type = 'video/ogg'
    
    # 直接使用OUTPUT_FOLDER作为根目录
    return send_from_directory(OUTPUT_FOLDER, filename, mimetype=mime_type, as_attachment=False, conditional=True)
