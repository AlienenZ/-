<div align="center">

# 课堂行为检测系统

### Classroom Behavior Detection System

<p>
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PyQt5-5.15-green?logo=qt&logoColor=white" alt="PyQt5">
  <img src="https://img.shields.io/badge/YOLO-v26-orange?logo=ultralytics&logoColor=white" alt="YOLO">
  <img src="https://img.shields.io/badge/OpenCV-4.x-red?logo=opencv&logoColor=white" alt="OpenCV">
  <img src="https://img.shields.io/badge/SQLite-3-blue" alt="SQLite">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</p>

<p>
  基于 <strong>YOLO26n 轻量化模型</strong> + <strong>PyQt5 现代深色界面</strong> 构建的课堂行为智能检测系统<br>
  支持实时摄像头监控、图片检测、视频录制与多角色用户管理
</p>

---


</div>

## 功能特性

<table>
<tr>
<td width="50%">

### 智能检测

- **举手识别** — `raising_hand`
- **阅读识别** — `reading`
- **书写识别** — `writing`
- **玩手机识别** — `using_phone`

</td>
<td width="50%">

### 系统管理

- 多角色权限（管理员 / 教师）
- PBKDF2-SHA256 密码加密存储
- 用户增删改查与角色变更
- 登录日志审计追踪

</td>
</tr>
<tr>
<td>

### 检测模式

- 图片检测（支持 PNG/JPG/BMP）
- 实时摄像头检测（多摄像头选择）
- 视频录制保存（AVI 格式）
- 检测结果可视化叠加

</td>
<td>

### 界面设计

- 深色科技主题（暗蓝配色）
- 侧边栏导航 + 卡片式布局
- 渐变登录界面 + 毛玻璃卡片
- 全局 QSS 样式一致性

</td>
</tr>
</table>


## 项目结构

```
design/
├── main.py                 # 应用入口 · 主窗口逻辑 · 检测引擎
├── main_window_ui.py       # 主窗口 UI 布局（侧边栏 + 卡片）
├── user_management.py      # 用户数据库 · 登录对话框 · 用户管理
├── styles.py               # 全局深色主题样式表 · 颜色常量
├── train.py                # YOLO26 模型训练脚本
├── users.db                # SQLite 用户数据库
├── login_history.log       # 登录审计日志
├── README.MD               # 项目文档
│
├── dataset/                # 训练数据集
│   ├── dataset.yaml        # 数据集配置文件
│   ├── images/             # 标注图片（train/val/test）
│   └── labels/             # YOLO 格式标注文件
│
├── runs/                   # 模型训练输出
│   └── detect/             # 检测模型权重
│
├── video_records/          # 摄像头录制视频存储
└── .venv/                  # Python 虚拟环境
```

## 技术架构

```
┌──────────────────────────────────────────────────────────┐
│                    PyQt5 应用层                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ 登录模块  │  │ 主窗口   │  │ 用户管理  │  │ 日志审计  │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────────┘ │
│       │              │              │                      │
│  ┌────▼──────────────▼──────────────▼──────────────────┐  │
│  │              styles.py (QSS 全局主题)                │  │
│  └─────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────┤
│                    业务逻辑层                              │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │ YOLO26 推理   │  │ OpenCV 图像   │  │ 用户认证       │  │
│  │ (ultralytics) │  │ 处理管线      │  │ (PBKDF2+Salt) │  │
│  └──────┬───────┘  └──────┬───────┘  └───────┬────────┘  │
├─────────┼──────────────────┼──────────────────┼───────────┤
│         │           数据层                    │            │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼────────┐  │
│  │ best.pt 权重  │  │ 视频/图片文件 │  │ SQLite 数据库  │  │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
└──────────────────────────────────────────────────────────┘
```

## 快速开始

### 环境要求

| 依赖 | 版本 | 说明 |
|------|------|------|
| Python | 3.10+ | 推荐 3.10/3.11 |
| PyTorch | 2.0+ | CUDA 版本（GPU 加速） |
| PyQt5 | 5.15 | GUI 框架 |
| ultralytics | latest | YOLO26 推理引擎 |
| OpenCV | 4.x | 图像/视频处理 |

### 安装步骤

```bash
# 1. 克隆项目
git clone <repository-url>
cd design

# 2. 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate    # Linux/macOS

# 3. 安装依赖
pip install PyQt5 ultralytics opencv-python torch torchvision

# 4. 启动系统
python main.py
```

### 默认账户

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | `admin` | `admin123` |

> 首次运行自动创建管理员账户，登录后可在「系统 → 用户管理」中添加教师账户。

## 使用指南

### 图片检测

1. 点击侧边栏 **「加载图片」** 按钮
2. 选择本地图片文件（PNG/JPG/BMP）
3. 系统自动调用 YOLO26 模型进行推理
4. 检测框叠加显示在图片上，结果列表展示在底部面板

### 摄像头检测

1. 点击侧边栏 **「启动摄像头」** 按钮
2. 如有多个摄像头，从下拉列表选择
3. 实时检测画面在 OpenCV 窗口中显示
4. 视频自动录制保存至 `video_records/` 目录
5. 按 **Q** 键停止监控

### 用户管理（仅管理员）

1. 菜单栏 → 系统 → 用户管理
2. 支持添加用户、删除用户、修改角色
3. 角色分为 `admin`（管理员）和 `teacher`（教师）

## 模型训练

```bash
# 确保数据集结构正确
dataset/
├── dataset.yaml
├── images/train/
├── images/val/
├── labels/train/
└── labels/val/

# 开始训练
python train.py
```

**训练参数：**

| 参数 | 值 | 说明 |
|------|-----|------|
| 基础模型 | `yolo26n.pt` | YOLO26 纳米级模型 |
| 训练轮数 | `120` | 可根据数据量调整 |
| 图像尺寸 | `640×640` | 输入分辨率 |
| 批次大小 | `16` | 受 GPU 显存影响 |
| 早停轮数 | `40` | 防止过拟合 |
| 优化器 | `MuSGD` | YOLO26 专用优化器 |

训练完成后，最优权重保存在 `runs/detect/classroom_model/weights/best.pt`。

## 配色方案

系统采用深色科技主题，配色定义在 `styles.py` 中：

| 用途 | 色值 | 预览 |
|------|------|------|
| 主背景 | `#1a2332` | ![#1a2332](https://via.placeholder.com/16/1a2332/1a2332.png) |
| 卡片背景 | `#1e2d3d` | ![#1e2d3d](https://via.placeholder.com/16/1e2d3d/1e2d3d.png) |
| 侧边栏 | `#0d1520` | ![#0d1520](https://via.placeholder.com/16/0d1520/0d1520.png) |
| 强调色 | `#29b6f6` | ![#29b6f6](https://via.placeholder.com/16/29b6f6/29b6f6.png) |
| 成功绿 | `#66bb6a` | ![#66bb6a](https://via.placeholder.com/16/66bb6a/66bb6a.png) |
| 警告橙 | `#ffa726` | ![#ffa726](https://via.placeholder.com/16/ffa726/ffa726.png) |
| 错误红 | `#ef5350` | ![#ef5350](https://via.placeholder.com/16/ef5350/ef5350.png) |

## 许可证

本项目基于 MIT License 开源，仅供学习与研究使用。

---

<div align="center">

**课堂行为检测系统** · 基于 YOLO26 + PyQt5 构建

</div>
