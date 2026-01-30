# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, copy_metadata


def _collect_analysis_packages(analysis) -> tuple[list, list, list]:
    packages: set[str] = set()
    for name, _path, _type in analysis.pure:
        top_level = name.split(".", 1)[0]
        if top_level:
            packages.add(top_level)
    datas: list = []
    binaries: list = []
    hiddenimports: list[str] = []
    for package in sorted(packages):
        try:
            pkg_datas, pkg_bins, pkg_hidden = collect_all(package)
        except Exception:
            continue
        datas += pkg_datas
        binaries += pkg_bins
        hiddenimports += pkg_hidden
    return datas, binaries, hiddenimports


base_datas = []
base_datas += copy_metadata("mcp")
try:
    base_datas += copy_metadata("fastmcp")
except Exception:
    pass

base_hiddenimports = [
    "lupa",
    "lupa.lua51",
    "lupa._lupa",
]

a0 = Analysis(
    ["src/server.py"],
    pathex=[],
    binaries=[],
    datas=base_datas,
    hiddenimports=base_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

auto_datas, auto_binaries, auto_hidden = _collect_analysis_packages(a0)

a = Analysis(
    ["src/server.py"],
    pathex=[],
    binaries=auto_binaries,
    datas=base_datas + auto_datas,
    hiddenimports=base_hiddenimports + auto_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="asana-mcp-server",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
