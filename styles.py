"""
现代深色主题样式模块 - 课堂行为检测系统
提供统一的 QSS 样式和颜色常量
"""

# ── 颜色常量 ──────────────────────────────────────────────
class Colors:
    BG_DARK       = "#0f1923"   # 最深背景
    BG_MAIN       = "#1a2332"   # 主背景
    BG_CARD       = "#1e2d3d"   # 卡片背景
    BG_INPUT      = "#253446"   # 输入框背景
    BG_HOVER      = "#2a3f55"   # 悬停背景
    BG_SELECTED   = "#0d47a1"   # 选中行
    ACCENT        = "#29b6f6"   # 主强调色 (亮蓝)
    ACCENT_HOVER  = "#4fc3f7"   # 强调色悬停
    ACCENT_DARK   = "#0288d1"   # 强调色深
    SUCCESS       = "#66bb6a"   # 成功绿
    WARNING       = "#ffa726"   # 警告橙
    ERROR         = "#ef5350"   # 错误红
    TEXT_PRIMARY   = "#e0e0e0"   # 主文字
    TEXT_SECONDARY = "#90a4ae"   # 次要文字
    TEXT_DIM       = "#546e7a"   # 暗淡文字
    BORDER         = "#2a3f55"  # 边框
    SCROLLBAR      = "#37474f"  # 滚动条
    SIDEBAR_BG     = "#0d1520"  # 侧边栏背景
    SIDEBAR_HOVER  = "#162230"  # 侧边栏悬停


# ── 应用主样式 ────────────────────────────────────────────
APP_STYLESHEET = f"""
/* ========== 全局 ========== */
QWidget {{
    font-family: "Microsoft YaHei UI", "Segoe UI", sans-serif;
    font-size: 13px;
    color: {Colors.TEXT_PRIMARY};
    background-color: {Colors.BG_MAIN};
}}

QMainWindow {{
    background-color: {Colors.BG_DARK};
}}

/* ========== 菜单栏 ========== */
QMenuBar {{
    background-color: {Colors.SIDEBAR_BG};
    color: {Colors.TEXT_PRIMARY};
    border-bottom: 1px solid {Colors.BORDER};
    padding: 2px 0;
    font-size: 13px;
}}
QMenuBar::item {{
    padding: 6px 14px;
    border-radius: 4px;
    margin: 2px 1px;
}}
QMenuBar::item:selected {{
    background-color: {Colors.BG_HOVER};
}}
QMenu {{
    background-color: {Colors.BG_CARD};
    border: 1px solid {Colors.BORDER};
    border-radius: 6px;
    padding: 4px;
}}
QMenu::item {{
    padding: 8px 28px;
    border-radius: 4px;
}}
QMenu::item:selected {{
    background-color: {Colors.ACCENT};
    color: #ffffff;
}}

/* ========== 按钮 ========== */
QPushButton {{
    background-color: {Colors.ACCENT};
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 14px;
    font-weight: bold;
    min-height: 20px;
}}
QPushButton:hover {{
    background-color: {Colors.ACCENT_HOVER};
}}
QPushButton:pressed {{
    background-color: {Colors.ACCENT_DARK};
}}
QPushButton:disabled {{
    background-color: {Colors.BG_INPUT};
    color: {Colors.TEXT_DIM};
}}

/* ========== 输入框 ========== */
QLineEdit {{
    background-color: {Colors.BG_INPUT};
    color: {Colors.TEXT_PRIMARY};
    border: 2px solid {Colors.BORDER};
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 14px;
    selection-background-color: {Colors.ACCENT};
}}
QLineEdit:focus {{
    border-color: {Colors.ACCENT};
}}
QLineEdit:hover {{
    border-color: {Colors.ACCENT_DARK};
}}

/* ========== 文本编辑框 ========== */
QTextEdit, QPlainTextEdit {{
    background-color: {Colors.BG_CARD};
    color: {Colors.TEXT_PRIMARY};
    border: 1px solid {Colors.BORDER};
    border-radius: 8px;
    padding: 10px;
    font-size: 13px;
    selection-background-color: {Colors.ACCENT};
}}

/* ========== 标签 ========== */
QLabel {{
    color: {Colors.TEXT_PRIMARY};
    background: transparent;
}}

/* ========== 组合框 ========== */
QComboBox {{
    background-color: {Colors.BG_INPUT};
    color: {Colors.TEXT_PRIMARY};
    border: 2px solid {Colors.BORDER};
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
    min-width: 100px;
}}
QComboBox:focus {{
    border-color: {Colors.ACCENT};
}}
QComboBox::drop-down {{
    border: none;
    width: 30px;
}}
QComboBox QAbstractItemView {{
    background-color: {Colors.BG_CARD};
    color: {Colors.TEXT_PRIMARY};
    border: 1px solid {Colors.BORDER};
    border-radius: 6px;
    selection-background-color: {Colors.ACCENT};
    padding: 4px;
}}

/* ========== 表格 ========== */
QTableWidget {{
    background-color: {Colors.BG_CARD};
    alternate-background-color: {Colors.BG_MAIN};
    color: {Colors.TEXT_PRIMARY};
    gridline-color: {Colors.BORDER};
    border: 1px solid {Colors.BORDER};
    border-radius: 8px;
    font-size: 13px;
    selection-background-color: {Colors.BG_SELECTED};
}}
QHeaderView::section {{
    background-color: {Colors.SIDEBAR_BG};
    color: {Colors.ACCENT};
    border: none;
    border-bottom: 2px solid {Colors.ACCENT};
    padding: 10px 8px;
    font-weight: bold;
    font-size: 13px;
}}
QTableCornerButton::section {{
    background-color: {Colors.SIDEBAR_BG};
    border: none;
}}

/* ========== 滚动条 ========== */
QScrollBar:vertical {{
    background: {Colors.BG_MAIN};
    width: 10px;
    border-radius: 5px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {Colors.SCROLLBAR};
    border-radius: 5px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {Colors.ACCENT};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    background: {Colors.BG_MAIN};
    height: 10px;
    border-radius: 5px;
    margin: 0;
}}
QScrollBar::handle:horizontal {{
    background: {Colors.SCROLLBAR};
    border-radius: 5px;
    min-width: 30px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {Colors.ACCENT};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}

/* ========== 状态栏 ========== */
QStatusBar {{
    background-color: {Colors.SIDEBAR_BG};
    color: {Colors.TEXT_SECONDARY};
    border-top: 1px solid {Colors.BORDER};
    font-size: 12px;
    padding: 4px 10px;
}}

/* ========== 消息框 ========== */
QMessageBox {{
    background-color: {Colors.BG_CARD};
}}
QMessageBox QLabel {{
    color: {Colors.TEXT_PRIMARY};
    font-size: 14px;
}}
QMessageBox QPushButton {{
    min-width: 80px;
    min-height: 32px;
}}

/* ========== 输入对话框 ========== */
QInputDialog {{
    background-color: {Colors.BG_CARD};
}}
QInputDialog QLabel {{
    color: {Colors.TEXT_PRIMARY};
}}
"""


# ── 登录对话框专用样式 ────────────────────────────────────
LOGIN_STYLESHEET = f"""
QDialog {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {Colors.BG_DARK}, stop:1 #0a2a43);
}}
QLabel {{
    color: {Colors.TEXT_PRIMARY};
    background: transparent;
    font-size: 14px;
}}
QLineEdit {{
    background-color: {Colors.BG_INPUT};
    color: {Colors.TEXT_PRIMARY};
    border: 2px solid {Colors.BORDER};
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 15px;
    selection-background-color: {Colors.ACCENT};
}}
QLineEdit:focus {{
    border-color: {Colors.ACCENT};
}}
QPushButton {{
    background-color: {Colors.ACCENT};
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 12px 32px;
    font-size: 15px;
    font-weight: bold;
}}
QPushButton:hover {{
    background-color: {Colors.ACCENT_HOVER};
}}
QPushButton:pressed {{
    background-color: {Colors.ACCENT_DARK};
}}
"""
