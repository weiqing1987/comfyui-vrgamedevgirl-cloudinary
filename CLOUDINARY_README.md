# Cloudinary 集成使用说明

## 概述

此模块将 comfyui-vrgamedevgirl 插件的视频和音频输出上传到 Cloudinary 存储桶，解决 RunningHub 不支持文件夹输出的问题。

## 配置的 Cloudinary 账户

- **Cloud Name**: `dftco0cki`
- **API Key**: `192422146789215`
- **API Secret**: `HKcrrpmDGP2u0qimbuweYxfnlt4`

## 安装步骤

### 1. 安装 Cloudinary Python SDK

在 ComfyUI 的 Python 环境中运行：

```bash
pip install cloudinary
```

或者使用 requirements.txt：

```bash
cd C:\Users\weidi\Desktop\tool\ComfyUI_plusV14\01 comfyui_V14\ComfyUI-aki-V14\ComfyUI\custom_nodes\comfyui-vrgamedevgirl
pip install -r requirements.txt
```

### 2. 重启 ComfyUI

安装完成后重启 ComfyUI 以加载新节点。

## 新增节点

### 视频上传节点

**VRGDG Upload Video to Cloudinary** (GeneralVideoNodes.py)
- 输入：`video_path` (本地视频文件路径)
- 输出：
  - `cloudinary_url`: Cloudinary 公开访问 URL
  - `public_id`: Cloudinary 资源 ID
  - `upload_success`: 上传是否成功 (BOOLEAN)

**VRGDG Upload Video to Cloudinary (Humo)** (HumoAutomation.py)
- 与上述功能相同，专用于 HUMO 工作流

### 音频上传节点

**VRGDG Upload Audio to Cloudinary** (VRGDG_AudioNodes.py)
- 输入：`audio` (AUDIO 类型), `audio_name`
- 输出：
  - `cloudinary_url`: Cloudinary 公开访问 URL
  - `public_id`: Cloudinary 资源 ID
  - `upload_success`: 上传是否成功 (BOOLEAN)

## 使用示例

### 基本视频上传流程

```
[Video Combine] → video_path
                    ↓
[VRGDG Upload Video to Cloudinary]
                    ↓
    cloudinary_url → 用于 RunningHub 或分享
```

### 基本音频上传流程

```
[Audio Output] → audio
                   ↓
[VRGDG Upload Audio to Cloudinary]
                    ↓
    cloudinary_url → 用于 RunningHub 或分享
```

## Cloudinary 资源管理

### 访问上传的资源

所有上传的资源存储在：
- 视频：`https://res.cloudinary.com/dftco0cki/video/upload/vrgamedevgirl/videos/...`
- 音频：`https://res.cloudinary.com/dftco0cki/video/upload/vrgamedevgirl/audio/...`

### Cloudinary 控制台

访问：https://cloudinary.com/console
登录后可以：
- 查看所有上传的媒体
- 管理文件夹和标签
- 分析使用情况
- 配置转换和优化

## RunningHub 集成

### 问题背景
- RunningHub 不支持文件夹输出
- 原项目输出多个视频片段到文件夹
- 导致只能输出 10 秒视频

### 解决方案
1. 使用 Cloudinary 上传节点上传每个视频片段
2. 从 Cloudinary 获取公开 URL
3. 在 RunningHub 中使用 URL 直接引用视频

## 故障排除

### "Cloudinary module not available"
- 确认已运行 `pip install cloudinary`
- 重启 ComfyUI

### "Upload failed"
- 检查网络连接
- 验证 Cloudinary 凭证是否正确
- 查看 ComfyUI 控制台日志获取详细错误信息

### "File not found"
- 确认视频/音频文件路径正确
- 确保文件已生成完成再上传

## 文件结构

```
comfyui-vrgamedevgirl/
├── cloudinary_storage.py      # Cloudinary 核心模块
├── GeneralVideoNodes.py       # 添加了 VRGDG_UploadVideoToCloudinary
├── VRGDG_AudioNodes.py        # 添加了 VRGDG_UploadAudioToCloudinary
├── HumoAutomation.py          # 添加了 VRGDG_UploadVideoToCloudinary_Humo
├── requirements.txt           # 添加了 cloudinary 依赖
└── CLOUDINARY_README.md       # 本文档
```

## 注意事项

1. **带宽限制**: Cloudinary 免费套餐有带宽限制，请注意使用情况
2. **存储空间**: 免费套餐提供有限的存储空间
3. **视频时长**: 免费套餐对视频时长有限制
4. **隐私设置**: 默认上传为公开可访问，如需私有请修改代码

## 技术支持

如有问题，请查看：
- Cloudinary 文档：https://cloudinary.com/documentation
- 项目 GitHub: https://github.com/vrgamegirl19/comfyui-vrgamedevgirl
