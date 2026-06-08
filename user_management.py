import sqlite3
import hashlib
import os
from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QMessageBox,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QComboBox, QFrame, QGraphicsDropShadowEffect,
                             QWidget, QApplication)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor
from styles import Colors


class UserDB:
    def __init__(self, db_path='users.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()
        self._init_admin()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'student'
            )
        ''')
        self.conn.commit()

    def _init_admin(self):
        self.cursor.execute("SELECT id FROM users WHERE role='admin'")
        if not self.cursor.fetchone():
            self.add_user('admin', 'admin123', 'admin')

    def _hash_password(self, password, salt=None):
        if salt is None:
            salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt + key

    def add_user(self, username, password, role='student'):
        salt = os.urandom(32)
        pwd_hash = self._hash_password(password, salt)
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, pwd_hash, role)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, username, password):
        self.cursor.execute(
            "SELECT id, password_hash, role FROM users WHERE username=?",
            (username,)
        )
        row = self.cursor.fetchone()
        if row:
            uid, stored_hash, role = row
            salt = stored_hash[:32]
            new_hash = salt + hashlib.pbkdf2_hmac(
                'sha256', password.encode('utf-8'), salt, 100000
            )
            if new_hash == stored_hash:
                return {'id': uid, 'username': username, 'role': role}
        return None

    def get_all_users(self):
        self.cursor.execute("SELECT id, username, role FROM users")
        return self.cursor.fetchall()

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        self.conn.commit()

    def update_role(self, user_id, new_role):
        self.cursor.execute("UPDATE users SET role=? WHERE id=?", (new_role, user_id))
        self.conn.commit()

    def close(self):
        self.conn.close()


# ══════════════════════════════════════════════════════════
#  现代登录对话框
# ══════════════════════════════════════════════════════════
class LoginDialog(QDialog):
    def __init__(self, user_db):
        super().__init__()
        self.user_db = user_db
        self.user_info = None
        self.setWindowTitle('课堂行为检测系统 · 登录')
        self.setFixedSize(460, 520)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {Colors.BG_DARK}, stop:1 #0a2a43);
            }}
        """)

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(40, 20, 40, 30)
        mainLayout.setSpacing(0)

        # ── 标题区 ──
        iconLabel = QLabel("\U0001F3EB")
        iconLabel.setAlignment(Qt.AlignCenter)
        iconLabel.setStyleSheet("font-size: 48px; background: transparent; padding: 10px;")
        mainLayout.addWidget(iconLabel)

        titleLabel = QLabel("课堂行为检测系统")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setStyleSheet(f"""
            QLabel {{
                color: {Colors.ACCENT};
                font-size: 22px;
                font-weight: bold;
                background: transparent;
                padding: 8px 0 2px 0;
            }}
        """)
        mainLayout.addWidget(titleLabel)

        subtitleLabel = QLabel("Classroom Behavior Detection System")
        subtitleLabel.setAlignment(Qt.AlignCenter)
        subtitleLabel.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_DIM};
                font-size: 12px;
                background: transparent;
                padding-bottom: 28px;
            }}
        """)
        mainLayout.addWidget(subtitleLabel)

        # ── 登录卡片 ──
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_CARD};
                border-radius: 16px;
                border: 1px solid {Colors.BORDER};
            }}
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 8)
        card.setGraphicsEffect(shadow)

        cardLayout = QVBoxLayout(card)
        cardLayout.setContentsMargins(28, 28, 28, 24)
        cardLayout.setSpacing(16)

        # 用户名
        userLabel = QLabel("\U0001F464  用户名")
        userLabel.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 12px;
                font-weight: bold;
                background: transparent;
                padding-left: 2px;
            }}
        """)
        cardLayout.addWidget(userLabel)

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText('请输入用户名')
        self.username_edit.setMinimumHeight(44)
        self.username_edit.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.BG_INPUT};
                color: {Colors.TEXT_PRIMARY};
                border: 2px solid {Colors.BORDER};
                border-radius: 10px;
                padding: 10px 16px;
                font-size: 15px;
            }}
            QLineEdit:focus {{
                border-color: {Colors.ACCENT};
            }}
        """)
        cardLayout.addWidget(self.username_edit)

        # 密码
        pwdLabel = QLabel("\U0001F512  密码")
        pwdLabel.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 12px;
                font-weight: bold;
                background: transparent;
                padding-left: 2px;
            }}
        """)
        cardLayout.addWidget(pwdLabel)

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText('请输入密码')
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setMinimumHeight(44)
        self.password_edit.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.BG_INPUT};
                color: {Colors.TEXT_PRIMARY};
                border: 2px solid {Colors.BORDER};
                border-radius: 10px;
                padding: 10px 16px;
                font-size: 15px;
            }}
            QLineEdit:focus {{
                border-color: {Colors.ACCENT};
            }}
        """)
        self.password_edit.returnPressed.connect(self.login)
        cardLayout.addWidget(self.password_edit)

        cardLayout.addSpacing(8)

        # 登录按钮
        self.login_btn = QPushButton('登  录')
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setMinimumHeight(48)
        self.login_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {Colors.ACCENT_DARK}, stop:1 {Colors.ACCENT});
                color: #ffffff;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
                letter-spacing: 4px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {Colors.ACCENT}, stop:1 {Colors.ACCENT_HOVER});
            }}
            QPushButton:pressed {{
                background: {Colors.ACCENT_DARK};
            }}
        """)
        self.login_btn.clicked.connect(self.login)
        cardLayout.addWidget(self.login_btn)

        mainLayout.addWidget(card)
        mainLayout.addStretch()

        # 底部提示
        hintLabel = QLabel("默认管理员: admin / admin123")
        hintLabel.setAlignment(Qt.AlignCenter)
        hintLabel.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_DIM};
                font-size: 11px;
                background: transparent;
                padding-top: 12px;
            }}
        """)
        mainLayout.addWidget(hintLabel)

    def login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        if not username or not password:
            QMessageBox.warning(self, '提示', '用户名和密码不能为空')
            return
        user = self.user_db.verify_user(username, password)
        if user:
            self.user_info = user
            self.accept()
        else:
            QMessageBox.warning(self, '错误', '用户名或密码错误')

    def register(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        if not username or not password:
            QMessageBox.warning(self, '提示', '用户名和密码不能为空')
            return
        if self.user_db.add_user(username, password, 'teacher'):
            QMessageBox.information(self, '成功', '注册成功，请登录')
        else:
            QMessageBox.warning(self, '失败', '注册失败，用户名可能已存在')


# ══════════════════════════════════════════════════════════
#  现代用户管理对话框
# ══════════════════════════════════════════════════════════
class UserManageDialog(QDialog):
    def __init__(self, user_db):
        super().__init__()
        self.user_db = user_db
        self.setWindowTitle('用户管理')
        self.setMinimumSize(680, 480)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {Colors.BG_MAIN};
            }}
        """)

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(24, 20, 24, 20)
        mainLayout.setSpacing(16)

        # ── 标题栏 ──
        headerLayout = QHBoxLayout()
        headerLabel = QLabel("\U0001F465  用户管理")
        headerLabel.setStyleSheet(f"""
            QLabel {{
                color: {Colors.ACCENT};
                font-size: 20px;
                font-weight: bold;
                background: transparent;
            }}
        """)
        headerLayout.addWidget(headerLabel)
        headerLayout.addStretch()

        userCount = QLabel(f"共 {len(user_db.get_all_users())} 个用户")
        userCount.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 13px;
                background: transparent;
            }}
        """)
        headerLayout.addWidget(userCount)
        mainLayout.addLayout(headerLayout)

        # ── 表格 ──
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', '用户名', '角色'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {Colors.BG_CARD};
                alternate-background-color: {Colors.BG_MAIN};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER};
                border-radius: 10px;
                font-size: 13px;
                selection-background-color: {Colors.BG_SELECTED};
                padding: 4px;
            }}
            QHeaderView::section {{
                background-color: {Colors.SIDEBAR_BG};
                color: {Colors.ACCENT};
                border: none;
                border-bottom: 2px solid {Colors.ACCENT};
                padding: 12px 8px;
                font-weight: bold;
                font-size: 13px;
            }}
        """)
        self.refresh_table()
        mainLayout.addWidget(self.table)

        # ── 操作栏 ──
        opFrame = QFrame()
        opFrame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_CARD};
                border-radius: 10px;
                border: 1px solid {Colors.BORDER};
            }}
        """)
        opLayout = QHBoxLayout(opFrame)
        opLayout.setContentsMargins(16, 12, 16, 12)
        opLayout.setSpacing(10)

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText('新用户名')
        self.username_edit.setMinimumHeight(38)
        self.username_edit.setStyleSheet(self._input_style())

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText('密码')
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setMinimumHeight(38)
        self.password_edit.setStyleSheet(self._input_style())

        self.role_combo = QComboBox()
        self.role_combo.addItems(['teacher', 'admin'])
        self.role_combo.setMinimumHeight(38)
        self.role_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {Colors.BG_INPUT};
                color: {Colors.TEXT_PRIMARY};
                border: 2px solid {Colors.BORDER};
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 13px;
                min-width: 90px;
            }}
            QComboBox:focus {{
                border-color: {Colors.ACCENT};
            }}
            QComboBox QAbstractItemView {{
                background-color: {Colors.BG_CARD};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER};
                selection-background-color: {Colors.ACCENT};
            }}
        """)

        add_btn = QPushButton('添加用户')
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setMinimumHeight(38)
        add_btn.setStyleSheet(self._button_style(Colors.ACCENT))
        add_btn.clicked.connect(self.add_user)

        del_btn = QPushButton('删除选中')
        del_btn.setCursor(Qt.PointingHandCursor)
        del_btn.setMinimumHeight(38)
        del_btn.setStyleSheet(self._button_style(Colors.ERROR))
        del_btn.clicked.connect(self.delete_user)

        save_role_btn = QPushButton('修改角色')
        save_role_btn.setCursor(Qt.PointingHandCursor)
        save_role_btn.setMinimumHeight(38)
        save_role_btn.setStyleSheet(self._button_style(Colors.WARNING))
        save_role_btn.clicked.connect(self.change_role)

        opLayout.addWidget(self.username_edit, 2)
        opLayout.addWidget(self.password_edit, 2)
        opLayout.addWidget(self.role_combo, 1)
        opLayout.addWidget(add_btn)
        opLayout.addWidget(del_btn)
        opLayout.addWidget(save_role_btn)

        mainLayout.addWidget(opFrame)

    def refresh_table(self):
        users = self.user_db.get_all_users()
        self.table.setRowCount(len(users))
        for i, (uid, uname, role) in enumerate(users):
            idItem = QTableWidgetItem(str(uid))
            idItem.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, idItem)

            nameItem = QTableWidgetItem(uname)
            nameItem.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, nameItem)

            roleItem = QTableWidgetItem(role)
            roleItem.setTextAlignment(Qt.AlignCenter)
            if role == 'admin':
                roleItem.setForeground(QColor(Colors.ACCENT))
            else:
                roleItem.setForeground(QColor(Colors.TEXT_SECONDARY))
            self.table.setItem(i, 2, roleItem)

    def add_user(self):
        uname = self.username_edit.text().strip()
        pwd = self.password_edit.text()
        role = self.role_combo.currentText()
        if not uname or not pwd:
            QMessageBox.warning(self, '提示', '用户名和密码不能为空')
            return
        if self.user_db.add_user(uname, pwd, role):
            QMessageBox.information(self, '成功', '用户添加成功')
            self.username_edit.clear()
            self.password_edit.clear()
            self.refresh_table()
        else:
            QMessageBox.warning(self, '失败', '添加失败，用户名可能已存在')

    def delete_user(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, '提示', '请选择要删除的用户')
            return
        uid = int(self.table.item(row, 0).text())
        self.user_db.delete_user(uid)
        self.refresh_table()

    def change_role(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, '提示', '请选择用户')
            return
        uid = int(self.table.item(row, 0).text())
        new_role = self.role_combo.currentText()
        self.user_db.update_role(uid, new_role)
        self.refresh_table()

    def _input_style(self):
        return f"""
            QLineEdit {{
                background-color: {Colors.BG_INPUT};
                color: {Colors.TEXT_PRIMARY};
                border: 2px solid {Colors.BORDER};
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border-color: {Colors.ACCENT};
            }}
        """

    def _button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                opacity: 0.85;
                filter: brightness(1.1);
            }}
            QPushButton:pressed {{
                opacity: 0.7;
            }}
        """
