# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['undis.py'],
    pathex=["undis"],
    binaries=[],
    datas=[
        ("assets/theme.json", "assets"),
        ("assets/Empty-Image.png", "assets"),
        ("assets/Missing-Image.png", "assets"),
    ],
    hiddenimports=[
        "PIL._tkinter_finder",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='undis',
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
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='undis',
)