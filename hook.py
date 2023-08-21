import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
sys._MEIPASS= str(BASE_DIR / 'libs')

# 为所有已存在于 sys.path 中的路径都插入 libs ，加到 sys.path 中
# 让程序到 libs 文件夹查找依赖
for p in sys.path.copy():
    relative_p = Path(p).relative_to(BASE_DIR)
    new_p = BASE_DIR / 'libs' / relative_p
    sys.path.insert(0, str(new_p))

sys.path.insert(0, str(BASE_DIR))    # 把运行文件所在的根目录排到第一位，优先从根目录查找依赖包
