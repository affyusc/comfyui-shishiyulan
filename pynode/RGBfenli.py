import torch
from typing import Tuple
from PIL import Image
import numpy as np

class RGBSplitAndGrayscale:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_in": ("IMAGE", {}),  # 期望的输入图像
            }
        }

    RETURN_TYPES = ("IMAGE", "IMAGE", "IMAGE", "IMAGE")  # 4 个输出：R 通道，G 通道，B 通道，灰度图
    RETURN_NAMES = ("R 通道", "G 通道", "B 通道", "灰度图")  # 对应输出的名称
    FUNCTION = "split_rgb_channels"  # 需要实现的功能函数
    CATEGORY = "WUKONG/图像处理"  # 分类

    def preprocess_image(self, image_in: torch.Tensor) -> np.ndarray:
        # 如果输入是 PyTorch Tensor，将其转换为 NumPy 数组
        if isinstance(image_in, torch.Tensor):
            image_in = image_in.detach().cpu().numpy()

        # 如果图像是4维数组，去掉批处理维度
        if len(image_in.shape) == 4:
            image_in = np.squeeze(image_in, axis=0)  # 去掉批处理维度 (1, H, W, C) -> (H, W, C)

        # 如果图像是浮点数，假定范围是 [0, 1]，将其缩放到 [0, 255]
        if image_in.dtype == np.float32 or image_in.dtype == np.float64:
            image_in = (image_in * 255).clip(0, 255).astype(np.uint8)  # 确保转换为 uint8 类型

        return image_in

    def split_rgb_channels(self, image_in: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        # 预处理图像，将其转换为 NumPy 格式
        image_in = self.preprocess_image(image_in)

        # 确保图像有3个通道 (H, W, 3)
        if image_in.shape[-1] != 3:
            raise ValueError("Input image must have 3 channels (RGB).")

        # 将 NumPy 数组转换为 PIL 图像
        pil_image = Image.fromarray(image_in)

        # 分离 R, G, B 通道
        r, g, b = pil_image.split()

        # 将整张图像转换为灰度图像
        gray_image = pil_image.convert('L')

        # 打印调试信息以检查通道是否正确
        print(f"R 通道: {np.array(r).max()}, G 通道: {np.array(g).max()}, B 通道: {np.array(b).max()}, 灰度图: {np.array(gray_image).max()}")

        # 将 PIL 图像转回 NumPy 并再转成 PyTorch Tensor 格式
        r_channel = torch.from_numpy(np.array(r)).unsqueeze(0).float() / 255.0  # 确保范围是 [0, 1]
        g_channel = torch.from_numpy(np.array(g)).unsqueeze(0).float() / 255.0
        b_channel = torch.from_numpy(np.array(b)).unsqueeze(0).float() / 255.0
        gray_image = torch.from_numpy(np.array(gray_image)).unsqueeze(0).float() / 255.0

        return r_channel, g_channel, b_channel, gray_image

# 定义节点映射
NODE_CLASS_MAPPINGS = {
    "RGBSplitAndGrayscale": RGBSplitAndGrayscale
}
