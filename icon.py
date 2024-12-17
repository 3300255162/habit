from PIL import Image, ImageDraw, ImageFont
import os

# 创建一个 512x512 的图像
size = 512
image = Image.new('RGB', (size, size), 'white')
draw = ImageDraw.Draw(image)

# 绘制圆形背景
circle_color = '#4CAF50'  # 绿色
draw.ellipse([10, 10, size-10, size-10], fill=circle_color)

# 添加文字
try:
    font = ImageFont.truetype('simhei.ttf', 200)
except:
    font = ImageFont.load_default()

text = '习'
text_color = 'white'

# 获取文字大小
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]

# 计算文字位置（居中）
x = (size - text_width) / 2
y = (size - text_height) / 2

# 绘制文字
draw.text((x, y), text, fill=text_color, font=font)

# 保存图像
image.save('icon.png')
