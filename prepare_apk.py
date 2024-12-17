import os
import shutil

# 创建新文件夹
apk_dir = 'habit_apk'
if not os.path.exists(apk_dir):
    os.makedirs(apk_dir)

# 需要复制的文件
files_to_copy = [
    'main_kivy.py',  # 将被重命名为 main.py
    'buildozer.spec',
    'icon.png',
    'requirements.txt'
]

# 复制文件
for file in files_to_copy:
    if file == 'main_kivy.py':
        shutil.copy2(file, os.path.join(apk_dir, 'main.py'))
    else:
        shutil.copy2(file, os.path.join(apk_dir, file))

print("Files prepared successfully!")
