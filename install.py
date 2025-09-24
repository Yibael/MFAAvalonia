#!/usr/bin/env python3
"""
MFAAvalonia 项目安装脚本
用于 GitHub Actions 自动构建和打包
"""

import sys
import os
import shutil
import json
from pathlib import Path

def create_install_directory():
    """创建安装目录"""
    install_dir = Path("install")
    if install_dir.exists():
        shutil.rmtree(install_dir)
    install_dir.mkdir(exist_ok=True)
    return install_dir

def copy_project_files(install_dir):
    """复制项目文件到安装目录"""
    
    # 需要复制的文件和目录
    files_to_copy = [
        "README.md",
        "README_en.md", 
        "LICENSE",
        "interface.json",  # 如果存在
    ]
    
    dirs_to_copy = [
        "assets",  # 资源文件
        "resource",  # MAA 资源文件（如果存在）
        "lang",  # 语言文件（如果存在）
    ]
    
    # 复制文件
    for file_path in files_to_copy:
        src = Path(file_path)
        if src.exists():
            dst = install_dir / src.name
            shutil.copy2(src, dst)
            print(f"复制文件: {src} -> {dst}")
    
    # 复制目录
    for dir_path in dirs_to_copy:
        src = Path(dir_path)
        if src.exists() and src.is_dir():
            dst = install_dir / src.name
            shutil.copytree(src, dst, dirs_exist_ok=True)
            print(f"复制目录: {src} -> {dst}")

def create_default_interface_json(install_dir):
    """如果不存在 interface.json，创建一个默认的"""
    interface_path = install_dir / "interface.json"
    
    if not interface_path.exists():
        default_interface = {
            "name": "MFAAvalonia",
            "version": "1.0.0",
            "url": "https://github.com/Yibael/MFAAvalonia",
            "custom_title": "MFAAvalonia",
            "resource": [
                {
                    "name": "默认资源",
                    "path": "{PROJECT_DIR}/resource"
                }
            ],
            "task": [
                {
                    "name": "示例任务",
                    "entry": "ExampleTask",
                    "check": false,
                    "doc": "这是一个示例任务，请根据实际需求修改 interface.json"
                }
            ]
        }
        
        with open(interface_path, 'w', encoding='utf-8') as f:
            json.dump(default_interface, f, ensure_ascii=False, indent=2)
        
        print(f"创建默认 interface.json: {interface_path}")

def create_startup_scripts(install_dir):
    """创建启动脚本"""
    
    # Windows 启动脚本
    bat_content = '''@echo off
chcp 65001 > nul
echo 启动 MFAAvalonia...
if exist "MFAAvalonia.exe" (
    start "" "MFAAvalonia.exe"
) else (
    echo 错误: 找不到 MFAAvalonia.exe
    pause
)
'''
    
    with open(install_dir / "start.bat", 'w', encoding='utf-8') as f:
        f.write(bat_content)
    
    # Linux/macOS 启动脚本
    sh_content = '''#!/bin/bash
echo "启动 MFAAvalonia..."
if [ -f "./MFAAvalonia" ]; then
    ./MFAAvalonia
elif [ -f "./MFAAvalonia.exe" ]; then
    ./MFAAvalonia.exe
else
    echo "错误: 找不到 MFAAvalonia 可执行文件"
    exit 1
fi
'''
    
    sh_path = install_dir / "start.sh"
    with open(sh_path, 'w', encoding='utf-8') as f:
        f.write(sh_content)
    
    # 设置可执行权限
    os.chmod(sh_path, 0o755)
    
    print("创建启动脚本完成")

def create_readme(install_dir, version):
    """创建安装说明文件"""
    readme_content = f'''# MFAAvalonia {version}

## 快速开始

### Windows 用户
双击 `start.bat` 或直接运行 `MFAAvalonia.exe`

### Linux/macOS 用户  
运行 `./start.sh` 或直接运行 `./MFAAvalonia`

## 配置文件

- `interface.json` - 主配置文件，定义任务和资源
- `resource/` - MAA 资源文件目录
- `lang/` - 多语言支持文件

## 首次使用

1. 确保已安装 .NET 8.0 运行时
2. 将你的 MAA 项目资源文件复制到 `resource/` 目录
3. 根据你的项目修改 `interface.json` 配置文件
4. 运行程序

## 获取帮助

- 项目主页: https://github.com/Yibael/MFAAvalonia  
- 问题反馈: https://github.com/Yibael/MFAAvalonia/issues

构建时间: {version}
'''
    
    with open(install_dir / "使用说明.txt", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("创建使用说明完成")

def main():
    """主函数"""
    # 获取版本信息
    version = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    print(f"开始安装 MFAAvalonia {version}")
    
    try:
        # 创建安装目录
        install_dir = create_install_directory()
        print(f"创建安装目录: {install_dir}")
        
        # 复制项目文件
        copy_project_files(install_dir)
        
        # 创建默认配置文件（如果需要）
        create_default_interface_json(install_dir)
        
        # 创建启动脚本
        create_startup_scripts(install_dir)
        
        # 创建说明文件
        create_readme(install_dir, version)
        
        print(f"\n✅ MFAAvalonia {version} 安装包准备完成!")
        print(f"安装目录: {install_dir.absolute()}")
        
        # 显示安装目录内容
        print("\n📁 安装包内容:")
        for item in sorted(install_dir.iterdir()):
            item_type = "📁" if item.is_dir() else "📄"
            print(f"  {item_type} {item.name}")
            
    except Exception as e:
        print(f"❌ 安装过程中出现错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()