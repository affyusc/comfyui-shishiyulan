class Wukonghuatiao:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "浮点权重": ("FLOAT", {
                        "default": 1,
                        "min": 0,
                        "max": 1,
                        "step": 0.01,
                        "display": "slider"
                    }),
                },
                "optional": {}
        }
    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "run"
    CATEGORY = "WUKONG/滑条"
    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False,)
    def run(self, 浮点权重):
        scaled_number = 浮点权重
        return (scaled_number,)
