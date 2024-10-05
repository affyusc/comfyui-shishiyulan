class Wukonggudingchicun:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "size_selector": (
                    ["512", "1024", "1536", "1920", "2048", "2880"],  # 定义下拉菜单的选项
                    {"default": "1024"},  # 设置默认值
                ),
            },
            "optional": {},
        }

    RETURN_TYPES = ("INT",)  # 返回一个整数值，用于宽度或高度
    FUNCTION = "run"
    CATEGORY = "WUKONG/其他"
    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False,)

    def run(self, size_selector):
        # 将选择的值转换为整数
        selected_size = int(size_selector)
        
        return (selected_size,)
