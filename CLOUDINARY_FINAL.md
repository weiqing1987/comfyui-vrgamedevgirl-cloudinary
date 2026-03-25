# Cloudinary 存储桶集成 - 完整方案

## 概述

将 comfyui-vrgamedevgirl 生成的所有视频自动上传到 Cloudinary 存储桶，解决 RunningHub 只能输出 10 秒视频的问题。

---

## 安装的节点

### 1. **VRGDG_UploadVideoToCloudinary_Auto**（推荐使用）
- **位置**: `GeneralVideoNodes.py`
- **用途**: 自动上传 Video Combine 生成的每个视频片段
- **输入**:
  - `trigger` (VHS_FILENAMES) - 从 Video Combine 的 FILENAMES 输出连接
  - `output_folder` (STRING) - 视频输出文件夹
  - `video_name_prefix` (STRING) - 视频文件名前缀，默认 `video`
  - `upload_enabled` (BOOLEAN) - 是否启用上传
  - `cloudinary_cloud_name` - Cloudinary 云名称
  - `cloudinary_api_key` - API 密钥
  - `cloudinary_api_secret` - API 密钥（密码）
- **输出**:
  - `cloudinary_url` - Cloudinary 公开访问 URL
  - `public_id` - 资源 ID
  - `upload_success` - 上传是否成功
  - `local_path` - 本地文件路径

### 2. **VRGDG_CreateFinalVideo_SRT** (已修改)
- **位置**: `HumoAutomation.py`
- **用途**: 最终合成视频并上传到 Cloudinary
- **新增输入**:
  - `enable_cloudinary` - 启用 Cloudinary 上传
  - `cloudinary_cloud_name` - dftco0cki
  - `cloudinary_api_key` - 192422146789215
  - `cloudinary_api_secret` - HKcrrpmDGP2u0qimbuweYxfnlt4

---

## 安装步骤

### 1. 安装 Cloudinary Python SDK
```bash
pip install cloudinary
```

### 2. 重启 ComfyUI

---

## 工作流连接方法

### 方案 A：每个视频片段上传（推荐）

```
┌─────────────────────────┐
│  Video Combine (VHS)    │
│  (生成视频片段)          │
└───────────┬─────────────┘
            │ FILENAMES
            │
            ├─────────────────────────────┐
            │                             │
            ▼                             ▼
    后续节点处理              ┌───────────────────────┐
                              │ VRGDG_UploadVideoTo   │
                              │ Cloudinary_Auto       │
                              │                       │
                              │ - output_folder: 连接 │
                              │ - 其他云配置已预填    │
                              └───────────┬───────────┘
                                          │
                                          │ cloudinary_url
                                          ▼
                                  保存到 Cloudinary
```

### 方案 B：仅上传最终合成视频

```
┌─────────────────────────────────┐
│  VRGDG_CreateFinalVideo_SRT     │
│  (最终视频合成)                 │
│                                 │
│  - enable_cloudinary: True      │
│  - 云配置已预填                 │
└─────────────────────────────────┘
            │
            │ 自动上传最终视频到 Cloudinary
            ▼
    Cloudinary 存储桶
```

---

## Cloudinary 配置

已预填你的账户信息：
- **Cloud Name**: `dftco0cki`
- **API Key**: `192422146789215`
- **API Secret**: `HKcrrpmDGP2u0qimbuweYxfnlt4`

### 视频存储路径
- **视频片段**: `vrgamedevgirl/videos/`
- **最终视频**: `vrgamedevgirl/final_videos/`

---

## 查看上传的视频

### Cloudinary 控制台
1. 访问：https://cloudinary.com/console
2. 登录账户
3. 进入 **Media Library**
4. 查看 `vrgamedevgirl` 文件夹

### 视频 URL 格式
```
https://res.cloudinary.com/dftco0cki/video/upload/vrgamedevgirl/videos/video_xxx.mp4
```

---

## RunningHub 使用

### 问题分析
- RunningHub 只能看到本地输出文件夹的前 10 秒视频
- 无法访问完整的文件夹结构

### 解决方案
1. **每个视频片段生成后自动上传到 Cloudinary**
   - 使用 `VRGDG_UploadVideoToCloudinary_Auto` 节点
   - 连接到 Video Combine 的 `FILENAMES` 输出

2. **最终合成视频也上传到 Cloudinary**
   - 在 `VRGDG_CreateFinalVideo_SRT` 中启用 `enable_cloudinary`

3. **在 RunningHub 中使用 Cloudinary URL**
   - 从 `cloudinary_url` 输出获取 URL
   - 直接在 RunningHub 中使用 URL 引用视频

---

## 故障排除

### "Cloudinary module not available"
- 确认已运行 `pip install cloudinary`
- 重启 ComfyUI

### "Upload failed"
- 检查网络连接
- 验证 Cloudinary 凭证是否正确
- 查看 ComfyUI 控制台日志获取详细错误信息

### "No video files found"
- 确认 `output_folder` 路径正确
- 确保 Video Combine 已执行完成

---

## 文件修改列表

1. **cloudinary_storage.py** - 新建，Cloudinary 核心模块
2. **GeneralVideoNodes.py** - 添加 `VRGDG_UploadVideoToCloudinary_Auto` 节点
3. **HumoAutomation.py** - 修改 `VRGDG_CreateFinalVideo_SRT` 添加上传功能
4. **requirements.txt** - 添加 `cloudinary` 依赖

---

## 注意事项

1. **带宽限制**: Cloudinary 免费套餐有带宽限制
2. **存储空间**: 免费套餐提供有限的存储空间
3. **视频时长**: 免费套餐对单个视频时长有限制
4. **隐私设置**: 默认上传为公开可访问
