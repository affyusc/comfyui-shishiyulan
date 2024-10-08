from PIL import Image, ImageOps, ImageSequence
from PIL.PngImagePlugin import PngInfo
import os
import numpy as np
import json
import sys
from comfy.cli_args import args
import folder_paths

current_dir = os.path.dirname(__file__)
grandparent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(grandparent_dir)
from comfy.cli_args import args

class WukongSaveImagesNode:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", ),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                "custom_output_dir": ("STRING", {"default": "", "optional": True}),
                
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "WUKONG/其他"

    def save_images(self, images, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None, custom_output_dir="", **kwargs):
        default_results = self._save_images_to_dir(images, filename_prefix, prompt, extra_pnginfo, self.output_dir)
        
        if custom_output_dir:
            self._save_images_to_dir(images, filename_prefix, prompt, extra_pnginfo, custom_output_dir)
        
        return {"ui": {"images": default_results}}

    def _save_images_to_dir(self, images, filename_prefix, prompt, extra_pnginfo, output_dir):
        results = list()
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, output_dir, images[0].shape[1], images[0].shape[0])
        
        for (batch_number, image) in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))
            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.png"
            img.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=self.compress_level)
            
            display_path = os.path.join(output_dir, subfolder)
            results.append({
                "filename": file,
                "subfolder": display_path,
                "type": self.type
            })
            counter += 1
        
        return results

# 定义节点映射，以便 ComfyUI 检测到这个自定义节点
NODE_CLASS_MAPPINGS = {
    "WukongSaveImagesNode": WukongSaveImagesNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WukongSaveImagesNode": "Wukong保存图像节点"
}

# For testing the node functionality
if __name__ == "__main__":
    # Example test
    test_image = torch.rand((1, 256, 256, 3), dtype=torch.float32)  # Random image for testing
    node = WukongSaveImagesNode()
    node.save_images([test_image], filename_prefix="TestPrefix")
