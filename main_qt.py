import sys
from datetime import datetime
import sqlite3
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QPushButton, QLabel, QScrollArea, QDialog,
                            QLineEdit, QSpinBox, QTextEdit, QMessageBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon

class AddHabitDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加新习惯")
        self.setMinimumWidth(300)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 16px;
                margin: 5px;
            }
            QLineEdit, QTextEdit, QSpinBox {
                font-size: 16px;
                padding: 8px;
                margin: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton {
                font-size: 18px;
                padding: 10px;
                margin: 10px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 习惯名称
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("输入习惯名称")
        self.name_input.setMinimumHeight(50)
        layout.addWidget(QLabel("习惯名称:"))
        layout.addWidget(self.name_input)
        
        # 描述
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("描述一下你想培养的习惯...")
        self.description_input.setMinimumHeight(100)
        layout.addWidget(QLabel("描述:"))
        layout.addWidget(self.description_input)
        
        # 目标天数
        self.target_days_input = QSpinBox()
        self.target_days_input.setRange(1, 365)
        self.target_days_input.setValue(21)
        self.target_days_input.setMinimumHeight(50)
        layout.addWidget(QLabel("目标天数:"))
        layout.addWidget(self.target_days_input)
        
        # 确认按钮
        self.confirm_button = QPushButton("添加")
        self.confirm_button.setMinimumHeight(60)
        self.confirm_button.clicked.connect(self.accept)
        layout.addWidget(self.confirm_button)
        
        self.setLayout(layout)

class HabitButton(QPushButton):
    def __init__(self, habit_id, name, streak, target, parent=None):
        super().__init__(parent)
        self.habit_id = habit_id
        self.setText(f"{name}\n连续{streak}天/目标{target}天")
        self.setMinimumHeight(80)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px;
                text-align: center;
                margin: 8px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("好习惯追踪器")
        self.setMinimumWidth(400)
        
        # 设置应用样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #333333;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QWidget {
                background-color: transparent;
            }
        """)
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 创建布局
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 添加标题
        title = QLabel("好习惯追踪器")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #2196F3; margin: 20px;")
        layout.addWidget(title)
        
        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #f1f1f1;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #888;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical {
                height: 0px;
            }
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        scroll_widget = QWidget()
        self.habits_layout = QVBoxLayout()
        self.habits_layout.setSpacing(10)
        self.habits_layout.setContentsMargins(10, 10, 10, 10)
        scroll_widget.setLayout(self.habits_layout)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # 添加新习惯按钮
        add_button = QPushButton("添加新习惯")
        add_button.clicked.connect(self.show_add_dialog)
        add_button.setMinimumHeight(70)
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px;
                font-size: 20px;
                margin: 10px 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        layout.addWidget(add_button)
        
        main_widget.setLayout(layout)
        
        # 初始化数据库
        self.init_db()
        # 加载习惯
        self.load_habits()
        
        # 设置窗口全屏
        self.showMaximized()
    
    def init_db(self):
        conn = sqlite3.connect('habits.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS habits
                    (id INTEGER PRIMARY KEY,
                     name TEXT NOT NULL,
                     description TEXT,
                     created_at TIMESTAMP,
                     target_days INTEGER DEFAULT 21,
                     current_streak INTEGER DEFAULT 0,
                     last_check_in TIMESTAMP)''')
        conn.commit()
        conn.close()
    
    def load_habits(self):
        # 清除现有的习惯按钮
        for i in reversed(range(self.habits_layout.count())): 
            self.habits_layout.itemAt(i).widget().setParent(None)
        
        # 从数据库加载习惯
        conn = sqlite3.connect('habits.db')
        c = conn.cursor()
        c.execute('SELECT id, name, current_streak, target_days FROM habits')
        habits = c.fetchall()
        conn.close()
        
        # 添加习惯按钮
        for habit in habits:
            habit_id, name, streak, target = habit
            button = HabitButton(habit_id, name, streak, target)
            button.clicked.connect(lambda checked, x=habit_id: self.check_in(x))
            self.habits_layout.addWidget(button)
    
    def show_add_dialog(self):
        dialog = AddHabitDialog(self)
        if dialog.exec():
            name = dialog.name_input.text()
            description = dialog.description_input.toPlainText()
            target_days = dialog.target_days_input.value()
            
            if name:
                conn = sqlite3.connect('habits.db')
                c = conn.cursor()
                c.execute('''INSERT INTO habits (name, description, created_at, target_days)
                            VALUES (?, ?, ?, ?)''',
                         (name, description, datetime.now(), target_days))
                conn.commit()
                conn.close()
                
                self.load_habits()
                QMessageBox.information(self, "成功", "新习惯添加成功！")
    
    def check_in(self, habit_id):
        conn = sqlite3.connect('habits.db')
        c = conn.cursor()
        now = datetime.now()
        
        # 获取习惯信息
        c.execute('SELECT last_check_in, current_streak FROM habits WHERE id = ?', (habit_id,))
        habit = c.fetchone()
        
        if habit:
            last_check_in = datetime.fromisoformat(habit[0]) if habit[0] else None
            current_streak = habit[1]
            
            # 更新连续天数
            if last_check_in:
                time_diff = now - last_check_in
                if time_diff.days <= 1:
                    current_streak += 1
                else:
                    current_streak = 1
            else:
                current_streak = 1
            
            # 更新数据库
            c.execute('''UPDATE habits 
                        SET last_check_in = ?, current_streak = ?
                        WHERE id = ?''',
                     (now.isoformat(), current_streak, habit_id))
            conn.commit()
            
            msg = QMessageBox(self)
            msg.setWindowTitle("打卡成功")
            msg.setText(f"已连续打卡 {current_streak} 天！")
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                }
                QMessageBox QLabel {
                    color: #333;
                    font-size: 18px;
                    padding: 20px;
                }
                QMessageBox QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 10px 20px;
                    font-size: 16px;
                    min-width: 100px;
                }
            """)
            msg.exec()
        
        conn.close()
        self.load_habits()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用 Fusion 风格，在移动设备上表现更好
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
