# -*- coding: utf-8 -*-
"""
现代主窗口 UI - 课堂行为检测系统
侧边栏导航 + 卡片式布局
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from styles import Colors


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setMinimumSize(900, 650)

        font = QtGui.QFont("Microsoft YaHei UI", 10)
        MainWindow.setFont(font)

        # ── 中央部件 ──
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.mainHLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.mainHLayout.setContentsMargins(0, 0, 0, 0)
        self.mainHLayout.setSpacing(0)

        # ==================== 侧边栏 ====================
        self.sidebar = QtWidgets.QFrame(self.centralWidget)
        self.sidebar.setFixedWidth(220)
        self.sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.SIDEBAR_BG};
                border-right: 1px solid {Colors.BORDER};
            }}
        """)

        self.sidebarLayout = QtWidgets.QVBoxLayout(self.sidebar)
        self.sidebarLayout.setContentsMargins(16, 20, 16, 20)
        self.sidebarLayout.setSpacing(6)

        # Logo / 标题区
        self.titleLabel = QtWidgets.QLabel(self.sidebar)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setStyleSheet(f"""
            QLabel {{
                color: {Colors.ACCENT};
                font-size: 18px;
                font-weight: bold;
                padding: 20px 0;
                border-bottom: 1px solid {Colors.BORDER};
                margin-bottom: 16px;
            }}
        """)
        self.titleLabel.setText("课堂行为\n检测系统")
        self.sidebarLayout.addWidget(self.titleLabel)

        # 用户信息
        self.userLabel = QtWidgets.QLabel(self.sidebar)
        self.userLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.userLabel.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 12px;
                padding: 6px 0;
                margin-bottom: 12px;
            }}
        """)
        self.sidebarLayout.addWidget(self.userLabel)

        # 侧边栏按钮
        self.btnLoadImage = self._create_sidebar_button("  \U0001F5BC  加载图片")
        self.btnStartCamera = self._create_sidebar_button("  \U0001F4F7  启动摄像头")
        self.btnVideoRecord = self._create_sidebar_button("  \U0001F3AC  视频录制")
        self.btnHistory = self._create_sidebar_button("  \U0001F4CB  检测记录")

        self.sidebarLayout.addWidget(self.btnLoadImage)
        self.sidebarLayout.addWidget(self.btnStartCamera)
        self.sidebarLayout.addWidget(self.btnVideoRecord)
        self.sidebarLayout.addWidget(self.btnHistory)
        self.sidebarLayout.addStretch()

        # 底部版本信息
        self.versionLabel = QtWidgets.QLabel(self.sidebar)
        self.versionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.versionLabel.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_DIM};
                font-size: 11px;
                padding-top: 10px;
                border-top: 1px solid {Colors.BORDER};
            }}
        """)
        self.versionLabel.setText("v2.0 · YOLO26")
        self.sidebarLayout.addWidget(self.versionLabel)

        self.mainHLayout.addWidget(self.sidebar)

        # ==================== 右侧内容区 ====================
        self.contentArea = QtWidgets.QWidget(self.centralWidget)
        self.contentLayout = QtWidgets.QVBoxLayout(self.contentArea)
        self.contentLayout.setContentsMargins(24, 20, 24, 16)
        self.contentLayout.setSpacing(16)

        # ── 顶部状态卡片 ──
        self.statsFrame = QtWidgets.QFrame()
        self.statsFrame.setFixedHeight(80)
        self.statsFrame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a3a5c, stop:1 {Colors.BG_CARD});
                border-radius: 12px;
                border: 1px solid {Colors.BORDER};
            }}
        """)
        self.statsLayout = QtWidgets.QHBoxLayout(self.statsFrame)
        self.statsLayout.setContentsMargins(24, 10, 24, 10)

        self.statDetection = self._create_stat_item("检测状态", "就绪")
        self.statCount = self._create_stat_item("检测目标", "0")
        self.statModel = self._create_stat_item("模型", "YOLO26n")
        self.statFPS = self._create_stat_item("FPS", "--")

        self.statsLayout.addWidget(self.statDetection)
        self.statsLayout.addWidget(self._create_stat_divider())
        self.statsLayout.addWidget(self.statCount)
        self.statsLayout.addWidget(self._create_stat_divider())
        self.statsLayout.addWidget(self.statModel)
        self.statsLayout.addWidget(self._create_stat_divider())
        self.statsLayout.addWidget(self.statFPS)
        self.contentLayout.addWidget(self.statsFrame)

        # ── 图像显示卡片 ──
        self.imageCard = QtWidgets.QFrame()
        self.imageCard.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_CARD};
                border-radius: 12px;
                border: 1px solid {Colors.BORDER};
            }}
        """)
        self.imageCardLayout = QtWidgets.QVBoxLayout(self.imageCard)
        self.imageCardLayout.setContentsMargins(2, 2, 2, 2)

        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLabel.setMinimumHeight(300)
        self.imageLabel.setStyleSheet(f"""
            QLabel {{
                background-color: {Colors.BG_DARK};
                border-radius: 10px;
                color: {Colors.TEXT_DIM};
                font-size: 16px;
                border: 2px dashed {Colors.BORDER};
                padding: 40px;
            }}
        """)
        self.imageLabel.setText("选择图片或启动摄像头开始检测")
        self.imageCardLayout.addWidget(self.imageLabel)
        self.contentLayout.addWidget(self.imageCard, stretch=1)

        # ── 检测结果卡片 ──
        self.resultCard = QtWidgets.QFrame()
        self.resultCard.setMaximumHeight(200)
        self.resultCard.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_CARD};
                border-radius: 12px;
                border: 1px solid {Colors.BORDER};
            }}
        """)
        self.resultCardLayout = QtWidgets.QVBoxLayout(self.resultCard)
        self.resultCardLayout.setContentsMargins(16, 10, 16, 10)

        self.resultTitle = QtWidgets.QLabel("检测结果")
        self.resultTitle.setStyleSheet(f"""
            QLabel {{
                color: {Colors.ACCENT};
                font-size: 14px;
                font-weight: bold;
                padding-bottom: 4px;
            }}
        """)
        self.resultCardLayout.addWidget(self.resultTitle)

        self.resultText = QtWidgets.QTextEdit()
        self.resultText.setReadOnly(True)
        self.resultText.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG_DARK};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER};
                border-radius: 8px;
                padding: 10px;
                font-family: "Cascadia Code", "Consolas", monospace;
                font-size: 13px;
            }}
        """)
        self.resultCardLayout.addWidget(self.resultText)
        self.contentLayout.addWidget(self.resultCard)

        self.mainHLayout.addWidget(self.contentArea)
        MainWindow.setCentralWidget(self.centralWidget)

        # ── 兼容旧接口名 ──
        self.loadImageButton = self.btnLoadImage
        self.startCameraButton = self.btnStartCamera

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

    # ── 辅助方法 ──────────────────────────────────────────
    def _create_sidebar_button(self, text):
        btn = QtWidgets.QPushButton(text)
        btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Colors.TEXT_PRIMARY};
                border: none;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {Colors.SIDEBAR_HOVER};
                color: {Colors.ACCENT};
            }}
            QPushButton:pressed {{
                background-color: {Colors.ACCENT};
                color: #ffffff;
            }}
        """)
        return btn

    def _create_stat_item(self, title, value):
        frame = QtWidgets.QFrame()
        frame.setStyleSheet("background: transparent;")
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        titleLabel = QtWidgets.QLabel(title)
        titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        titleLabel.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 11px;
                background: transparent;
            }}
        """)

        valueLabel = QtWidgets.QLabel(value)
        valueLabel.setAlignment(QtCore.Qt.AlignCenter)
        valueLabel.setStyleSheet(f"""
            QLabel {{
                color: {Colors.ACCENT};
                font-size: 20px;
                font-weight: bold;
                background: transparent;
            }}
        """)
        # 存储引用方便后续更新
        frame._valueLabel = valueLabel

        layout.addWidget(titleLabel)
        layout.addWidget(valueLabel)
        return frame

    def _create_stat_divider(self):
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setStyleSheet(f"color: {Colors.BORDER}; background: transparent;")
        return line
