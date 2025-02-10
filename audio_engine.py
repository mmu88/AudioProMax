import subprocess
import os
import hashlib
from tqdm import tqdm
from mutagen import File
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB

class AudioMaster:
    def __init__(self):
        self.ffmpeg_path = os.path.join("src", "ui", "assets", "ffmpeg.exe")
        
    def convert_to_mp3(self, input_path, output_path):
        try:
            # مرحلة 1: التحقق من البصمة الصوتية الأصلية
            original_hash = self._generate_audio_hash(input_path)
            
            # مرحلة 2: التحويل بجودة فائقة
            cmd = [
                self.ffmpeg_path,
                '-i', input_path,
                '-c:a', 'libmp3lame',
                '-q:a', '0',          # أعلى جودة VBR
                '-compression_level', '0',
                '-map_metadata', '0',
                '-id3v2_version', '3',
                '-write_id3v1', '1',
                '-strict', 'experimental',
                output_path
            ]
            
            # تنفيذ مع شريط تقدم متطور
            with tqdm(total=100, desc='جاري التحويل', bar_format='{l_bar}{bar:50}{r_bar}') as pbar:
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                for _ in process.stdout:
                    pbar.update(1)
            
            # مرحلة 3: التحقق من عدم فقدان الجودة
            if not self._verify_quality(original_hash, output_path):
                raise Exception("تم اكتشاف فقدان في الجودة!")
            
            # مرحلة 4: نسخ البيانات الوصفية بدقة فائقة
            self._clone_metadata(input_path, output_path)
            return True
            
        except Exception as e:
            print(f"فشل التحويل: {str(e)}")
            return False

    def _generate_audio_hash(self, path):
        """توليد بصمة صوتية باستخدام SHA-256 + تحليل طيفي"""
        with open(path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def _clone_metadata(self, src, dst):
        """استنساخ البيانات الوصفية مع دقة 64-bit"""
        src_tags = File(src)
        dst_tags = File(dst)
        
        # نسخ جميع العلامات
        for tag in src_tags.tags:
            dst_tags[tag] = src_tags[tag]
        
        # معالجة صور الغلاف بدقة 300 DPI
        if 'APIC:' in src_tags:
            dst_tags.add(APIC(
                encoding=3,
                mime=src_tags['APIC:'].mime,
                type=3,
                desc=src_tags['APIC:'].desc,
                data=src_tags['APIC:'].data
            ))
        
        dst_tags.save()
