# 🎮 VRGameDevGirl's Video / Image & HUMO Workflow Nodes for ComfyUI (+ Cloudinary)

Custom ComfyUI nodes for **music video workflows** and **high-quality video/image enhancement**.
Includes HUMO-based multi-scene workflows, audio splitting, video combining, and realtime-ready enhancement tools.

**☁️ Cloudinary Integration:** This fork adds Cloudinary cloud storage integration for automatic video/audio upload.

---

# 🎬 AI Music Video Workflow (ComfyUI)

Turn a **reference image** and an **audio track** into a fully **AI-generated music video**.
The workflow automatically splits lyrics, generates scene prompts, and syncs everything into a cinematic final video.

## 🚀 How it Works
1. Upload a **reference image** (your main character).
2. Import your **audio file** (with lyric syncing).
3. Set a **folder name** for outputs.
4. Customize the **Prompt Creator** to define style, mood, and scenes.

✨ Everything else — transcription, scene building, video chunks, and final rendering — runs automatically.
The result: a stylized, synced **AI-driven music video**.

---

## 🌟 Features

### Core Video Nodes
- 🎞️ **Fast Film Grain** (`FastFilmGrain`)
  Add controllable, grayscale or color grain for cinematic texture.
  ➕ *Now includes a `batch_size` setting to reduce out-of-memory (OOM) issues on long or high-res videos.*

- 🎨 **Color Match to Reference** (`ColorMatchToReference`)
  Align image tones to a reference image using LAB color matching.

- 🎯 **Fast Unsharp Sharpen** (`FastUnsharpSharpen`)
  Simple and efficient sharpening using unsharp masking.

- 🌀 **Fast Laplacian Sharpen** (`FastLaplacianSharpen`)
  Edge-based sharpening via Laplacian kernel for crisp detail.

- 📏 **Fast Sobel Sharpen** (`FastSobelSharpen`)
  Gradient-based edge enhancement using Sobel filters.

### ☁️ Cloudinary Integration (NEW)
- 📤 **VRGDG_CreateFinalVideo_SRT** - Auto-upload final video to Cloudinary
- 📤 **VRGDG_UploadVideoToCloudinary_Auto** - Upload video segments (optional)
- 🎵 **VRGDG_UploadAudioToCloudinary** - Upload audio files to Cloudinary

Features:
- Automatic upload of final synthesized video
- Cloudinary URLs returned as node outputs
- Perfect for RunningHub workflow integration
- Configurable cloud storage folder structure

---

## 📦 Installation

### Method 1: Clone from GitHub (Recommended)

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/weiqing1987/comfyui-vrgamedevgirl-cloudinary.git
cd comfyui-vrgamedevgirl-cloudinary
```

### Method 2: Manual Download
1. Download this repository as a ZIP file
2. Extract to your `ComfyUI/custom_nodes` directory
3. Rename the folder to `comfyui-vrgamedevgirl`

### Install Dependencies

**Step 1: Install ComfyUI Manager** (Required)
```bash
# From your ComfyUI root directory
pip install -U --pre comfyui-manager

# Or if using embedded Python
python_embeded/python.exe -m pip install -U --pre comfyui-manager
```

**Step 2: Install Python Packages**
```bash
# From your ComfyUI root directory
pip install -r custom_nodes/comfyui-vrgamedevgirl/requirements.txt

# Or if using embedded Python
python_embeded/python.exe -m pip install -r custom_nodes/comfyui-vrgamedevgirl/requirements.txt
```

**Step 3: Restart ComfyUI**

---

## ✨ Requirements

### Python Packages

See `requirements.txt` for the full list:

```
kornia
librosa
imageio
torchcodec
google-generativeai
av
stable-ts
demucs
transformers
accelerate
huggingface_hub
cloudinary
```

---

## 🧠 Node Details

### Core Video Enhancement Nodes

#### ✅ Fast Film Grain (`FastFilmGrain`)
Adds customizable film grain to each frame.

**Inputs:**
- `images`: Frame tensor input
- `grain_intensity`: Blend amount (0 to 1)
- `saturation_mix`: 0 = grayscale grain, 1 = full RGB noise

#### 🎨 Color Match to Reference (`ColorMatchToReference`)
Matches image color distribution to a reference image using LAB space normalization.

**Inputs:**
- `images`: Your video frames
- `reference_image`: A single image to match tone and color against
- `match_strength`: Blend between original and matched (0.0–1.0)

#### 🎯 Fast Unsharp Sharpen (`FastUnsharpSharpen`)
Applies unsharp masking to enhance edges.

**Inputs:**
- `images`: Input image tensor
- `strength`: Sharpening amount (0.0 to 2.0)

#### 🌀 Fast Laplacian Sharpen (`FastLaplacianSharpen`)
Enhances edges by applying a Laplacian kernel.

**Inputs:**
- `images`: Input image tensor
- `strength`: Sharpening amount (0.0 to 2.0)

#### 📏 Fast Sobel Sharpen (`FastSobelSharpen`)
Uses Sobel filters to detect image gradients and amplify edge contrast.

**Inputs:**
- `images`: Input image tensor
- `strength`: Sharpening amount (0.0 to 2.0)

---

### ☁️ Cloudinary Nodes

#### 📤 VRGDG_CreateFinalVideo_SRT
Creates final video from segments and optionally uploads to Cloudinary.

**Inputs:**
- `trigger`: VHS_FILENAMES from video combine node
- `audio`: Audio file for the final video
- `threshold`: Minimum number of segments before creating final video
- `group_list`: Group ID for rerun mode (optional)
- `video_folder`: Output folder path

**Cloudinary Settings (in widget panel):**
- `enable_cloudinary`: Enable/disable cloud upload
- `cloudinary_cloud_name`: Your Cloudinary cloud name
- `cloudinary_api_key`: Your API key
- `cloudinary_api_secret`: Your API secret

**Output:**
- Final video saved locally
- Cloudinary URL printed to console (if upload enabled)

#### 🎵 VRGDG_UploadAudioToCloudinary
Upload audio files to Cloudinary storage.

**Inputs:**
- `audio`: Audio tensor
- `audio_name`: Name for the uploaded file
- `upload_enabled`: Enable/disable upload

**Outputs:**
- `cloudinary_url`: Full URL to the uploaded audio
- `public_id`: Cloudinary public ID
- `upload_success`: Boolean indicating success

---

## 🔧 Cloudinary Configuration

### Getting Your Cloudinary Credentials

1. Go to [Cloudinary Console](https://console.cloudinary.com/)
2. Sign up or log in
3. Find your credentials in the Dashboard:
   - **Cloud Name** (e.g., `dftco0cki`)
   - **API Key** (e.g., `192422146789215`)
   - **API Secret** (e.g., `HKcrrpmDGP2u0qimbuweYxfnlt4`)

### Free Tier Limits

Cloudinary free tier includes:
- 25 GB storage
- 25 GB bandwidth/month
- 25,000 transformations/month

For most music video projects, this is sufficient!

---

## 🛠️ Roadmap

- [x] 🎞️ Fast Film Grain (`FastFilmGrain`)
- [x] 🎨 Color Match To Reference (`ColorMatchToReference`)
- [x] 📏 Fast Sobel Sharpen (`FastSobelSharpen`)
- [x] 🌀 Fast Laplacian Sharpen (`FastLaplacianSharpen`)
- [x] 🎯 Fast Unsharp Sharpen (`FastUnsharpSharpen`)
- [x] ☁️ Cloudinary Video Upload Integration
- [x] 🎵 Cloudinary Audio Upload Integration
- [ ] 🌫️ Local Contrast / Dehaze
- [ ] 🎛️ LUT Loader or Approximate Match

---

## 📁 Folder Structure

```
comfyui-vrgamedevgirl/
│
├── __init__.py
├── HumoAutomation.py         # Final video creation + Cloudinary
├── GeneralVideoNodes.py      # Video enhancement nodes
├── VRGDG_AudioNodes.py       # Audio processing + Cloudinary upload
├── cloudinary_storage.py     # Cloudinary integration
├── requirements.txt
├── README.md
├── LICENSE
└── ... (other nodes)
```

---

## 🧑‍💻 Author

**VRGameDevGirl**
✨ Custom tools for cinematic AI workflows
💌 Questions or collabs? Reach out via GitHub

---

## 📜 License

This project is licensed under the MIT License.

---

## 🔗 Links

- [Original Repository](https://github.com/vrgamegirl19/comfyui-vrgamedevgirl)
- [Cloudinary Fork Repository](https://github.com/weiqing1987/comfyui-vrgamedevgirl-cloudinary)
- [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager)
