# MFAAvalonia GitHub Actions 使用指南

## 什么是 GitHub Actions？

GitHub Actions 是 GitHub 提供的自动化工具，它可以：
- 在代码推送时自动构建项目
- 在发布新版本时自动打包和发布
- 自动运行测试
- 自动部署应用程序

## install.yml 工作流程详解

### 触发条件 (on)
```yaml
on:
  push:
    tags:
      - "v*"           # 当推送以 "v" 开头的标签时触发（如 v1.0.0）
    branches:
      - "**"           # 任何分支的推送都会触发
    paths:
      - ".github/workflows/install.yml"  # 当这些路径的文件改变时触发
      - "assets/**"
      - "**.py"
  pull_request:        # 拉取请求时也会触发
  workflow_dispatch:   # 允许手动触发工作流程
```

### 工作任务 (jobs)

#### 1. meta 任务
**作用：** 确定版本标签和是否为正式发布

```yaml
meta:
  runs-on: ubuntu-latest  # 运行在 Ubuntu 虚拟机上
```

**重要功能：**
- 自动检测是否为发布版本（标签以 v 开头）
- 生成版本号标签
- 为后续任务提供版本信息

#### 2. install 任务
**作用：** 为多个平台构建安装包

```yaml
strategy:
  matrix:
    os: [win, macos, linux, android]     # 支持的操作系统
    arch: [aarch64, x86_64]              # 支持的架构
```

**详细步骤：**
1. **下载 MaaFramework：** 从官方仓库下载最新版本
2. **下载 MFAAvalonia：** 下载 GUI 组件
3. **执行安装脚本：** 运行 install.py 脚本
4. **上传构建产物：** 将构建结果上传为 GitHub Artifacts

#### 3. changelog 任务
**作用：** 自动生成更新日志

#### 4. release 任务
**作用：** 创建正式发布版本（仅在推送标签时执行）

## 如何修改 install.yml 适配你的项目

### 步骤 1：克隆或下载当前文件
```bash
# 下载当前的 install.yml 文件
wget https://raw.githubusercontent.com/Yibael/MFAAvalonia/master/.github/workflows/install.yml
```

### 步骤 2：修改关键配置

找到并修改以下内容：

```yaml
# 第 75-76 行附近，修改下载源
repository: SweetSmellFox/MFAAvalonia  # 改为：YourUsername/YourProject

# 第 116 行附近，修改 artifact 名称
name: MaaXXX-${{ matrix.os }}-${{ matrix.arch }}  # 改为：YourProject-${{ matrix.os }}-${{ matrix.arch }}
```

### 步骤 3：修改项目特定信息

在你的项目根目录创建或修改 `install.py` 脚本，确保它：
1. 正确处理你的项目文件结构
2. 复制必要的资源文件
3. 设置正确的配置文件

## 常见误解和注意事项

### ❌ 常见误解
1. **"GitHub Actions 会自动知道我的项目结构"**
   - ✅ **实际情况：** 需要通过脚本明确告诉 Actions 如何处理你的文件

2. **"只要复制 install.yml 就能直接使用"**
   - ✅ **实际情况：** 需要根据你的项目修改相应的仓库名、项目名等

3. **"Actions 会自动发布到我的仓库"**
   - ✅ **实际情况：** 需要确保仓库有正确的权限设置

### ⚠️ 重要注意事项

1. **权限设置：**
   ```yaml
   # 确保你的仓库 Settings > Actions > General 中启用了：
   # - Read and write permissions
   # - Allow GitHub Actions to create and approve pull requests
   ```

2. **Secrets 配置：**
   - `GITHUB_TOKEN` 通常是自动提供的
   - 如果需要其他密钥，在仓库 Settings > Secrets 中添加

3. **分支保护：**
   - 如果启用了分支保护，可能需要额外配置权限

## 手动安装方法（备选方案）

如果不想使用 GitHub Actions，可以手动安装：

1. **下载最新发行版**
   ```bash
   # 从 GitHub Releases 页面下载预构建版本
   ```

2. **复制资源文件**
   ```bash
   # 将 maafw 项目中的资源复制到 MFAAvalonia/resource 中
   cp -r your-maa-project/assets/resource/* MFAAvalonia/resource/
   ```

3. **配置 interface.json**
   ```bash
   # 复制并修改配置文件
   cp your-maa-project/assets/interface.json MFAAvalonia/
   ```

4. **修改配置文件**
   - 添加项目名称、版本等信息
   - 配置资源路径和任务

## 下一步操作

1. **Fork 或创建你的仓库**
2. **修改 install.yml 中的仓库信息**
3. **确保有正确的 install.py 脚本**
4. **测试工作流程**：
   ```bash
   # 推送一个测试标签
   git tag v0.1.0-test
   git push origin v0.1.0-test
   ```
5. **查看 Actions 页面**确认工作流程是否正常运行

## 故障排除

### 常见问题：

1. **Actions 失败：权限不足**
   - 检查仓库的 Actions 权限设置

2. **找不到文件或仓库**
   - 确认修改了正确的仓库名和文件路径

3. **构建失败**
   - 查看 Actions 日志中的具体错误信息
   - 确认 install.py 脚本是否正确

4. **发布失败**
   - 确认标签格式正确（以 v 开头）
   - 检查是否有发布权限

需要帮助？可以查看 GitHub Actions 的官方文档或在项目的 Issues 中提问。