from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import argparse
import sys
import os
from routes.image_routes import image_routes
from routes.video_routes import video_routes
from models.model_loader import load_model
from utils.video_utils import is_port_available, find_available_port, normalize_path
from config import OUTPUT_FOLDER, DEBUG_MODE

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 注册蓝图
app.register_blueprint(image_routes)
app.register_blueprint(video_routes)

@app.route('/static/outputs/<path:filename>')
def serve_output(filename):
    """
    提供输出文件的静态访问，适当设置MIME类型
    """
    # 修复路径问题，使用normalize_path确保路径分隔符一致并检查目录存在
    file_path = normalize_path(os.path.join(OUTPUT_FOLDER, filename))
    
    if DEBUG_MODE:
        print(f"尝试提供静态文件: {file_path}")
        print(f"文件是否存在: {os.path.exists(file_path)}")
        if os.path.exists(file_path):
            print(f"文件大小: {os.path.getsize(file_path)} 字节")
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return jsonify({'error': f'文件不存在: {filename}'}), 404
    
    # 根据文件扩展名设置正确的MIME类型
    mime_type = None
    if filename.lower().endswith('.mp4'):
        mime_type = 'video/mp4'
    elif filename.lower().endswith('.webm'):
        mime_type = 'video/webm'
    elif filename.lower().endswith('.ogg'):
        mime_type = 'video/ogg'
    elif filename.lower().endswith(('.jpg', '.jpeg')):
        mime_type = 'image/jpeg'
    elif filename.lower().endswith('.png'):
        mime_type = 'image/png'
    
    # 使用send_from_directory提供文件，添加conditional=True支持断点续传和范围请求
    return send_from_directory(OUTPUT_FOLDER, filename, mimetype=mime_type, as_attachment=False, conditional=True)

@app.route('/direct_video/<path:filename>')
def serve_direct_video(filename):
    """
    直接提供视频文件访问，支持断点续传
    """
    # 构建完整的绝对路径
    file_path = normalize_path(os.path.join(OUTPUT_FOLDER, filename))
    
    if DEBUG_MODE:
        print(f"尝试提供视频文件: {file_path}")
        print(f"文件是否存在: {os.path.exists(file_path)}")
        if os.path.exists(file_path):
            print(f"文件大小: {os.path.getsize(file_path)} 字节")
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return jsonify({'error': f'视频文件不存在: {filename}'}), 404
    
    # 获取文件的MIME类型
    mime_type = 'video/mp4'
    if filename.lower().endswith('.webm'):
        mime_type = 'video/webm'
    elif filename.lower().endswith('.ogg'):
        mime_type = 'video/ogg'
    
    if DEBUG_MODE:
        print(f"提供视频文件: 目录={OUTPUT_FOLDER}, 文件名={filename}, MIME类型={mime_type}")
    
    # 支持断点续传和范围请求
    return send_from_directory(OUTPUT_FOLDER, filename, mimetype=mime_type, as_attachment=False, conditional=True)

def main():
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
    
    # 输出静态资源目录的绝对路径
    outputs_dir = os.path.abspath(OUTPUT_FOLDER)
    print(f"视频输出目录绝对路径: {outputs_dir}")
    
    try:
        app.run(debug=DEBUG_MODE, host='0.0.0.0', port=port)
    except OSError as e:
        print(f"启动服务器时出错: {e}")
        print("可能的原因：")
        print("1. 端口已被占用")
        print("2. 没有足够的权限绑定到该端口")
        print(f"请尝试使用不同的端口: python {sys.argv[0]} --port <端口号>")
        sys.exit(1)

if __name__ == '__main__':
    main()
