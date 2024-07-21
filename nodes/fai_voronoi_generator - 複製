import torch
import numpy as np
import math
import random
from modules.noise import VoronoiNoise
from modules.easing import easing_functions, KeyframeScheduler, safe_eval

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False
        
WILDCARD = AnyType("*")

class FAI_Voronoi_Generator:
    color = "#FF0072"  # 设置节点颜色为粉色
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "batch_size": ("INT", {"min": 1, "max": 4096}),
                "width": ("INT", {"default": 64, "min": 64, "max": 4096}),
                "height": ("INT", {"default": 64, "min": 64, "max": 4096}),
            },
            "optional": {
                "distance_metric": ([
                    "euclidean (圆形)",
                    "manhattan (矩形)",
                    "chebyshev (菱形)",
                    "minkowski (圆方形)",
                    "elliptical (椭圆形)",
                    "kaleidoscope_star (万花筒_旋转星)",
                    "kaleidoscope_wave (万花筒_波浪)",
                    "kaleidoscope_radiation_α (万花筒_放射线_α)",
                    "kaleidoscope_radiation_β (万花筒_放射线_β)",
                    "kaleidoscope_radiation_γ (万花筒_放射线_γ)"
                ],),
                "x_schedule": ("LIST",),
                "y_schedule": ("LIST",),
                "scale_schedule": ("LIST",),
                "detail_schedule": ("LIST",),
                "randomness_schedule": ("LIST",),
                "seed_schedule": ("LIST", ),
                "device": (["cuda", "cpu"],),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "INT")
    RETURN_NAMES = ("images", "batch_size")

    FUNCTION = "generate"
    CATEGORY = "⚛️FAI_Node⚛️/Voronoi Generator"
    
    def generate(self, batch_size, width, height, distance_metric="euclidean (圆形)", x_schedule=[0], y_schedule=[0], scale_schedule=[1.0], detail_schedule=[100], randomness_schedule=[1], seed_schedule=[0], device="cuda"):
        voronoi = VoronoiNoise(width=width, height=height, scale=scale_schedule, detail=detail_schedule, seed=seed_schedule, 
                            X=x_schedule, Y=y_schedule, 
                            randomness=randomness_schedule, distance_metric=distance_metric, batch_size=batch_size, device=device)
        voronoi = voronoi.to(device)
        tensors = voronoi()
        return(tensors, batch_size)
    
class FAIScaleScheduler:
    formulas = {
        "高频振荡（High-Frequency Oscillation） - 适合高频节奏的音乐": "0:(15 * cos((a / 60 * 3.141 * (t + 0) / b))**70 + 0.009)",
        "非线性变化（Nonlinear Variation） - 适合不规则节奏的音乐": "0:(10 * abs(tan(t / b * 3.141 * (a / 60))) % 1 + 0.01)",
        "重复线性变化（Repeating Linear Change） - 适合节奏鲜明的音乐": "0:(10 * abs(2 * ((t / b * a / 60) % 1) - 1) + 0.01)",
        "平滑周期变化（Smooth Periodic Change）[Sin] - 适合柔和的音乐节奏": "0:(10 * abs(sin(t / b * 2 * 3.141 * (a / 60))) + 0.01)",
        "平滑周期变化（Smooth Periodic Change）[Cosine] - 适合柔和的音乐节奏": "0:(10 * abs(cos(t / b * 2 * 3.141 * (a / 60))) + 0.01)",
        "二次曲线变化（Quadratic Curve Change） - 适合渐变的音乐节奏": "0:((t / b * a / 60)**2 % 1 * 10 + 0.01)",
        "三次曲线变化（Cubic Curve Change） - 适合渐进的音乐节奏": "0:((t / b * a / 60)**3 % 1 * 10 + 0.01)",
        "对数变化（Logarithmic Change） - 适合渐强的音乐节奏": "0:(10 * log(t / b * a / 60 + 1) % 1 + 0.01)",
        "线性绝对值变化（Linear Absolute Change） - 适合明确节奏的音乐": "0:(10 * abs(t / b * a / 60 % 1) + 0.01)",
        "指数变化（Exponential Change） - 适合逐渐增强的音乐效果": "0:((exp(t / b * a / 60) - 1) / (exp(1) - 1) * 10 + 0.01)",
        "柔和波浪变化（Gentle Wave Change） - 适合轻柔的音乐节奏": "0:(5 * sin(2 * 3.141 * (t / b) * (a / 60))**2 + 0.01)",
        "温和振荡变化（Gentle Oscillation Change） - 适合轻松的音乐节奏": "0:(5 * (cos(3.141 * (t / b) * (a / 60))**3 + 1) / 2 + 0.01)",
        "平滑递增变化（Smooth Incremental Change） - 适合舒缓的音乐节奏": "0:(5 * (1 - exp(-3 * (t / b) * (a / 60))) + 0.01)",
        "S型曲线变化（S-Curve Change） - 适合渐进和渐出效果": "0:(10 / (1 + exp(-10 * ((t / b * a / 60) - 0.5))) + 0.01)",
        "脉冲变化（Pulse Change） - 适合脉冲和短促节奏": "0:(10 * (t % (b / a) < (b / a) / 2) + 0.01)",
        "抛物线变化（Parabolic Change） - 适合渐变和峰值节奏": "0:(10 * (1 - ((t / b * a / 60 - 0.5) ** 2) * 4) + 0.01)",
        "锯齿波变化（Sawtooth Change） - 适合急剧上升和下降的节奏": "0:(10 * ((t / b * a / 60) % 1) + 0.01)"
    }
    @classmethod
    def INPUT_TYPES(cls):
        easing_funcs = list(easing_functions.keys())
        easing_funcs.insert(0, "None")
        return {
            "required": {
                "formula": (list(cls.formulas.keys()), ),
                "easing_mode": (easing_funcs, )
            },
            "optional": {
                "end_frame": ("INT", {"min": 0}),
                "ndigits": ("INT", {"min": 1, "max": 12, "default": 5}),
                "a": (WILDCARD, {}),  # 允许外部输入
                "b": (WILDCARD, {})   # 允许外部输入
            }
        }

    RETURN_TYPES = ("LIST", )
    RETURN_NAMES = ("schedule_list", )

    FUNCTION = "generate_schedule"
    CATEGORY = "⚛️FAI_Node⚛️/Voronoi Generator"

    def generate_schedule(self, formula, easing_mode, end_frame=0, ndigits=2, a=1.0, b=1.0):
        selected_formula = self.formulas[formula]

        custom_vars = {"a": a, "b": b}
        scheduler = KeyframeScheduler(end_frame=end_frame, custom_vars=custom_vars)
        schedule = scheduler.generate_schedule(selected_formula, easing_mode=easing_mode, ndigits=ndigits)
        return (schedule, )


NODE_CLASS_MAPPINGS = {
    "FAI_Voronoi_Generator": FAI_Voronoi_Generator,
    "FAIScaleScheduler": FAIScaleScheduler
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FAI_Voronoi_Generator": "⚛️FAI_Voronoi_Generator⚛️",
    "FAIScaleScheduler": "⚛️FAI Scale Scheduler⚛️"
}
  #FUNCTION = "generate_schedule"
  #CATEGORY = "⚛️FAI_Node⚛️/Voronoi Generator"