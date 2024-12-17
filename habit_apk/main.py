# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase
from datetime import datetime
import sqlite3
import os

# 注册中文字体
if os.name == 'nt':  # Windows
    LabelBase.register(name='SimHei', 
                      fn_regular='C:/Windows/Fonts/simhei.ttf')
else:  # Linux/Mac
    try:
        LabelBase.register(name='SimHei', 
                          fn_regular='/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf')
    except:
        pass

# 设置默认字体
from kivy.config import Config
Config.set('kivy', 'default_font', ['SimHei', 'data/fonts/DroidSansFallback.ttf'])

class AddHabitPopup(Popup):
    def __init__(self, add_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = '添加新习惯'
        self.size_hint = (0.9, 0.9)
        self.add_callback = add_callback

        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # 习惯名称输入
        layout.add_widget(Label(text='习惯名称:', size_hint_y=None, height=dp(30), font_name='SimHei'))
        self.name_input = TextInput(multiline=False, size_hint_y=None, height=dp(40), font_name='SimHei')
        layout.add_widget(self.name_input)

        # 描述输入
        layout.add_widget(Label(text='描述:', size_hint_y=None, height=dp(30), font_name='SimHei'))
        self.description_input = TextInput(multiline=True, size_hint_y=None, height=dp(100), font_name='SimHei')
        layout.add_widget(self.description_input)

        # 目标天数输入
        layout.add_widget(Label(text='目标天数:', size_hint_y=None, height=dp(30), font_name='SimHei'))
        self.target_days_input = TextInput(
            text='21', multiline=False, input_filter='int',
            size_hint_y=None, height=dp(40), font_name='SimHei'
        )
        layout.add_widget(self.target_days_input)

        # 确认按钮
        confirm_button = Button(
            text='添加',
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex('#2196F3'),
            font_name='SimHei'
        )
        confirm_button.bind(on_release=self.add_habit)
        layout.add_widget(confirm_button)

        self.content = layout

    def add_habit(self, instance):
        name = self.name_input.text.strip()
        if name:
            description = self.description_input.text.strip()
            try:
                target_days = int(self.target_days_input.text)
            except ValueError:
                target_days = 21

            self.add_callback(name, description, target_days)
            self.dismiss()

class HabitButton(Button):
    def __init__(self, habit_id, name, streak, target, **kwargs):
        super().__init__(**kwargs)
        self.habit_id = habit_id
        self.text = f'{name}\n连续{streak}天/目标{target}天'
        self.background_color = get_color_from_hex('#4CAF50')
        self.size_hint_y = None
        self.height = dp(80)
        self.font_name = 'SimHei'

class HabitTrackerApp(App):
    def build(self):
        # 设置窗口大小和背景色
        Window.clearcolor = get_color_from_hex('#F5F5F5')
        
        # 创建主布局
        self.main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(10)
        )

        # 添加标题
        title = Label(
            text='好习惯追踪器',
            size_hint_y=None,
            height=dp(50),
            color=get_color_from_hex('#2196F3'),
            font_size=dp(24),
            font_name='SimHei'
        )
        self.main_layout.add_widget(title)

        # 创建滚动视图
        scroll = ScrollView()
        self.habits_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None
        )
        self.habits_layout.bind(minimum_height=self.habits_layout.setter('height'))
        scroll.add_widget(self.habits_layout)
        self.main_layout.add_widget(scroll)

        # 添加新习惯按钮
        add_button = Button(
            text='添加新习惯',
            size_hint_y=None,
            height=dp(60),
            background_color=get_color_from_hex('#2196F3'),
            font_name='SimHei'
        )
        add_button.bind(on_release=self.show_add_dialog)
        self.main_layout.add_widget(add_button)

        # 初始化数据库
        self.init_db()
        # 加载习惯
        self.load_habits()

        return self.main_layout

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
        self.habits_layout.clear_widgets()
        
        conn = sqlite3.connect('habits.db')
        c = conn.cursor()
        c.execute('SELECT id, name, current_streak, target_days FROM habits')
        habits = c.fetchall()
        conn.close()

        for habit in habits:
            habit_id, name, streak, target = habit
            button = HabitButton(habit_id, name, streak, target)
            button.bind(on_release=lambda btn: self.check_in(btn.habit_id))
            self.habits_layout.add_widget(button)

    def show_add_dialog(self, instance):
        popup = AddHabitPopup(add_callback=self.add_habit)
        popup.open()

    def add_habit(self, name, description, target_days):
        conn = sqlite3.connect('habits.db')
        c = conn.cursor()
        c.execute('''INSERT INTO habits (name, description, created_at, target_days)
                    VALUES (?, ?, ?, ?)''',
                 (name, description, datetime.now(), target_days))
        conn.commit()
        conn.close()
        self.load_habits()

    def check_in(self, habit_id):
        conn = sqlite3.connect('habits.db')
        c = conn.cursor()
        now = datetime.now()
        
        c.execute('SELECT last_check_in, current_streak FROM habits WHERE id = ?', (habit_id,))
        habit = c.fetchone()
        
        if habit:
            last_check_in = datetime.fromisoformat(habit[0]) if habit[0] else None
            current_streak = habit[1]
            
            if last_check_in:
                days_diff = (now - last_check_in).days
                if days_diff == 0:  # 今天已经打卡
                    popup = Popup(
                        title='提示',
                        content=Label(
                            text='今天已经打卡了！',
                            font_name='SimHei'
                        ),
                        size_hint=(0.8, 0.3)
                    )
                    popup.open()
                    return
                elif days_diff == 1:  # 连续打卡
                    current_streak += 1
                else:  # 中断了连续打卡
                    current_streak = 1
            else:  # 第一次打卡
                current_streak = 1
            
            # 更新打卡记录
            c.execute('''UPDATE habits 
                        SET last_check_in = ?, current_streak = ?
                        WHERE id = ?''', (now, current_streak, habit_id))
            conn.commit()
            
            # 显示打卡成功提示
            popup = Popup(
                title='打卡成功',
                content=Label(
                    text=f'已连续打卡 {current_streak} 天！',
                    font_name='SimHei'
                ),
                size_hint=(0.8, 0.3)
            )
            popup.open()
            
            # 重新加载习惯列表
            self.load_habits()
        
        conn.close()

if __name__ == '__main__':
    HabitTrackerApp().run()
