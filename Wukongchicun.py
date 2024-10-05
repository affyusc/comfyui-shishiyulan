class Wukongchicun:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "选择1024尺寸": ("BOOLEAN", {"default": False}),
                "选择1536尺寸": ("BOOLEAN", {"default": False}),
                "选择1920尺寸": ("BOOLEAN", {"default": False}),
                "选择2048尺寸": ("BOOLEAN", {"default": False}),
                "选择2880尺寸": ("BOOLEAN", {"default": False}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("INT",)  # 返回一个整数值，用于宽度或高度
    FUNCTION = "run"
    CATEGORY = "WUKONG/其他"
    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False,)

    def run(self, 选择1024尺寸, 选择1536尺寸, 选择1920尺寸, 选择2048尺寸, 选择2880尺寸):
        selected_size = None

        # 互斥逻辑：一次只能选择一个尺寸
        if 选择1024尺寸:
            selected_size = 1024
            选择1536尺寸 = False
            选择1920尺寸 = False
            选择2048尺寸 = False
            选择2880尺寸 = False
        elif 选择1536尺寸:
            selected_size = 1536
            选择1024尺寸 = False
            选择1920尺寸 = False
            选择2048尺寸 = False
            选择2880尺寸 = False
        elif 选择1920尺寸:
            selected_size = 1920
            选择1024尺寸 = False
            选择1536尺寸 = False
            选择2048尺寸 = False
            选择2880尺寸 = False
        elif 选择2048尺寸:
            selected_size = 2048
            选择1024尺寸 = False
            选择1536尺寸 = False
            选择1920尺寸 = False
            选择2880尺寸 = False
        elif 选择2880尺寸:
            selected_size = 2880
            选择1024尺寸 = False
            选择1536尺寸 = False
            选择1920尺寸 = False
            选择2048尺寸 = False

        # 如果没有选中尺寸，则返回默认尺寸
        if selected_size is None:
            selected_size = 1024  # 默认值

        return (selected_size,)
