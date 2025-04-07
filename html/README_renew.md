# 驾驶行为检测系统

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)](https://flask.palletsprojects.com/)
[![YOLO](https://img.shields.io/badge/YOLO-v8-yellow)](https://github.com/ultralytics/ultralytics)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5%2B-red)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

一个基于YOLOv8目标检测算法的驾驶行为检测系统，通过深度学习技术实时检测驾驶行为，提供全面的数据分析。本系统同时支持图片和视频处理，适用于驾驶行为监控、安全驾驶培训和驾驶状态分析等场景。

![系统预览](https://via.placeholder.com/800x450.png?text=驾驶行为检测系统界面预览)

## 📌 功能特点

### 核心功能
- **多模态输入**：支持图片(JPG、PNG)和视频文件(MP4、MOV、AVI)上传与分析
- **实时检测**：采用高效的YOLOv8模型进行实时目标检测
- **行为识别**：精确识别多种驾驶行为
- **状态追踪**：持续跟踪视频中的驾驶状态，记录状态持续时间
- **结果可视化**：直观展示检测结果，包括边界框标注和类别标签

### 用户体验
- **拖拽上传**：支持文件拖拽上传，操作便捷
- **进度实时显示**：视频处理过程中实时显示进度
- **响应式设计**：适配不同屏幕尺寸的设备
- **直观操作**：简洁易用的界面设计

### 数据分析
- **多维统计**：自动生成检测总数、类别数、平均可信度等统计数据
- **图表分析**：通过交互式图表展示各类别的检测数量和可信度分布
- **类别详情**：展示每个检测类别的详细信息，包括检出次数和置信度
- **时长分析**：分析视频中各行为的持续时间，评估驾驶风险

## 🔍 检测类别详解

系统可以检测以下主要类别的驾驶行为：

### 驾驶行为类别
- **安全驾驶**：驾驶员专注于道路，双手放在方向盘上的标准驾驶姿势
- **发短信-右手**：驾驶员使用右手发送短信
- **打电话-右手**：驾驶员使用右手打电话
- **发短信-左手**：驾驶员使用左手发送短信
- **打电话-左手**：驾驶员使用左手打电话
- **操作车载无线电**：驾驶员调整或操作车载无线电设备
- **喝饮料**：驾驶员在驾驶过程中喝水或其他饮料
- **向后伸手**：驾驶员将手伸向后排座位
- **整理发型或化妆**：驾驶员在驾驶时整理头发或进行化妆

这些行为类别可以帮助识别和评估驾驶中的注意力分散情况，从而提高道路安全性。

## 💻 技术栈详情

### 前端技术
- **HTML5 / CSS3**：构建现代化的用户界面
- **原生JavaScript**：实现前端交互逻辑和数据处理
- **Chart.js (v3.7+)**：绘制交互式数据可视化图表
- **Font Awesome (v5.15+)**：提供丰富的图标资源
- **响应式设计**：CSS变量和Flexbox/Grid布局

### 后端技术
- **Python 3.8+**：核心编程语言
- **Flask (v2.0+)**：轻量级Web框架
- **Flask-CORS**：处理跨域资源共享
- **OpenCV (cv2)**：图像和视频处理库
- **Ultralytics YOLOv8**：最新版本的YOLO目标检测模型
- **PIL/Pillow**：Python图像处理库
- **NumPy**：科学计算库，用于数组处理
- **FFmpeg**：视频格式转换和处理

## 🚀 安装和使用详解

### 系统要求
- **操作系统**：Windows 10/11, macOS 10.15+, Ubuntu 20.04+
- **处理器**：推荐Intel Core i5/AMD Ryzen 5或更高配置
- **内存**：最低8GB RAM，推荐16GB+
- **存储空间**：至少500MB可用空间
- **Python环境**：Python 3.8或更高版本
- **GPU支持**：NVIDIA GPU + CUDA 11.0+（可选，但推荐用于加速处理）

### 详细安装步骤

1. **克隆代码仓库**：
```bash
git clone https://github.com/yourusername/car-inside-detection.git
cd car-inside-detection
```

2. **创建虚拟环境**（推荐）：
```bash
# 使用venv
python -m venv venv

# 在Windows上激活环境
venv\Scripts\activate

# 在macOS/Linux上激活环境
source venv/bin/activate
```

3. **安装依赖项**：
```bash
pip install -r requirements.txt
```

4. **安装FFMPEG**：
   - **Windows**：
     - 下载[FFMPEG](https://ffmpeg.org/download.html)
     - 解压到合适位置，如C:\ffmpeg
     - 将bin目录添加到系统PATH环境变量
     - 或在44444.py中更新FFMPEG_PATH变量为ffmpeg.exe的完整路径
   
   - **macOS**：
     ```bash
     brew install ffmpeg
     ```
   
   - **Linux**：
     ```bash
     sudo apt update
     sudo apt install ffmpeg
     ```

5. **准备模型文件**：
   - 在项目根目录下创建`models`文件夹
   - 下载预训练的YOLOv8模型文件
   - 将模型文件重命名为`car_inside_detect.pt`并放入models文件夹

6. **创建必要的目录结构**：
```bash
mkdir -p uploads static/outputs temp
```

### 运行服务

1. **启动Flask服务器**：
```bash
python 44444.py
```

2. **指定自定义端口**（可选）：
```bash
python 44444.py --port 8080
```

3. **访问Web界面**：
   - 打开浏览器访问 http://localhost:5050 （或您指定的其他端口）
   - 首次加载页面可能需要几秒钟时间来初始化YOLO模型

## 📊 使用指南

### 上传文件

1. **选择文件方式**：
   - 点击上传区域选择文件
   - 或直接将文件拖拽到上传区域

2. **支持的文件格式**：
   - **图片**：JPG、JPEG、PNG
   - **视频**：MP4、MOV、AVI（推荐使用MP4格式获得最佳兼容性）

3. **文件大小限制**：
   - 图片：最大20MB
   - 视频：最大500MB（建议控制在2-3分钟内以获得较快的处理速度）

### 检测处理

1. **开始检测**：
   - 上传文件后，点击"开始检测"按钮
   - 系统将自动分析上传的文件

2. **处理过程**：
   - 图片检测通常在几秒内完成
   - 视频检测时间取决于视频长度，会显示进度条
   - 请勿关闭浏览器窗口，否则处理将被中断

3. **查看结果**：
   - 检测完成后，系统自动显示结果
   - 对于图片，直接显示标注后的图像
   - 对于视频，显示处理后的视频，可以播放、暂停和拖动进度条

### 结果分析

结果页面分为三个标签页：

1. **检测统计**：
   - 显示总体统计信息，如检测总数和类别数
   - 展示每个类别的详细统计，包括检出次数和置信度
   - 对于视频，还会显示每个行为的持续时间

2. **详细信息**：
   - 按列表形式展示所有检测结果
   - 包括类别名称、检测ID和置信度
   - 对于视频，还会显示检测帧号
   - 支持翻页浏览大量检测结果

3. **图表分析**：
   - 类别检测数量柱状图
   - 类别可信度对比图（平均和最高置信度）
   - 交互式图表，支持悬停查看详细数据

## 📋 项目结构详解

```
car-inside-detection/
│
├── 44444.py              # 后端服务器主程序，包含Flask路由和YOLO处理逻辑
├── 44444.html            # 前端界面HTML文件，包含用户界面和JavaScript交互代码
├── README.md             # 项目说明文档
├── requirements.txt      # Python依赖项列表
│
├── models/               # 模型文件夹
│   └── car_inside_detect.pt  # YOLOv8检测模型
│
├── uploads/              # 上传文件临时存储目录
│   └── ...               # 用户上传的原始文件（系统自动管理）
│
├── static/               # 静态资源目录
│   └── outputs/          # 输出结果目录
│       └── ...           # 处理后的图片和视频（系统自动管理）
│
└── temp/                 # 临时文件目录
    └── ...               # 视频处理过程中的临时文件（系统自动管理）
```

## 🔧 API参考

### 后端API端点

1. **`/predict`** - 处理图片文件
   - **方法**：POST
   - **参数**：
     - `file`：图片文件（multipart/form-data）
   - **返回**：JSON对象，包含检测结果、图像URL和统计信息

2. **`/predict_video`** - 处理视频文件
   - **方法**：POST
   - **参数**：
     - `file`：视频文件（multipart/form-data）
   - **返回**：JSON对象，包含检测结果、视频URL、统计信息和视频信息

3. **`/progress`** - 获取视频处理进度
   - **方法**：GET
   - **参数**：
     - `filename`：正在处理的文件名（URL参数）
   - **返回**：JSON对象，包含当前进度（0到1之间的小数）

### 检测结果格式

1. **图片检测响应**：
```json
{
  "success": true,
  "detections": [
    {
      "class": "安全驾驶",
      "confidence": 0.92,
      "bbox": [100, 150, 300, 400]
    },
    ...
  ],
  "image_url": "/static/outputs/abc123_result.jpg",
  "statistics": {
    "total_count": 3,
    "class_count": 2,
    "avg_confidence": 0.85,
    "max_confidence": 0.92,
    "class_details": [...]
  }
}
```

2. **视频检测响应**：
```json
{
  "success": true,
  "detections": [...],
  "video_url": "/static/outputs/abc123_result.mp4",
  "statistics": {
    "total_count": 120,
    "class_count": 4,
    "avg_confidence": 0.78,
    "max_confidence": 0.95,
    "class_details": [...],
    "total_frames": 450,
    "fps": 30,
    "video_duration": 15
  },
  "video_info": {
    "width": 1280,
    "height": 720,
    "fps": 30,
    "total_frames": 450
  }
}
```

## 🛠️ 开发和定制指南

### 自定义检测模型

1. **使用自定义YOLOv8模型**：
   - 将您训练好的YOLOv8模型(.pt文件)放入models文件夹
   - 修改44444.py中的模型路径：
   ```python
   model_car_inside_detection = YOLO(r'.\models\your_custom_model.pt')
   ```

2. **调整检测参数**：
   - 修改置信度阈值(conf)和IOU阈值(iou)以调整检测灵敏度：
   ```python
   # 在44444.py文件中
   # 提高置信度阈值以减少误检
   results = model(input_path, conf=0.35, iou=0.45)  
   # 或降低置信度以增加检出率
   results = model(input_path, conf=0.20, iou=0.45)  
   ```

### 类别映射自定义

1. **修改类别映射规则**：
   - 编辑`map_class_name`函数以自定义类别映射规则：
   ```python
   def map_class_name(cls_name):
       # 添加新的映射规则
       if cls_name.startswith("打哈欠"):
           return "疲劳驾驶"
       if cls_name.startswith("眨眼"):
           return "疲劳驾驶"
       # 原有逻辑
       if cls_name.startswith("与乘客交谈"):
           return "安全驾驶"
       return cls_name
   ```

### 前端定制

1. **修改界面样式**：
   - 在44444.html中编辑CSS变量以更改颜色方案：
   ```css
   :root {
       --primary-color: #3f51b5; /* 修改主色调 */
       --secondary-color: #4caf50; /* 修改次要色调 */
       /* 其他样式变量 */
   }
   ```

2. **添加新的图表**：
   - 在charts-container中添加新的图表卡片：
   ```html
   <div class="chart-card">
       <div class="chart-title">新增图表</div>
       <div class="chart-container">
           <canvas id="newCustomChart"></canvas>
       </div>
   </div>
   ```
   
   - 在JavaScript中初始化新图表：
   ```javascript
   const newChartCtx = document.getElementById('newCustomChart').getContext('2d');
   // 设置图表配置和数据
   ```

### 系统优化

1. **GPU加速**：
   - 确保已安装CUDA和cuDNN
   - YOLOv8默认使用可用的GPU，无需额外配置

2. **视频处理性能优化**：
   - 调整视频帧采样率，减少处理帧数：
   ```python
   # 在predict_video函数中
   # 例如，每3帧处理1帧
   if frame_count % 3 != 0:
       frame_count += 1
       continue
   ```

3. **内存优化**：
   - 修改MAX_FILES_PER_FOLDER变量控制缓存文件数量：
   ```python
   # 减少保留的文件数量以节省磁盘空间
   MAX_FILES_PER_FOLDER = 3
   ```

## ❓ 故障排除和常见问题

### 安装问题

1. **依赖项安装失败**
   - **问题**：`pip install -r requirements.txt`失败
   - **解决方案**：
     - 尝试逐个安装依赖项：`pip install flask flask-cors opencv-python ultralytics pillow`
     - 检查Python版本是否满足要求（3.8+）
     - 对于Windows用户，某些包可能需要Visual C++构建工具，请安装[Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

2. **CUDA相关错误**
   - **问题**：使用GPU时出现CUDA错误
   - **解决方案**：
     - 确保已安装兼容的CUDA和cuDNN版本
     - 检查GPU驱动是否最新
     - 尝试降级至较旧但稳定的CUDA版本
     - 如问题持续，可在命令行添加参数强制使用CPU：`python 44444.py --device cpu`

### 运行问题

1. **模型加载失败**
   - **问题**：出现"模型加载失败"错误
   - **解决方案**：
     - 确认models文件夹中存在car_inside_detect.pt文件
     - 检查模型文件是否损坏，尝试重新下载
     - 查看日志获取更详细的错误信息

2. **视频处理中断**
   - **问题**：处理较大视频时系统崩溃
   - **解决方案**：
     - 使用较短的视频（建议不超过3分钟）
     - 增加系统可用内存
     - 降低视频分辨率后再上传
     - 检查磁盘空间是否充足

3. **视频无法播放**
   - **问题**：处理后的视频在浏览器中无法播放
   - **解决方案**：
     - 确保已正确安装FFMPEG
     - 尝试使用不同的浏览器（推荐Chrome或Firefox）
     - 检查视频格式，优先使用MP4格式
     - 查看浏览器控制台获取详细错误信息

## 📝 许可证

本项目采用MIT许可证，详情请参阅LICENSE文件。

```
MIT License

Copyright (c) 2023 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 📊 效果展示

### 检测界面
![检测界面](https://via.placeholder.com/800x450.png?text=检测界面)

### 检测结果
![检测结果](https://via.placeholder.com/800x450.png?text=检测结果)

### 统计分析
![统计分析](https://via.placeholder.com/800x450.png?text=统计分析)

## 🔮 未来计划

- 增加实时摄像头检测支持
- 添加批量文件处理功能
- 开发检测结果导出为PDF/CSV功能
- 集成更多数据分析工具
- 支持更多自定义配置选项
- 添加用户账户和历史记录功能

## 🤝 贡献指南

我们欢迎所有形式的贡献，包括但不限于：

1. **提交Issues**：报告bug、提出功能建议或讨论改进意见
2. **提交Pull Requests**：修复bug或实现新功能
3. **改进文档**：完善README或添加使用教程
4. **分享使用案例**：提供项目应用场景和效果

贡献流程：
1. Fork本仓库
2. 创建您的特性分支：`git checkout -b feature/amazing-feature`
3. 提交您的更改：`git commit -m 'Add some amazing feature'`
4. 推送到分支：`git push origin feature/amazing-feature`
5. 开启Pull Request

## 📧 联系方式

如有任何问题或建议，请通过以下方式联系我们：

- **GitHub Issues**：[提交Issue](https://github.com/yourusername/car-inside-detection/issues)
- **电子邮件**：your.email@example.com
- **项目讨论区**：[GitHub Discussions](https://github.com/yourusername/car-inside-detection/discussions)

---

**免责声明**：本系统仅用于教育和研究目的，不应用于任何商业监控或侵犯隐私的场景。使用本系统应遵守当地法律法规。
