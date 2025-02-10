import subprocess
import os
from mutagen import File
from mutagen.id3 import ID3, APIC

class AudioConverter:
    def __init__(self):
        self.ffmpeg_path = os.path.join("src", "ui", "assets", "ffmpeg.exe")
        
    def convert(self, input_path, output_path, format='mp3'):
        codec_config = {
            'mp3': ['-c:a', 'libmp3lame', '-q:a', '0'],
            'flac': ['-c:a', 'flac', '-compression_level', '12'],
            'wav': ['-c:a', 'pcm_s24le'],
            'aac': ['-c:a', 'libfdk_aac', '-vbr', '5'],
            'ogg': ['-c:a', 'libvorbis', '-q:a', '10']
        }
        
        cmd = [
            self.ffmpeg_path,
            '-i', input_path,
            '-map_metadata', '0',
            '-id3v2_version', '3',
            *codec_config.get(format, ['-c:a', 'copy']),
            output_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            self._preserve_metadata(input_path, output_path)
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

    def _preserve_metadata(self, src, dst):
        src_tags = File(src)
        dst_tags = File(dst)
        
        # نسخ كل البيانات الوصفية
        for tag in src_tags.tags:
            dst_tags[tag] = src_tags[tag]
        
        # معالجة صور الغلاف
        if 'APIC:' in src_tags:
            dst_tags.add(APIC(
                encoding=3,
                mime=src_tags['APIC:'].mime,
                type=3,
                desc=src_tags['APIC:'].desc,
                data=src_tags['APIC:'].data
            ))
        
        dst_tags.save()
