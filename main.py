from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
import sqlite3
import os

class HabitTrackerApp(App):
    def build(self):
        # 创建主布局
        self.main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # 添加标题
        title = Label(
            text='Habit Tracker',
            size_hint_y=None,
            height=dp(50),
            color=get_color_from_hex('#2196F3'),
            font_size=dp(24)
        )
        self.main_layout.add_widget(title)
        
        # 添加测试按钮
        test_button = Button(
            text='Test Button',
            size_hint_y=None,
            height=dp(60),
            background_color=get_color_from_hex('#4CAF50')
        )
        self.main_layout.add_widget(test_button)
        
        return self.main_layout

if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')
    HabitTrackerApp().run()
