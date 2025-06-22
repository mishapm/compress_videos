# Video Compressor Script

This Python script automates video compression by analyzing and processing video and audio bitrates in a given folder. It is designed to reduce file sizes while maintaining quality thresholds.

## Features

- Scans a specified folder for **video files only**.
- **Skips** all non-video files.
- **Moves videos** to a target folder if the video bitrate is **below 15 Mbps**.
- **Audio processing**:
  - If audio bitrate is **below 194 kbps**, it is copied without re-encoding (`-c:a copy`).
  - If audio bitrate is **194 kbps or higher**, it is re-encoded to **194 kbps**.
- **Video processing**:
  - Re-encodes the video to **15 Mbps** using the **original frame rate** (FPS).
- The output is saved to a `compressed` folder with the **same file name** as the original.

## Requirements

- [Python 3.x](https://www.python.org/)
- [`ffmpeg`](https://ffmpeg.org/)
- [`ffmpeg-python`](https://pypi.org/project/ffmpeg-python/)

## Installation

1. **Install ffmpeg-python**:
   ```bash
   pip install ffmpeg-python
   ```

2. **Check if FFmpeg is installed**

   Open a Command Prompt and run:

   ```bash
   ffmpeg -version
   ```

   If the command is not recognized, you need to install FFmpeg.

3. **Install FFmpeg (if not already installed)**

   - Download FFmpeg from [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
   - Choose: **Release full build (ZIP)**
   - Extract it to a folder (e.g., `C:\ffmpeg`)
   - Ensure the path to the binary looks like: `C:\ffmpeg\bin\ffmpeg.exe`

4. **Add FFmpeg to the PATH (Windows only)**

   - Open: **Start Menu → Search “Environment Variables”**
   - Under **System variables**, find `Path` → Click **Edit**
   - Click **New** and paste the path:
     ```
     C:\ffmpeg\bin
     ```
   - Click **OK** on all dialogs.

5. **Verify Installation**

   Open a new Command Prompt window and run:

   ```bash
   ffmpeg -version
   ```

   If you see the version info — you're good to go ✅