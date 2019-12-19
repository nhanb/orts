# -*- mode: python ; coding: utf-8  -*-
# vim: set ft=python:

block_cipher = None


a = Analysis(
    ["orts.py"],
    binaries=[],
    datas=[
        ("main_view.enaml", "."),
        ("gui_assets", "gui_assets"),
        ("data", "data"),
        ("web", "web"),
    ],
    hiddenimports=[
        "utils.gui",
        "enaml",
        "enaml.core.parser.parse_tab.lextab36",
        "enaml.core.compiler_helpers",
        "enaml.core.compiler_nodes",
        "enaml.core.enamldef_meta",
        "enaml.core.template",
        "enaml.widgets.api",
        "enaml.widgets.form",
        "enaml.layout.api",
        "enaml.stdlib.fields",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="orts",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="orts",
)
