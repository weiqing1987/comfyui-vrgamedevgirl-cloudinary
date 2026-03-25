# Cloudinary 节点使用说明

## 快速开始

### 1. 安装依赖
```bash
pip install cloudinary
```

### 2. 重启 ComfyUI

---

## 节点说明

### 📤 **VRGDG Upload Video to Cloudinary (Auto)** ⭐ 推荐
**自动上传模式 - 用于 RunningHub 工作流**

这个节点会自动查找 Video Combine 生成的最新视频文件并上传。

#### 输入：
| 端口 | 类型 | 说明 |
|------|------|------|
| `trigger` | VHS_FILENAMES | **从 Video Combine 的 FILENAMES 输出连接** - 确保视频已保存 |
| `output_folder` | STRING | 视频输出文件夹路径（可从上游节点连接） |
| `video_name_prefix` | STRING | 视频文件名前缀，默认 `video` |
| `upload_enabled` | BOOLEAN | 是否启用上传 |

#### 输出：
| 端口 | 类型 | 说明 |
|------|------|------|
| `cloudinary_url` | STRING | **Cloudinary 公开 URL** - 用于 RunningHub |
| `public_id` | STRING | Cloudinary 资源 ID |
| `upload_success` | BOOLEAN | 上传是否成功 |
| `local_path` | STRING | 本地视频文件路径 |

---

### 📤 **VRGDG Upload Video to Cloudinary**
**手动模式 - 指定视频路径上传**

#### 输入：
| 端口 | 类型 | 说明 |
|------|------|------|
| `video_path` | STRING | 视频文件的完整路径 |
| `video_name` | STRING | 上传到 Cloudinary 的文件名 |
| `upload_enabled` | BOOLEAN | 是否启用上传 |

#### 输出：
| 端口 | 类型 | 说明 |
|------|------|------|
| `cloudinary_url` | STRING | Cloudinary 公开 URL |
| `public_id` | STRING | Cloudinary 资源 ID |
| `upload_success` | BOOLEAN | 上传是否成功 |

---

### 🎵 **VRGDG Upload Audio to Cloudinary**
**音频上传节点**

#### 输入：
| 端口 | 类型 | 说明 |
|------|------|------|
| `audio` | AUDIO | ComfyUI AUDIO 类型输入 |
| `audio_name` | STRING | 音频文件名 |
| `upload_enabled` | BOOLEAN | 是否启用上传 |

#### 输出：
| 端口 | 类型 | 说明 |
|------|------|------|
| `cloudinary_url` | STRING | Cloudinary 公开 URL |
| `public_id` | STRING | Cloudinary 资源 ID |
| `upload_success` | BOOLEAN | 上传是否成功 |

---

## RunningHub 工作流示例

### 视频生成 + 自动上传流程

```
┌─────────────────┐
│  Video Combine  │ (Video Re-Animator 或其他视频生成节点)
└────────┬────────┘
         │ FILENAMES (VHS_FILENAMES)
         ├──────────────────────────────┐
         │                              │
         │ output_folder                │
         ▼                              ▼
┌─────────────────────────────────────────────────────┐
│        VRGDG Upload Video to Cloudinary (Auto)      │
│  - trigger: 连接 Video Combine 的 FILENAMES          │
│  - output_folder: 从上游连接                         │
│  - video_name_prefix: "video"                        │
│  - upload_enabled: True                              │
└─────────────────────────────────────────────────────┘
         │
         │ cloudinary_url
         ▼
┌─────────────────────────┐
│  输出到 RunningHub       │ (使用 URL)
└─────────────────────────┘
```

### 节点连接示例

```
[Video Combine]
       │
       ├─→ IMAGE → [显示/后续处理]
       │
       └─→ FILENAMES ──→ [VRGDG Upload Video to Cloudinary (Auto)]
                              │
                              ├─→ cloudinary_url → [Save Text / 输出]
                              ├─→ public_id → [Save Text]
                              └─→ upload_success → [条件判断]
```

---

## Cloudinary 控制台

### 查看上传的文件
1. 访问：https://cloudinary.com/console
2. 登录你的账户
3. 进入 **Media Library**
4. 查看 `vrgamedevgirl/videos/` 和 `vrgamedevgirl/audio/` 文件夹

### 获取视频 URL 格式
```
https://res.cloudinary.com/dftco0cki/video/upload/v1234567890/vrgamedevgirl/videos/video_abc123.mp4
```

---

## 常见问题

### Q: 是否需要添加其他输出节点？
**A:** 不需要！`cloudinary_url` 输出是 STRING 类型，可以直接：
- 连接到 `Save Text` 节点保存为文件
- 在 RunningHub 中直接使用
- 连接到其他需要 URL 的节点

### Q: Video Combine 没有 FILENAMES 输出怎么办？
**A:** 使用 **VRGDG Upload Video to Cloudinary**（手动模式），直接指定视频路径。

### Q: 上传失败怎么办？
**A:** 检查：
1. 是否安装了 `cloudinary` 包：`pip install cloudinary`
2. 重启 ComfyUI
3. 查看控制台日志获取详细错误信息

### Q: 可以自动上传所有生成的视频吗？
**A:** 是的，将 `VRGDG Upload Video to Cloudinary (Auto)` 连接到你的工作流，每次生成视频后都会自动上传。

---

## 配置的账户信息

- **Cloud Name**: `dftco0cki`
- **视频存储路径**: `vrgamedevgirl/videos/`
- **音频存储路径**: `vrgamedevgirl/audio/`

---

## 完整工作流示例 JSON

将 Video Combine 的输出自动上传到 Cloudinary 的示例工作流已包含在 `Workflows/` 文件夹中。
