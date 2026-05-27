#!/usr/bin/env python3
"""生成插件图标"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    """创建指定尺寸的图标"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 渐变背景 (简化为纯色)
    # 计算圆角矩形
    radius = int(size * 0.15)
    
    # 绘制圆角矩形背景
    for x in range(size):
        for y in range(size):
            # 检查是否在圆角矩形内
            in_rect = True
            
            # 四个角的检查
            corners = [
                (radius, radius),  # 左上
                (size - radius, radius),  # 右上
                (radius, size - radius),  # 左下
                (size - radius, size - radius)  # 右下
            ]
            
            for cx, cy in corners:
                if ((x < radius and y < radius and (x, y) == (cx - radius, cy - radius)) or
                    (x >= size - radius and y < radius) or
                    (x < radius and y >= size - radius) or
                    (x >= size - radius and y >= size - radius)):
                    # 简化处理
                    pass
            
            # 渐变色
            ratio = (x + y) / (2 * size)
            r = int(102 + (118 - 102) * ratio)  # 667eea -> 764ba2
            g = int(126 + (75 - 126) * ratio)
            b = int(234 + (162 - 234) * ratio)
            
            draw.point((x, y), fill=(r, g, b, 255))
    
    # 绘制文字
    try:
        font_large = ImageFont.truetype("arial.ttf", int(size * 0.25))
        font_small = ImageFont.truetype("arial.ttf", int(size * 0.1))
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 1688 文字
    text = "1688"
    bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = int(size * 0.35)
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font_large)
    
    # 保存
    img.save(output_path, 'PNG')
    print(f"生成: {output_path}")

if __name__ == "__main__":
    icons_dir = os.path.dirname(os.path.abspath(__file__))
    
    create_icon(16, os.path.join(icons_dir, "icon16.png"))
    create_icon(48, os.path.join(icons_dir, "icon48.png"))
    create_icon(128, os.path.join(icons_dir, "icon128.png"))
    
    print("图标生成完成!")
