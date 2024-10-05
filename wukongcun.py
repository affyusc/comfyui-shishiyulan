import os
import json
import datetime
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageOps, ImageSequence
import numpy as np
import torch
from PIL.PngImagePlugin import PngInfo
import folder_paths
import sys

class Wukongbaocunl:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()  # 默认输出目录
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "WUKONG"}),
                "format": (["png", "jpg", "webp"],),
                "quality": ("INT", {"default": 95, "min": 1, "max": 100, "step": 1}),
                "apply_watermark": ("BOOLEAN", {"default": False}),
                "watermark_text": ("STRING", {"default": ""}),
                "custom_output_dir": ("STRING", {"default": "", "optional": True})
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ()
    FUNCTION = "save_enhanced_image"
    OUTPUT_NODE = True
    CATEGORY = "WUKONG/其他"

    def save_enhanced_image(self, images, filename_prefix, format, quality, apply_watermark, watermark_text, custom_output_dir="", prompt=None, extra_pnginfo=None):
        default_results = self._save_images_to_dir(images, filename_prefix, format, quality, apply_watermark, watermark_text, prompt, extra_pnginfo, self.output_dir)
        
        if custom_output_dir:
            self._save_images_to_dir(images, filename_prefix, format, quality, apply_watermark, watermark_text, prompt, extra_pnginfo, custom_output_dir)
        
        return {"ui": {"images": default_results}}

    def _save_images_to_dir(self, images, filename_prefix, format, quality, apply_watermark, watermark_text, prompt, extra_pnginfo, output_dir):
        results = []
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        for i, image in enumerate(images):
            img = Image.fromarray((image.squeeze().cpu().numpy() * 255).astype(np.uint8))

            # 添加水印
            if apply_watermark and watermark_text:
                self.add_watermark(img, watermark_text)

            # 保存图像
            filename = f"{filename_prefix}_{timestamp}_{i}.{format}"
            filepath = os.path.join(output_dir, filename)

            if format == "png":
                img.save(filepath, format="PNG", compress_level=(100 - quality) // 10)
            elif format == "jpg":
                img.save(filepath, format="JPEG", quality=quality)
            elif format == "webp":
                img.save(filepath, format="WEBP", quality=quality)

            results.append({
                "filename": filename,
                "subfolder": "",
                "type": self.type
            })

        return results

    def add_watermark(self, img, text):
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        # 使用 textbbox 而不是 textsize
        bbox = draw.textbbox((0, 0), text, font=font)
        textwidth, textheight = bbox[2] - bbox[0], bbox[3] - bbox[1]

        width, height = img.size
        x = width - textwidth - 10
        y = height - textheight - 10

        draw.text((x, y), text, font=font, fill=(255, 255, 255, 128))

# 节点映射
NODE_CLASS_MAPPINGS = {
    "Wukongbaocunl": Wukongbaocunl
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Wukongbaocunl": "Wukongbaocunl"
}
