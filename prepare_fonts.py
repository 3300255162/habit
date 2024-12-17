import os
import shutil
import sys
from urllib.request import urlretrieve

def prepare_fonts():
    fonts_dir = os.path.join(os.path.dirname(__file__), 'fonts')
    os.makedirs(fonts_dir, exist_ok=True)
    
    # 目标字体文件路径
    simhei_path = os.path.join(fonts_dir, 'simhei.ttf')
    
    # 如果字体文件已存在，跳过
    if os.path.exists(simhei_path):
        print("字体文件已存在，跳过下载")
        return
    
    # 首先尝试从 Windows 系统复制
    if sys.platform == 'win32':
        windows_font = 'C:/Windows/Fonts/simhei.ttf'
        if os.path.exists(windows_font):
            print("从 Windows 系统复制字体文件...")
            shutil.copy2(windows_font, simhei_path)
            return
    
    # 如果无法从系统复制，则下载开源替代字体
    print("下载开源字体...")
    font_url = "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansSC-Regular.otf"
    try:
        urlretrieve(font_url, simhei_path)
        print("字体下载完成")
    except Exception as e:
        print(f"下载字体失败: {e}")
        print("请手动将 simhei.ttf 复制到 fonts 目录")

if __name__ == '__main__':
    prepare_fonts()
