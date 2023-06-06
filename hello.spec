# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['hello.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['hook.py'],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# ============================魔改部分=================================================


import re
import os

# 将需要排除的模块写到一个列表（不带 .py）
my_modules = ['hello_main', ]

# 将被排除的模块添加到 a.data 
for name in my_modules:
    source_file = name + '.py'
    dest_file = name + '.py'
    a.datas.append((source_file, dest_file, 'DATA'))

# 筛选 a.pure
a.pure = [x for x in a.pure if x[0] not in my_modules]


# 把 a.pure 中原本要打包进 exe 的 py 文件以二进制依赖文件复制
a.binaries.extend([(x[1][x[1].find(x[0].replace('.', sep)):], 
                    x[1], 
                    'BINARY') 
                    for x in a.pure])
a.pure.clear()


# 用一个函数选择性对依赖文件目标路径改名
def new_dest(package: str):
    if package == 'base_library.zip' or re.match(r'python\d+.dll', package):
        return package
    return 'libs' + os.sep + package

a.binaries = [(new_dest(x[0]), x[1], x[2]) for x in a.binaries]


# 打印 a.dates ，显示哪些文件被复制到打包文件夹
# from pprint import pprint
# pprint(a.datas)

# =============================================================================

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='hello',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='hello',
)
