import numpy as np
import torch
import os
from PIL import Image, ImageDraw, ImageOps, ImageFont

颜色_mapping = {
    "白色": (255, 255, 255),
    "黑色": (0, 0, 0),
    "红色": (255, 0, 0),
    "绿色": (0, 255, 0),
    "蓝色": (0, 0, 255),
    "黄色": (255, 255, 0),
    "青色": (0, 255, 255),
    "品红": (255, 0, 255),
    "橙色": (255, 165, 0),
    "紫色": (128, 0, 128),
    "粉色": (255, 192, 203),
    "棕色": (160, 85, 15),
    "灰色": (128, 128, 128),
    "浅灰": (211, 211, 211),
    "深灰": (102, 102, 102),
    "橄榄绿": (128, 128, 0),
    "酸橙色": (0, 128, 0),
    "鸭绿色": (0, 128, 128),
    "海军蓝": (0, 0, 128),
    "紫褐色": (128, 0, 0),
    "紫红色": (255, 0, 128),
    "浅绿色": (0, 255, 128),
    "银色": (192, 192, 192),
    "金色": (255, 215, 0),
    "青绿色": (64, 224, 208),
    "淡紫色": (230, 230, 250),
    "蓝紫色": (238, 130, 238),
    "珊瑚红": (255, 127, 80),
    "靛蓝色": (75, 0, 130),    
}

COLORS = ["自定义", "白色", "黑色", "红色", "绿色", "蓝色", "黄色",
          "青色", "品红", "橙色", "紫色", "粉色", "棕色", "灰色",
          "浅灰", "深灰", "橄榄绿", "酸橙色", "鸭绿色", "海军蓝", "紫褐色",
          "紫红色", "浅绿色", "银色", "金色", "青绿色", "淡紫色",
          "蓝紫色", "珊瑚红", "靛蓝色"]

ALIGN_OPTIONS = ["居中", "上", "下"]                 
ROTATE_OPTIONS = ["按文本 居中", "按图像 居中"]
JUSTIFY_OPTIONS = ["居中", "左", "右"]
PERSPECTIVE_OPTIONS = ["上", "下", "左", "右"]

def align_text(align, img_height, text_height, text_pos_y, margins):
    if align == "居中":
        text_plot_y = img_height / 2 - text_height / 2 + text_pos_y
    elif align == "上":
        text_plot_y = 0 + text_pos_y
    elif align == "下":
        text_plot_y = img_height - text_height + text_pos_y
    return text_plot_y

def get_text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)

    # Calculate the text width and height
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    return text_width, text_height

def justify_text(justify, img_width, line_width, margins):
    if justify == "左":
        text_plot_x = 0 + margins
    elif justify == "右":
        text_plot_x = img_width - line_width - margins
    elif justify == "居中":
        text_plot_x = img_width/2 - line_width/2 + margins
    return text_plot_x

def 六进制_to_rgb(六进制_颜色):
    六进制_颜色 = 六进制_颜色.lstrip('#')  # Remove the '#' character, if present
    r = int(六进制_颜色[0:2], 16)
    g = int(六进制_颜色[2:4], 16)
    b = int(六进制_颜色[4:6], 16)
    return (r, g, b)

def get_颜色_values(颜色, 颜色_六进制, 颜色_mapping):
    
    #Get RGB values for the text and background 颜色s.
    if 颜色 == "自定义":
        颜色_rgb = 六进制_to_rgb(颜色_六进制)
    else:
        颜色_rgb = 颜色_mapping.get(颜色, (0, 0, 0))  # Default to 黑色 if the 颜色 is not found
    return 颜色_rgb

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8)) 

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0) 

def draw_masked_text(text_mask, text,
                     font_name, font_size,
                     margins, line_spacing,
                     position_x, position_y, 
                     align, justify,
                     rotation_angle, rotation_options):
    
    # Create the drawing context        
    draw = ImageDraw.Draw(text_mask)

    # Define font settings
    font_folder = "fonts"
    font_file = os.path.join(font_folder, font_name)
    resolved_font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), font_file)
    font = ImageFont.truetype(str(resolved_font_path), size=font_size) 

     # Split the input text into lines
    text_lines = text.split('\n')

    # Calculate the size of the text plus padding for the tallest line
    max_text_width = 0
    max_text_height = 0

    for line in text_lines:
        # Calculate the width and height of the current line
        line_width, line_height = get_text_size(draw, line, font)
 
        line_height = line_height + line_spacing
        max_text_width = max(max_text_width, line_width)
        max_text_height = max(max_text_height, line_height)
    
    # Get the image width and height
    image_width, image_height = text_mask.size
    按图像_居中_x = image_width / 2
    按图像_居中_y = image_height / 2

    text_pos_y = position_y
    sum_text_plot_y = 0
    text_height = max_text_height * len(text_lines)

    for line in text_lines:
        # Calculate the width of the current line
        line_width, _ = get_text_size(draw, line, font)
                            
        # Get the text x and y positions for each line                                     
        text_plot_x = position_x + justify_text(justify, image_width, line_width, margins)
        text_plot_y = align_text(align, image_height, text_height, text_pos_y, margins)
        
        # Add the current line to the text mask
        draw.text((text_plot_x, text_plot_y), line, fill=255, font=font)
        
        text_pos_y += max_text_height  # Move down for the next line
        sum_text_plot_y += text_plot_y     # Sum the y positions

    # Calculate 居中s for rotation
    按文本_居中_x = text_plot_x + max_text_width / 2
    按文本_居中_y = sum_text_plot_y / len(text_lines)

    if rotation_options == "按文本 居中":
        rotated_text_mask = text_mask.rotate(rotation_angle, center=(按文本_居中_x, 按文本_居中_y))
    elif rotation_options == "按图像 居中":    
        rotated_text_mask = text_mask.rotate(rotation_angle, center=(按图像_居中_x, 按图像_居中_y))
    return rotated_text_mask

class Wongkongshuiyin:
    @classmethod
    def INPUT_TYPES(s):
        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]
        
        return {"required": {
                    "背景生成宽度": ("INT", {"default": 512, "min": 64, "max": 20000}),
                    "背景生成高度": ("INT", {"default": 512, "min": 64, "max": 20000}),
                    "text": ("STRING", {"multiline": True, "default": "请输入需要生成的水印文字,本插件字体均为网络公开资源字体，仅供学习交流使用，如需商用请自行更换商用字体，字体存放路径为插件内的fonts文件夹，请咨询抖音：大师兄（AIGC）"}),
                    "选择字体": (file_list,),
                    "字体大小": ("INT", {"default": 50, "min": 1, "max": 1024}),
                    "字体颜色": (COLORS,),
                    "背景颜色": (COLORS,),
                    "竖向位置": (ALIGN_OPTIONS,),
                    "横向位置": (JUSTIFY_OPTIONS,),
                    "文字页边距": ("INT", {"default": 0, "min": -1024, "max": 1024}),
                    "文字行间距": ("INT", {"default": 0, "min": -1024, "max": 1024}),
                    "横向偏移": ("INT", {"default": 0, "min": -20000, "max": 20000}),
                    "竖向偏移": ("INT", {"default": 0, "min": -20000, "max": 20000}),
                    "旋转角度": ("FLOAT", {"default": 0.0, "min": -360.0, "max": 360.0, "step": 0.1}),
                    "旋转中心": (ROTATE_OPTIONS,),
                },
                "optional": {
                    "字体_颜色_六进制": ("STRING", {"multiline": False, "default": "#000000"}),
                    "背景_颜色_六进制": ("STRING", {"multiline": False, "default": "#000000"}),
                    "输入原图": ("IMAGE", {}),
                }
        }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("输出图像",)
    FUNCTION = "draw_text"
    CATEGORY = "WUKONG/文本"
    def draw_text(self, 背景生成宽度,背景生成高度, text,
                  选择字体, 字体大小, 字体颜色,
                  背景颜色,
                  文字页边距,文字行间距,
                  横向偏移, 竖向偏移,
                  竖向位置, 横向位置,
                  旋转角度, 旋转中心,
                  字体_颜色_六进制='#000000', 背景_颜色_六进制='#000000', 输入原图=None):
        # Get RGB values for the text and background 颜色s
        text_颜色 = get_颜色_values(字体颜色, 字体_颜色_六进制, 颜色_mapping)
        bg_颜色 = get_颜色_values(背景颜色, 背景_颜色_六进制, 颜色_mapping)
        # Determine the size based on the input 输入原图 or the provided dimensions
        if 输入原图 is not None:
            # If an 输入原图 is provided, use its size
            back_输入原图 = tensor2pil(输入原图)  # Assuming tensor2pil converts a tensor to PIL Image
            size = back_输入原图.size
        else:
            # If no 输入原图 is provided, use the provided dimensions
            size = (背景生成宽度, 背景生成高度)
            back_输入原图 = Image.new('RGB', size, bg_颜色)
        # Create PIL 输入原图s for the text and background layers and text mask
        text_输入原图 = Image.new('RGB', size, text_颜色)
        text_mask = Image.new('L', back_输入原图.size)
        # Draw the text on the text mask
        rotated_text_mask = draw_masked_text(text_mask, text, 选择字体, 字体大小,
                                             文字页边距, 文字行间距,
                                             横向偏移, 竖向偏移,
                                             竖向位置, 横向位置,
                                             旋转角度, 旋转中心)
        # Composite the text 输入原图 onto the background 输入原图 using the rotated text mask
        输入原图_out = Image.composite(text_输入原图, back_输入原图, rotated_text_mask)
        # Convert the PIL 输入原图 back to a torch tensor
        return (pil2tensor(输入原图_out),)
