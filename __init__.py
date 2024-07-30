import sys
import os

# 添加当前路径到sys.path
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'nodes'))
sys.path.append(os.path.join(current_dir, 'modules'))


from colorama import Fore, Style, init
init(autoreset=True)

# 自定义颜色接近 #FF0072
class CustomColors:
    PINK = '\033[38;2;255;0;114m'
    PINK_HEX = '#FF0072'

from modules.log import create_logger

logger = create_logger()

ROOT = os.path.abspath(os.path.dirname(__file__))
NAME = "Fantasy AI Studio Node"
PACKAGE = "FAI_Node"
MENU_NAME = "FAI_Node"
NODES_DIR = os.path.join(ROOT, 'nodes')
EXTENSION_WEB_DIRS = {}

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# 手动导入节点
from fai_voronoi_generator import NODE_CLASS_MAPPINGS as FAI_Voronoi_Generator_MAPPINGS
from fai_voronoi_generator import NODE_DISPLAY_NAME_MAPPINGS as FAI_Voronoi_Generator_DISPLAY_NAMES
from fai_dynamic_mask import NODE_CLASS_MAPPINGS as FAI_Dynamic_Mask_MAPPINGS
from fai_dynamic_mask import NODE_DISPLAY_NAME_MAPPINGS as FAI_Dynamic_Mask_DISPLAY_NAMES

NODE_CLASS_MAPPINGS.update(FAI_Voronoi_Generator_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(FAI_Voronoi_Generator_DISPLAY_NAMES)
NODE_CLASS_MAPPINGS.update(FAI_Dynamic_Mask_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(FAI_Dynamic_Mask_DISPLAY_NAMES)

# 打印节点名称以确认
#print("Loaded nodes:", list(NODE_CLASS_MAPPINGS.keys()))
#print("Node display names:", list(NODE_DISPLAY_NAME_MAPPINGS.values()))

# 使用颜色进行特定节点加载日志
logger.info(f"{CustomColors.PINK}Loaded nodes: {list(NODE_CLASS_MAPPINGS.keys())}")
logger.info(f"{CustomColors.PINK}Node display names: {list(NODE_DISPLAY_NAME_MAPPINGS.values())}")

# 恢复颜色
logger.info(Style.RESET_ALL)

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
