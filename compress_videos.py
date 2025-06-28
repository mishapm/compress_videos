import os
import shutil
import subprocess
import ffmpeg

# Настройки битрейтов (в Kbps)
bitrate_video = 20_000  # 20 Mbps
bitrate_audio = 192     # 192 Kbps
max_bitrate_audio_for_copy = 225  # если выше — перекодировать

def get_stream_info(video_path):
    try:
        probe = ffmpeg.probe(video_path)
        video_stream = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        audio_stream = next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)
        return video_stream, audio_stream
    except Exception as e:
        print(f'⚠️ Could not read file info: {video_path}\n{e}')
        return None, None

def get_bitrate_kbps(stream):
    if stream and 'bit_rate' in stream:
        return int(stream['bit_rate']) // 1000
    return 0

def get_duration(input_path):
    try:
        probe = ffmpeg.probe(input_path)
        return float(probe['format']['duration'])
    except:
        return 0

def compress_video(input_path, output_path):
    video_stream, audio_stream = get_stream_info(input_path)
    if not video_stream:
        return

    video_bitrate_kbps = get_bitrate_kbps(video_stream)
    if 0 < video_bitrate_kbps < bitrate_video:
        print(f'📋 Moving (bitrate {video_bitrate_kbps} Kbps): {os.path.basename(input_path)}')
        shutil.move(input_path, output_path)
        return

    fps_str = video_stream.get('avg_frame_rate', '30/1')
    try:
        num, den = map(int, fps_str.split('/'))
        fps = num / den if den else 30
    except:
        fps = 30

    duration = get_duration(input_path)
    if duration == 0:
        print(f'⚠️ Could not get duration: {input_path}')
        return

    audio_codec = 'copy'
    audio_bitrate = None
    if audio_stream:
        ab = get_bitrate_kbps(audio_stream)
        if ab >= max_bitrate_audio_for_copy:
            audio_codec = 'aac'
            audio_bitrate = f'{bitrate_audio}k'

    # Build ffmpeg command
    cmd = [
        'ffmpeg', '-i', input_path,
        '-c:v', 'libx264',
        '-b:v', f'{bitrate_video}k',
        '-r', str(fps)
    ]
    if audio_stream:
        cmd += ['-c:a', audio_codec]
        if audio_bitrate:
            cmd += ['-b:a', audio_bitrate]
    else:
        cmd += ['-an']
    
    cmd += [
        '-progress', 'pipe:1',
        '-nostats',
        '-loglevel', 'error',
        '-y',
        output_path
    ]

    try:
        print(f'🛠️ Starting compression: {os.path.basename(input_path)}')
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                 text=True, bufsize=1)
        
        last_percent = -1
        filename = os.path.basename(input_path)
        
        for line in process.stdout:
            line = line.strip()
            if line.startswith("out_time_ms="):
                try:
                    out_time_us = int(line.split('=')[1])
                    current_seconds = out_time_us / 1_000_000
                    percent = min(int((current_seconds / duration) * 100), 100)
                    
                    if percent != last_percent and percent >= 0:
                        bar_length = 30
                        filled = int((percent / 100) * bar_length)
                        bar = '█' * filled + '░' * (bar_length - filled)
                        
                        print(f'\r🛠️ {filename}: [{bar}] {percent}% ({current_seconds:.1f}s/{duration:.1f}s)', 
                              end='', flush=True)
                        last_percent = percent
                except (ValueError, ZeroDivisionError):
                    continue
            elif line.startswith("progress=end"):
                bar = '█' * 30
                print(f'\r🛠️ {filename}: [{bar}] 100% ({duration:.1f}s/{duration:.1f}s)', 
                      end='', flush=True)
                break
        
        return_code = process.wait()
        
        if return_code == 0:
            print(f'\n✅ Compressed: {filename}')
            os.remove(input_path)
        else:
            stderr_output = process.stderr.read()
            print(f'\n❌ FFmpeg failed: {filename}')
            if stderr_output:
                print(f'Error details: {stderr_output}')
            if os.path.exists(output_path):
                os.remove(output_path)
                
    except Exception as e:
        print(f'\n❌ Unexpected error: {os.path.basename(input_path)} - {str(e)}')

def batch_compress(folder):
    output_dir = os.path.join(folder, 'compressed')
    os.makedirs(output_dir, exist_ok=True)

    extensions = ('.mp4', '.mov', '.m4v', '.3gp', '.avi', '.mkv', '.webm')
    files = [f for f in os.listdir(folder) if f.lower().endswith(extensions) and 
             os.path.isfile(os.path.join(folder, f))]
    total = len(files)

    if total == 0:
        print("❌ No video files found in the folder!")
        return

    print(f"📁 Found {total} video file(s) to process\n")

    for idx, filename in enumerate(files, 1):
        input_path = os.path.join(folder, filename)
        output_path = os.path.join(output_dir, filename)
        
        if os.path.exists(output_path):
            print(f'⏭️ Skipping (already exists): {filename}')
            continue
            
        print(f'\n📦 Processing {idx}/{total}: {filename}')
        compress_video(input_path, output_path)

    print('\n🎉 All files processed!')

if __name__ == '__main__':
    folder = input("📁 Enter path to folder with videos: ").strip('"')
    if not os.path.isdir(folder):
        print("❌ Invalid folder path!")
    else:
        batch_compress(folder)
