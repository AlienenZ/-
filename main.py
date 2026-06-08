import os
import logging
from datetime import datetime
import torch
import sys
import cv2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QDialog, QInputDialog,
    QVBoxLayout, QTextEdit, QPushButton, QFrame, QLabel, QHBoxLayout,
    QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QPixmap, QFont, QColor, QImage
from PyQt5.QtCore import Qt, QTimer
from main_window_ui import Ui_MainWindow
from ultralytics import YOLO
import numpy as np
from user_management import UserDB, LoginDialog, UserManageDialog
from styles import Colors, APP_STYLESHEET


class ClassroomBehaviorDetection(QMainWindow, Ui_MainWindow):
    def __init__(self, user_info, user_db):
        super().__init__()
        self.setupUi(self)
        self.user_info = user_info
        self.user_db = user_db

        role_name = '管理员' if user_info['role'] == 'admin' else '教师'
        self.setWindowTitle(f'课堂行为检测系统 · {user_info["username"]} ({role_name})')

        self.userLabel.setText(f"\U0001F464 {user_info['username']}  |  {role_name}")

        self.model = YOLO('runs/detect/runs/detect/classroom_model-2/weights/best.pt')

        self.btnLoadImage.clicked.connect(self.load_image)
        self.btnStartCamera.clicked.connect(self.start_camera)

        self.setup_menu()

    def setup_menu(self):
        menubar = self.menuBar()
        system_menu = menubar.addMenu('系统')
        if self.user_info['role'] == 'admin':
            manage_action = system_menu.addAction('用户管理')
            manage_action.triggered.connect(self.open_user_management)
            log_action = system_menu.addAction('查看日志')
            log_action.triggered.connect(self.open_log_viewer)
        system_menu.addAction('退出', self.close)

    def open_user_management(self):
        dialog = UserManageDialog(self.user_db)
        dialog.exec_()

    def open_log_viewer(self):
        try:
            with open('login_history.log', 'r', encoding='utf-8') as f:
                log_content = f.read()
        except FileNotFoundError:
            log_content = "日志文件尚未生成。"
        except Exception as e:
            log_content = f"读取日志出错: {str(e)}"

        dialog = QDialog(self)
        dialog.setWindowTitle('系统日志')
        dialog.resize(650, 450)
        dialog.setStyleSheet(f"background-color: {Colors.BG_MAIN};")

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(16, 16, 16, 16)

        titleLabel = QLabel("\U0001F4CB  系统日志")
        titleLabel.setStyleSheet(f"""
            QLabel {{
                color: {Colors.ACCENT};
                font-size: 18px;
                font-weight: bold;
                background: transparent;
                padding-bottom: 8px;
            }}
        """)
        layout.addWidget(titleLabel)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(log_content)
        text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG_CARD};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER};
                border-radius: 8px;
                padding: 12px;
                font-family: "Cascadia Code", "Consolas", monospace;
                font-size: 12px;
            }}
        """)
        layout.addWidget(text_edit)

        close_btn = QPushButton('关闭')
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setMinimumHeight(40)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ACCENT};
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 8px 24px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Colors.ACCENT_HOVER};
            }}
        """)
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)

        dialog.exec_()

    def load_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "",
            "Images (*.png *.xpm *.jpg *.bmp *.jpeg);;All Files (*)",
            options=options
        )
        if file_name:
            pixmap = QPixmap(file_name)
            self.imageLabel.setStyleSheet(f"""
                QLabel {{
                    background-color: {Colors.BG_DARK};
                    border-radius: 10px;
                    border: 2px solid {Colors.ACCENT};
                    padding: 4px;
                }}
            """)
            self.imageLabel.setPixmap(pixmap.scaled(
                self.imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
            img = cv2.imread(file_name)
            if img is not None:
                self.detect_behavior(img, window_name='Image Detection')

    def get_available_cameras(self, max_tested=5):
        available_cameras = []
        for i in range(max_tested):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
        return available_cameras

    def start_camera(self):
        cameras = self.get_available_cameras()
        if not cameras:
            self.resultText.setText("未检测到任何摄像头！")
            return

        if len(cameras) == 1:
            cam_idx = cameras[0]
        else:
            items = [f"摄像头 (索引 {idx})" for idx in cameras]
            item, ok = QInputDialog.getItem(
                self, "选择摄像头", "请选择要使用的摄像头:", items, 0, False
            )
            if not ok:
                return
            cam_idx = int(item.split("索引 ")[-1].rstrip(")"))

        cap = cv2.VideoCapture(cam_idx)
        if not cap.isOpened():
            self.resultText.setText(f"无法打开摄像头 (索引 {cam_idx})")
            return

        os.makedirs('video_records', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_filename = f"video_records/record_{timestamp}.avi"
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0.0:
            fps = 20.0

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(video_filename, fourcc, fps, (frame_width, frame_height))
        logging.info(f"用户 {self.user_info['username']} 开启了摄像头监控，视频保存在 {video_filename}")

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            self.detect_behavior(frame, window_name='Camera Detection')
            out.write(frame)
            cv2.imshow('Camera Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                logging.info(f"用户 {self.user_info['username']} 关闭了摄像头监控")
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()

    def detect_behavior(self, frame, window_name='Detection'):
        results = self.model(frame)
        boxes = results[0].boxes

        self.resultText.clear()
        if boxes is None or len(boxes) == 0:
            self.resultText.append("未检测到行为")
            self._update_stat(self.statDetection, "就绪")
            self._update_stat(self.statCount, "0")
            return

        xyxy   = boxes.xyxy.cpu().numpy()
        confs  = boxes.conf.cpu().numpy()
        clss   = boxes.cls.cpu().numpy()
        names  = results[0].names

        self._update_stat(self.statDetection, "检测中")
        self._update_stat(self.statCount, str(len(xyxy)))

        for i in range(len(xyxy)):
            x1, y1, x2, y2 = map(int, xyxy[i])
            conf = confs[i]
            cls_id = int(clss[i])
            label = names[cls_id]

            self.resultText.append(f'  {label}: {conf:.2f}  [{x1}, {y1}, {x2}, {y2}]')

            cv2.rectangle(frame, (x1, y1), (x2, y2), (41, 182, 246), 2)
            cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (41, 182, 246), 2)

        if window_name == 'Image Detection':
            cv2.imshow(window_name, frame)

    def _update_stat(self, statFrame, value):
        if hasattr(statFrame, '_valueLabel'):
            statFrame._valueLabel.setText(value)


def main():
    app = QApplication(sys.argv)

    # ── 应用全局样式 ──
    app.setStyleSheet(APP_STYLESHEET)

    # ── 设置全局字体 ──
    font = QFont("Microsoft YaHei UI", 10)
    font.setStyleStrategy(QFont.PreferAntialias)
    app.setFont(font)

    logging.basicConfig(
        filename='login_history.log',
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(message)s',
        encoding='utf-8'
    )

    user_db = UserDB('users.db')
    login = LoginDialog(user_db)
    if login.exec_() == QDialog.Accepted:
        user_info = login.user_info
        logging.info(f"用户登录成功: 用户名={user_info['username']}, 角色={user_info['role']}")
        ex = ClassroomBehaviorDetection(user_info, user_db)
        ex.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
