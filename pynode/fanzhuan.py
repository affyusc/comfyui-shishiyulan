from typing import Tuple
import torch
from PIL import Image
import numpy as np

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

class ImageTransform:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_in": ("IMAGE", {}),  # 输入图像
                "transform_type": (["水平翻转", "垂直翻转", "旋转90度", "旋转180度", "旋转360度"],)  # 下拉菜单选择
            }
        }

    RETURN_TYPES = ("IMAGE",)  # 返回一张变换后的图像
    RETURN_NAMES = ("变换后的图像",)
    FUNCTION = "apply_transform"  # 绑定到 apply_transform 函数
    CATEGORY = "WUKONG/图像处理"

    def apply_transform(self, image_in: torch.Tensor, transform_type: str) -> torch.Tensor:
        batch_tensor = []
        for image in image_in:
            image = tensor2pil(image)  # 将 Tensor 转换为 PIL 图像
            
            # 根据用户选择的变换类型执行操作
            if transform_type == "水平翻转":
                transformed_image = image.transpose(Image.FLIP_LEFT_RIGHT)
            elif transform_type == "垂直翻转":
                transformed_image = image.transpose(Image.FLIP_TOP_BOTTOM)
            elif transform_type == "旋转90度":
                transformed_image = image.rotate(90, expand=True)
            elif transform_type == "旋转180度":
                transformed_image = image.rotate(180)
            elif transform_type == "旋转360度":
                transformed_image = image.rotate(360)
            
            # 将 PIL 图像转换回 Tensor 并加入 batch
            batch_tensor.append(pil2tensor(transformed_image))
        
        # 拼接 batch，返回结果
        batch_tensor = torch.cat(batch_tensor, dim=0)
        return (batch_tensor, )

# 定义节点映射
NODE_CLASS_MAPPINGS = {
    "ImageTransform": ImageTransform
}
