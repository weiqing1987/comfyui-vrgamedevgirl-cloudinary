# Cloudinary 简化使用说明

## 节点：VRGDG_LoadAudioSplit_General

这个节点已经集成了 Cloudinary 上传功能，用于 RunningHub 输出。

---

## 使用方法

### 1. 安装依赖
```bash
pip install cloudinary
```

### 2. 重启 ComfyUI

### 3. 在节点中配置

在 **VRGDG_LoadAudioSplit_General** 节点中，你会看到以下新增选项：

#### Cloudinary 设置区域：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `enable_cloudinary` | False | 开启后会在 output_folder 基础上生成 Cloudinary URL |
| `cloudinary_cloud_name` | dftco0cki | Cloudinary 云名称 |
| `cloudinary_api_key` | 192422146789215 | API 密钥 |
| `cloudinary_api_secret` | HKcrrpmDGP2u0qimbuweYxfnlt4 | API 密钥（密码） |

---

## 输出说明

节点新增了一个输出端口：

| 端口 | 类型 | 说明 |
|------|------|------|
| `cloudinary_url` | STRING | Cloudinary URL 基础路径，用于 RunningHub |

---

## 工作流示例

```
┌─────────────────────────────┐
│ VRGDG_LoadAudioSplit_General│
│                             │
│ [Cloudinary 设置]            │
│ - enable_cloudinary: True   │
│ - cloud_name: dftco0cki     │
│ - api_key: 192422146789215  │
│ - api_secret: HKcr...       │
└─────────────┬───────────────┘
              │
              ├─→ output_folder → 本地文件夹路径
              │
              └─→ cloudinary_url → Cloudinary URL 基础路径
```

---

## 注意事项

1. **当前版本仅生成 URL 基础路径**
   - `cloudinary_url` 输出的是文件夹路径
   - 格式：`https://res.cloudinary.com/{cloud_name}/video/upload/{folder}`

2. **如需自动上传视频文件**
   - 使用 `VRGDG_UploadVideoToCloudinary` 节点
   - 连接到 Video Combine 的输出

3. **RunningHub 使用**
   - 将 `cloudinary_url` 连接到你的输出节点
   - 或使用 `Save Text` 节点保存为文件

---

## Cloudinary 控制台

查看上传的文件：
- 网址：https://cloudinary.com/console
- 文件夹：`vrgamedevgirl/videos/`
