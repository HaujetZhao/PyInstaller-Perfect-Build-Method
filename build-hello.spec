# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


# ===========================添加要额外复制的文件和文件夹==================================

from importlib.util import find_spec	# 用于查找模块所在路径
from os.path import dirname
from os import path
from pprint import pprint
import os, re


# 空列表，用于准备要复制的数据
datas = []

# 这是要额外复制的模块
manual_modules = []
for m in manual_modules:
    if not find_spec(m): continue
    src = dirname(find_spec(m).origin)
    dst = m
    datas.append((src, dst))

# 这是要额外复制的文件夹
my_folders = ['assets']
for f in my_folders:
    datas.append((f, f))

# 这是要额外复制的文件
my_files = ['hello_main.py', 'readme.md']
for f in my_files:
    datas.append((f, '.'))      # 复制到打包导出的根目录
    
    
    
    
# ==================新建 a 变量，分析脚本============================

a = Analysis(
    ['hello.py'],               # 分析 hello.py
    pathex=[],
    binaries=[],
    datas=datas,                # 把我们准备好的 datas 列表传入
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['hook.py'],  # 一定要传入 hook.py 用于修改模块查找路径
    excludes=['IPython'],       # 有时 pyinstaller 会抽风，加入一些不需要的包，在这里排除掉
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

#===================分析完成后，重定向 a 的二进制、py文件到 libs 文件夹================================


# 把 a.datas 中不属于自定义的文件重定向到 libs 文件夹
temp = a.datas.copy(); a.datas.clear()
for dst, src, type in temp:
    c1 =  (dst == 'base_library.zip')                 # 判断文件是否为 base_library.zip
    c2 = any([dst.startswith(f) for f in my_folders]) # 判断文件是否属于 my_folders
    c3 = any([dst.startswith(f) for f in my_files])	  # 判断文件是否属于 my_files
    if any([c1, c2, c3]):
        a.datas.append((dst, src, type))
    else:
        a.datas.append((path.join('libs', dst), src, type))

# 把 a.binaries 中的二进制文件放到 a.datas ，作为普通文件复制到 libs 目录
for dst, src, type in a.binaries:
    c1 = (dst=='Python')                       # 不修改 Pyhton 
    c2 = re.fullmatch(r'python\d+\.dll', dst)  # 不修改 python310.dll
    if any([c1, c2]):
        a.datas.append((dst, src, 'DATA'))
    else:
        a.datas.append((path.join('libs', dst), src, 'DATA'))
a.binaries.clear()

# 把所有的 py 文件依赖用 a.datas 复制到 libs 文件夹
# 可选地保留某些要打包的依赖
private_module = []                         # hello.exe 不保留任何依赖
temp = a.pure.copy(); a.pure.clear()
for name, src, type in temp:
    condition = [name.startswith(m) for m in private_module]
    if condition and any(condition):
        a.pure.append((name, src, type))    # 把需要保留打包的 py 文件重新添加回 a.pure
    else:
        name = name.replace('.', os.sep)
        init = path.join(name, '__init__.py')
        pos = src.find(init) if init in src else src.find(name)
        dst = src[pos:]
        dst = path.join('libs', dst)
        a.datas.append((dst, src, 'DATA'))  # 不需要打包的第三方依赖 py 文件引到 libs 文件夹






# ========================为 a 生成 exe =========================


pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,                  # 运行 hello 的 scripts
    [],
    exclude_binaries=True,
    name='hello',               # 程序的创口贴名字叫 hello
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,               # 运行时弹出终端窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[],                    # 这里可以给 exe 加图标，如果你有图标文件的话
)


# =============用 coll 把 exe 和其所属的文件收集到目标文件夹=========================

coll = COLLECT(
    exe,            # hello.exe
    a.binaries,     # hello.exe 的二进制文件（实际上已被清空了）
    a.zipfiles, 
    a.datas,        # hello.exe 的依赖文件和自定义复制文件，都被我们导到了这里
    strip=False,
    upx=True,
    upx_exclude=[],
    name='hello',   # 输出路径在 dist 文件夹里的 hello 文件夹
)


        