# 🎞️ BatchVideoCompressor

**BatchVideoCompressor** is a Python script for intelligently compressing video files in bulk. It analyzes the video and audio bitrate of each file, and decides whether to copy or re-encode them based on customizable thresholds. Designed for speed, quality, and ease of use.

---

## 🚀 Features

- 🔍 Automatically checks video/audio bitrate before compressing
- 📦 Skips videos that are already below the threshold
- ⚙️ Uses `ffmpeg` with progress bar and per-file feedback
- 🔊 Converts high-bitrate audio streams to AAC
- 🧹 Deletes original files after successful compression
- 🗂️ Processes multiple video formats in a folder

---

## 📅 Requirements

- Python 3.7+
- [ffmpeg](https://ffmpeg.org/) installed and accessible via command line
- Python libraries:
  ```bash
  pip install ffmpeg-python
  ```

---

## ⚙️ Usage

1. Clone this repository

2. Run the script:

   ```bash
   python compress_videos.py
   ```

3. Enter the path to the folder with video files when prompted.

4. The script will:

   - Analyze each file
   - Compress if needed
   - Move it to a `compressed/` subfolder
   - Show a live progress bar during each compression

---

## 🧠 Logic Overview

- Videos with bitrate under **20 Mbps** are skipped (you can change this).
- Audio with bitrate above **225 Kbps** is re-encoded to **AAC 192 Kbps**.
- Supported formats: `.mp4`, `.mov`, `.m4v`, `.3gp`, `.avi`, `.mkv`, `.webm`

You can easily tweak the settings at the top of the script:

```python
bitrate_video = 20  # Mbps threshold
bitrate_audio = 192  # Audio bitrate for re-encoding (in kbps)
max_bitrate_audio_for_copy = 225  # Max audio bitrate before re-encoding
```

---

## 📂 Output

Compressed videos are saved in a `compressed/` folder inside the original input folder.

---

## 📛 Notes

- Original files are deleted after successful compression.\
  If you want to keep originals, comment out this line:
  ```python
  os.remove(input_path)
  ```

---


