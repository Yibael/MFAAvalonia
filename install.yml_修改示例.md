# 修改 install.yml 的实际示例

## 原始文件中需要修改的部分

### 1. 修改下载 MFAAvalonia 的仓库信息

**原始代码（第 70-78 行左右）：**
```yaml
- name: Download MFAAvalonia
  if: matrix.os != 'android'
  id: download_mfa
  uses: robinraju/release-downloader@v1
  with:
    repository: SweetSmellFox/MFAAvalonia  # ← 这里需要修改
    fileName: "MFAAvalonia-*-${{ (matrix.os == 'win' && 'win') || (matrix.os == 'macos' && 'osx') || (matrix.os == 'linux' && 'linux') }}-${{ (matrix.arch == 'x86_64' && 'x64') || (matrix.arch == 'aarch64' && 'arm64') }}*"
    latest: true
    out-file-path: "MFA"
    extract: true
```

**修改后的代码示例：**
```yaml
- name: Download MFAAvalonia
  if: matrix.os != 'android'
  id: download_mfa
  uses: robinraju/release-downloader@v1
  with:
    repository: YourUsername/YourProjectName  # ← 改为你的GitHub用户名/项目名
    fileName: "MFAAvalonia-*-${{ (matrix.os == 'win' && 'win') || (matrix.os == 'macos' && 'osx') || (matrix.os == 'linux' && 'linux') }}-${{ (matrix.arch == 'x86_64' && 'x64') || (matrix.arch == 'aarch64' && 'arm64') }}*"
    latest: true
    out-file-path: "MFA"
    extract: true
```

### 2. 修改构建产物的名称

**原始代码（第 115-118 行左右）：**
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: MaaXXX-${{ matrix.os }}-${{ matrix.arch }}  # ← 这里需要修改
    path: "install"
```

**修改后的代码示例：**
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: YourProjectName-${{ matrix.os }}-${{ matrix.arch }}  # ← 改为你的项目名
    path: "install"
```

## 具体修改示例

假设你的项目信息如下：
- GitHub 用户名：`myusername`
- 项目名：`MyMaaProject`
- 项目显示名：`我的MAA项目`

### 完整的修改示例：

```yaml
# 在 install.yml 中需要修改的部分：

# 1. 如果你有自己的 MFAAvalonia 分支，修改这里：
repository: myusername/MyMaaProject

# 2. 修改构建产物名称：
name: MyMaaProject-${{ matrix.os }}-${{ matrix.arch }}

# 3. 如果需要自定义文件名模式，也可以修改：
fileName: "MyMaaProject-*-${{ (matrix.os == 'win' && 'win') || (matrix.os == 'macos' && 'osx') || (matrix.os == 'linux' && 'linux') }}-${{ (matrix.arch == 'x86_64' && 'x64') || (matrix.arch == 'aarch64' && 'arm64') }}*"
```

## 其他可能需要修改的文件

### 1. install.py 脚本

确保你的项目根目录有 `install.py` 脚本，它应该：

```python
#!/usr/bin/env python3
import sys
import os
import shutil
import json

def main():
    if len(sys.argv) > 1:
        version = sys.argv[1]
        print(f"Installing version: {version}")
    
    # 创建安装目录
    os.makedirs("install", exist_ok=True)
    
    # 复制你的项目文件
    # 这里需要根据你的项目结构进行调整
    if os.path.exists("assets"):
        shutil.copytree("assets", "install/assets", dirs_exist_ok=True)
    
    # 复制其他必要文件
    files_to_copy = [
        "interface.json",  # 如果有的话
        "README.md",
        # 添加其他需要的文件
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, "install/")
    
    print("Installation completed!")

if __name__ == "__main__":
    main()
```

### 2. interface.json 配置文件

创建或修改 `interface.json`：

```json
{
  "name": "我的MAA项目",
  "version": "1.0.0",
  "url": "https://github.com/myusername/MyMaaProject",
  "custom_title": "我的MAA项目",
  "resource": [
    {
      "name": "默认资源",
      "path": "{PROJECT_DIR}/resource/base"
    }
  ],
  "task": [
    {
      "name": "主要任务",
      "entry": "MainTask",
      "check": true,
      "doc": "这是主要的自动化任务"
    }
  ]
}
```

## 完整的部署流程

### 第一步：准备项目
```bash
# 1. Fork 或创建你的仓库
git clone https://github.com/yourusername/yourproject.git
cd yourproject

# 2. 复制 install.yml 到正确位置
mkdir -p .github/workflows
cp path/to/modified/install.yml .github/workflows/

# 3. 确保有必要的脚本和配置文件
touch install.py
touch interface.json
```

### 第二步：测试工作流程
```bash
# 1. 提交所有更改
git add .
git commit -m "Add GitHub Actions workflow"
git push origin main

# 2. 创建测试标签
git tag v0.1.0-test
git push origin v0.1.0-test
```

### 第三步：检查结果
1. 访问你的 GitHub 仓库
2. 点击 "Actions" 标签页
3. 查看工作流程是否成功运行
4. 检查生成的 Artifacts

### 第四步：正式发布
```bash
# 创建正式版本标签
git tag v1.0.0
git push origin v1.0.0
```

这将触发完整的构建和发布流程，自动创建 GitHub Release。