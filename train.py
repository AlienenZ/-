import os
from ultralytics import YOLO

def start_training():
    # 初始化 YOLO26 纳米级检测模型
    model = YOLO("yolo26n.pt")

    # 配置文件路径检查
    yaml_path = os.path.join(os.getcwd(), "dataset", "dataset.yaml")
    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"找不到数据集配置文件: {yaml_path}，请核对第二步的文件夹结构！")

    print("--- 开始训练 YOLO26 课堂行为检测模型 ---")
    
    # 3. 启动模型训练
    model.train(
        data=yaml_path,        # 指定数据集配置文件
        epochs=120,            # 训练轮数
        imgsz=640,             # 输入图像尺寸
        batch=16,              # 批次大小
        workers=0,             # 数据加载线程数
        patience=40,           # 早停机制：如果连续20轮验证集指标没有提升，则提前停止训练
        cache='disk',          # 启用数据缓存加速训练
        close_mosaic=0,        # 训练前不使用马赛克数据增强，提升初始阶段的收敛速度
        optimizer='MuSGD',     # 采用 YOLO26 特有的 MuSGD 混合优化器，收敛更稳定
        device='0',            # GPU训练
        project='runs/detect', # 训练输出根目录
        name='classroom_model' # 本次训练结果保存的文件夹名称
    )
    print("训练已完成！最优权重文件已保存至 runs/detect/classroom_model/weights/best.pt")

if __name__ == "__main__":
    start_training()