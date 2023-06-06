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
from os import sep

# 将需要排除的模块写到一个列表（不带 .py）
my_modules = ['hello_main', ]

# 将被排除的模块文件添加到 a.data，让其作为文件复制
for name in my_modules:
    source_file = name + '.py'
    dest_file = name + '.py'
    a.datas.append((source_file, dest_file, 'DATA'))
# 筛选 a.pure，把要排除的模块文件去除
a.pure = [x for x in a.pure if x[0] not in my_modules]



# a.pure 中保存了所需要的 py 依赖文件，默认他会被打包到 exe 文件中
# 在修改依赖文件路径后，这种默认的打包行为可能会导致一些错误
# 所以我们要把 a.pure 中原本将打包进 exe 的 py 文件以二进制依赖文件复制
a.binaries.extend([(x[1][x[1].find(x[0].replace('.', sep)):], 
                    x[1], 
                    'BINARY') 
                    for x in a.pure])
a.pure.clear()



# 用一个函数选择性对依赖文件目标路径改名，统一移动到 libs 文件夹，这样更清爽
def new_dest(package: str):
    if package == 'base_library.zip' or re.match(r'python\d+.dll', package):
        return package
    return 'libs' + os.sep + package

a.binaries = [(new_dest(x[0]), x[1], x[2]) for x in a.binaries]




# 删除自动添加的多余垃圾文件（一般都是版本信息之类的）
trash = ['dist-info']
def filter_trash(name):
    for t in trash:
        if t not in name: continue
        print(f'\nfiltered: {name}\n')
        return False
    return True
a.datas = [x for x in a.datas if filter_trash(x[0]) ]


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
