import os
import shutil
import sys
from urllib.request import urlretrieve
import hashlib
import time

def download_with_retry(url, target_path, max_retries=3):
    for i in range(max_retries):
        try:
            print(f"尝试下载 {url} (第 {i+1} 次)")
            urlretrieve(url, target_path)
            return True
        except Exception as e:
            print(f"下载失败: {e}")
            if i < max_retries - 1:
                time.sleep(2)  # 等待2秒后重试
            continue
    return False

def verify_file(file_path):
    """验证文件是否是有效的字体文件"""
    if not os.path.exists(file_path):
        return False
    
    # 检查文件大小（至少应该有100KB）
    if os.path.getsize(file_path) < 100 * 1024:
        return False
    
    # 检查文件头部是否是常见的字体格式
    with open(file_path, 'rb') as f:
        header = f.read(4)
        return header.startswith(b'\x00\x01\x00\x00') or header.startswith(b'OTTO') or header.startswith(b'true') or header.startswith(b'ttcf')

def prepare_fonts():
    fonts_dir = os.path.join(os.path.dirname(__file__), 'fonts')
    os.makedirs(fonts_dir, exist_ok=True)
    
    # 目标字体文件路径
    simhei_path = os.path.join(fonts_dir, 'simhei.ttf')
    
    # 如果字体文件已存在且有效，跳过
    if os.path.exists(simhei_path) and verify_file(simhei_path):
        print("字体文件已存在且有效，跳过下载")
        return True
    
    # 尝试从系统复制
    system_fonts = []
    if sys.platform == 'win32':
        system_fonts.append('C:/Windows/Fonts/simhei.ttf')
    elif sys.platform == 'darwin':  # macOS
        system_fonts.append('/Library/Fonts/Arial Unicode.ttf')
    elif sys.platform == 'linux':
        system_fonts.extend([
            '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
            '/usr/share/fonts/truetype/arphic/uming.ttc'
        ])
    
    for font in system_fonts:
        if os.path.exists(font) and verify_file(font):
            print(f"从系统复制字体文件: {font}")
            shutil.copy2(font, simhei_path)
            return True
    
    # 如果无法从系统复制，则下载开源替代字体
    print("尝试下载开源字体...")
    font_urls = [
        "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansSC-Regular.otf",
        "https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/SimplifiedChinese/SourceHanSansSC-Regular.otf"
    ]
    
    for url in font_urls:
        if download_with_retry(url, simhei_path):
            if verify_file(simhei_path):
                print("字体下载并验证成功")
                return True
            else:
                print("下载的文件不是有效的字体文件")
                os.remove(simhei_path)
    
    print("无法获取有效的字体文件")
    return False

if __name__ == '__main__':
    if prepare_fonts():
        print("字体准备完成")
        sys.exit(0)
    else:
        print("字体准备失败")
        sys.exit(1)
