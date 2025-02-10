import customtkinter as ctk
from tkinter import ttk, filedialog
from tqdm import tqdm
from core.audio_engine import AudioMaster

class UltimateUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ultimate Audio Master 2025")
        self.geometry("1400x900")
        
        # إعدادات الواجهة
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        
        # تهيئة المحول
        self.converter = AudioMaster()
        
        # بناء الواجهة
        self._create_main_panel()
        self._create_file_list()
        self._create_controls()
        
    def _create_main_panel(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)
        
        # منطقة السحب والإفلات المتقدمة
        self.drop_zone = ctk.CTkLabel(
            self.main_frame,
            text="اسحب الملفات هنا أو انقر للتحديد",
            font=("Arial", 18),
            height=150,
            fg_color="#2d2d2d",
            corner_radius=15
        )
        self.drop_zone.pack(fill="x", pady=10)
        
    def _create_file_list(self):
        # قائمة الملفات مع تفاصيل التحويل
        self.file_list = ttk.Treeview(
            self.main_frame,
            columns=("الحالة", "الجودة", "الحجم"),
            show="headings",
            height=15
        )
        self.file_list.heading("#0", text="اسم الملف")
        self.file_list.heading("الحالة", text="الحالة")
        self.file_list.heading("الجودة", text="الجودة")
        self.file_list.heading("الحجم", text="الحجم")
        self.file_list.pack(fill="both", expand=True)
        
    def _create_controls(self):
        # لوحة التحكم الذكية
        self.control_panel = ctk.CTkFrame(self.main_frame)
        self.control_panel.pack(fill="x", pady=10)
        
        # زر التحويل المتقدم
        self.btn_convert = ctk.CTkButton(
            self.control_panel,
            text="بدء التحويل الإلهي",
            command=self.start_conversion,
            width=200,
            height=50,
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=("Arial", 14, "bold")
        )
        self.btn_convert.pack(side="right", padx=20)
        
    def start_conversion(self):
        files = filedialog.askopenfilenames(
            filetypes=[("ملفات الصوت", "*.wav *.flac *.aac *.ogg *.m4a")]
        )
        for file in files:
            output_path = os.path.splitext(file)[0] + "_converted.mp3"
            self.converter.convert_to_mp3(file, output_path)
