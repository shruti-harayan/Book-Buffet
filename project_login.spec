# Optimized spec file for Book Buffet App
# -- project_login.spec --

import os
import glob
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Collect data files
images = [(file, os.path.join('images')) for file in glob.glob('images\\*.png')] + \
         [(file, os.path.join('images')) for file in glob.glob('images\\*.ico')]

additional_files = [
    ('BookDB.db', '.'),
    ('MemDB.db', '.'),
    ('admin.db', '.'),
    ('dashboard.py', '.'),  
    ('Existing Book.xlsx', '.'),
]

# Combine all data files
datas = images + additional_files

a = Analysis(
    ['project_login.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=collect_submodules('PIL'),  # optional, include if PIL gives errors
    hookspath=[],
    runtime_hooks=[],
    excludes=['torch', 'sympy', 'scipy', 'sklearn','setuptools','pytest','tensorflow','torchvision','PIL.ImageShow','matplotlib.tests','tkinter.test'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='BookBuffet',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # True if you want terminal window
    icon='images\\library.ico'  # set your app icon here
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BookBuffet'
)
