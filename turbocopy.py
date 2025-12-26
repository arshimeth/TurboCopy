import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
import subprocess
import threading
import sys
import os
import json
from tkinter import filedialog
from plyer import notification

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

LANGUAGES = {
    "tr": {
        "label": "Türkçe",
        "title": "TurboCopy",
        "drag_info": "(Klasörleri kutucuklara sürükleyebilirsiniz)",
        "source": "Kaynak:",
        "dest": "Hedef:",
        "browse": "Seç",
        "speed_lbl": "Hız Modu:",
        "speeds": ["🐢 Yavaş", "🚗 Orta", "🚀 Turbo"],
        "speed_info": "• Yavaş: PC kasmaz, arkada çalışır.\n• Orta: Standart dengeli hız.\n• Turbo: Tam performans (Sistem donabilir).",
        "shutdown": "İşlem bitince bilgisayarı kapat",
        "start_btn": "KOPYALAMAYI BAŞLAT",
        "log_ready": "Hazır...",
        "conflict_title": "Çakışma Ayarı",
        "conflict_msg": "Hedefte aynı isimde dosya varsa ne yapılsın?",
        "btn_overwrite": "1. Üzerine Yaz",
        "tip_overwrite": "DİKKAT! Hedefteki dosya ile kaynak aynı olsa bile hedefi ezer.",
        "btn_skip": "2. Atla (Pas Geç)",
        "tip_skip": "Hedefte dosya varsa dokunmaz. En hızlı yöntemdir.",
        "btn_update": "3. Akıllı Güncelleme",
        "tip_update": "ÖNERİLEN! Sadece kaynak dosya daha YENİ ise kopyalar.",
        "tip_hover": "*Detay için fareyi butonlarda tutun.",
        "done_title": "Tamamlandı",
        "done_msg": "Kopyalama işlemi bitti.",
        "err_empty": "HATA: Kaynak veya Hedef boş olamaz.",
        "cancel": "İptal edildi."
    },
    "en": {
        "label": "English",
        "title": "TurboCopy",
        "drag_info": "(You can drag & drop folders here)",
        "source": "Source:",
        "dest": "Target:",
        "browse": "Select",
        "speed_lbl": "Speed Mode:",
        "speeds": ["🐢 Slow", "🚗 Medium", "🚀 Turbo"],
        "speed_info": "• Slow: Background task, low CPU usage.\n• Medium: Balanced standard speed.\n• Turbo: Max performance (System may lag).",
        "shutdown": "Shutdown PC when finished",
        "start_btn": "START COPYING",
        "log_ready": "Ready...",
        "conflict_title": "Conflict Resolution",
        "conflict_msg": "File exists in destination. What to do?",
        "btn_overwrite": "1. Overwrite",
        "tip_overwrite": "WARNING! Replaces destination file even if identical.",
        "btn_skip": "2. Skip",
        "tip_skip": "Ignores existing files. Fastest method.",
        "btn_update": "3. Smart Update",
        "tip_update": "RECOMMENDED! Copies only if source is NEWER.",
        "tip_hover": "*Hover over buttons for details.",
        "done_title": "Finished",
        "done_msg": "Copy operation completed.",
        "err_empty": "ERROR: Source or Target cannot be empty.",
        "cancel": "Cancelled."
    },
    "ar": { 
        "label": "العربية",
        "title": "تيربو كوبي",
        "drag_info": "(يمكنك سحب وإفلات المجلدات هنا)",
        "source": "المصدر:",
        "dest": "الوجهة:",
        "browse": "تحديد",
        "speed_lbl": "وضع السرعة:",
        "speeds": ["🐢 بطيء", "🚗 متوسط", "🚀 تيربو"],
        "speed_info": "• بطيء: لا يؤثر على الجهاز، يعمل في الخلفية.\n• متوسط: سرعة قياسية متوازنة.\n• تيربو: أقصى أداء (قد يتجمد النظام).",
        "shutdown": "إيقاف تشغيل الكمبيوتر عند الانتهاء",
        "start_btn": "بدء النسخ",
        "log_ready": "جاهز...",
        "conflict_title": "إعداد التعارض",
        "conflict_msg": "الملف موجود في الوجهة. ماذا تريد أن تفعل؟",
        "btn_overwrite": "1. استبدال",
        "tip_overwrite": "تحذير! يستبدل الملف في الوجهة حتى لو كان متطابقاً.",
        "btn_skip": "2. تخطي",
        "tip_skip": "يتجاهل الملفات الموجودة. أسرع طريقة.",
        "btn_update": "3. تحديث ذكي",
        "tip_update": "موصى به! ينسخ فقط إذا كان المصدر أحدث.",
        "tip_hover": "*مرر الماوس فوق الأزرار للتفاصيل.",
        "done_title": "تم الانتهاء",
        "done_msg": "اكتملت عملية النسخ.",
        "err_empty": "خطأ: المصدر أو الوجهة فارغة.",
        "cancel": "تم الإلغاء."
    },
    "it": {
        "label": "Italiano",
        "title": "TurboCopy",
        "drag_info": "(Trascina le cartelle qui)",
        "source": "Origine:",
        "dest": "Destinaz:",
        "browse": "Scegli",
        "speed_lbl": "Velocità:",
        "speeds": ["🐢 Lento", "🚗 Medio", "🚀 Turbo"],
        "speed_info": "• Lento: Basso utilizzo CPU.\n• Medio: Velocità bilanciata.\n• Turbo: Massima performance.",
        "shutdown": "Spegni PC al termine",
        "start_btn": "AVVIA COPIA",
        "log_ready": "Pronto...",
        "conflict_title": "Conflitto",
        "conflict_msg": "Il file esiste. Cosa fare?",
        "btn_overwrite": "1. Sovrascrivi",
        "tip_overwrite": "ATTENZIONE! Sostituisce tutto.",
        "btn_skip": "2. Salta",
        "tip_skip": "Ignora file esistenti.",
        "btn_update": "3. Aggiorn. Smart",
        "tip_update": "Solo se più recente.",
        "tip_hover": "*Passa il mouse per dettagli.",
        "done_title": "Finito",
        "done_msg": "Copia completata.",
        "err_empty": "ERRORE: Origine/Destinazione vuota.",
        "cancel": "Annullato."
    },
    "jp": {
        "label": "日本語",
        "title": "TurboCopy",
        "drag_info": "(ここにフォルダをドラッグ＆ドロップ)",
        "source": "コピー元:",
        "dest": "コピー先:",
        "browse": "選択",
        "speed_lbl": "速度:",
        "speeds": ["🐢 低速", "🚗 中速", "🚀 高速"],
        "speed_info": "• 低速: バックグラウンド作業用。\n• 中速: 標準速度。\n• 高速: 最大パフォーマンス (PCが重くなる可能性があります)。",
        "shutdown": "完了後にPCをシャットダウン",
        "start_btn": "コピー開始",
        "log_ready": "準備完了...",
        "conflict_title": "競合設定",
        "conflict_msg": "同名のファイルが存在します。どうしますか？",
        "btn_overwrite": "1. 上書き",
        "tip_overwrite": "注意！ 強制的に上書きします。",
        "btn_skip": "2. スキップ",
        "tip_skip": "既存ファイルを無視します。",
        "btn_update": "3. スマート更新",
        "tip_update": "推奨！ 新しいファイルのみコピーします。",
        "tip_hover": "*詳細はボタンの上にマウスを置いてください。",
        "done_title": "完了",
        "done_msg": "コピーが完了しました。",
        "err_empty": "エラー: コピー元または先が空です。",
        "cancel": "キャンセルされました。"
    },
    "fr": {
        "label": "Français",
        "title": "TurboCopy",
        "drag_info": "(Glissez-déposez les dossiers ici)",
        "source": "Source:",
        "dest": "Cible:",
        "browse": "Ouvrir",
        "speed_lbl": "Vitesse:",
        "speeds": ["🐢 Lent", "🚗 Moyen", "🚀 Turbo"],
        "speed_info": "• Lent: Tâche de fond.\n• Moyen: Vitesse standard.\n• Turbo: Perf. max (Système peut ralentir).",
        "shutdown": "Éteindre PC à la fin",
        "start_btn": "DÉMARRER",
        "log_ready": "Prêt...",
        "conflict_title": "Conflit",
        "conflict_msg": "Fichier existant. Que faire?",
        "btn_overwrite": "1. Écraser",
        "tip_overwrite": "ATTENTION! Remplace tout.",
        "btn_skip": "2. Ignorer",
        "tip_skip": "Ignore les fichiers existants.",
        "btn_update": "3. Maj Intelligente",
        "tip_update": "Copie seulement si plus récent.",
        "tip_hover": "*Survolez pour détails.",
        "done_title": "Terminé",
        "done_msg": "Copie terminée.",
        "err_empty": "ERREUR: Source/Cible vide.",
        "cancel": "Annulé."
    },
    "ru": {
        "label": "Русский",
        "title": "TurboCopy",
        "drag_info": "(Перетащите папки сюда)",
        "source": "Ист:",
        "dest": "Цель:",
        "browse": "Выбор",
        "speed_lbl": "Скорость:",
        "speeds": ["🐢 Медл.", "🚗 Сред.", "🚀 Турбо"],
        "speed_info": "• Медленно: Фоновый режим.\n• Средне: Стандарт.\n• Турбо: Макс. скорость.",
        "shutdown": "Выключить ПК",
        "start_btn": "НАЧАТЬ",
        "log_ready": "Готов...",
        "conflict_title": "Конфликт",
        "conflict_msg": "Файл существует. Действие?",
        "btn_overwrite": "1. Перезаписать",
        "tip_overwrite": "ВНИМАНИЕ! Заменяет всё.",
        "btn_skip": "2. Пропустить",
        "tip_skip": "Самый быстрый метод.",
        "btn_update": "3. Обновить",
        "tip_update": "Только новые файлы.",
        "tip_hover": "*Наведите курсор для деталей.",
        "done_title": "Готово",
        "done_msg": "Копирование завершено.",
        "err_empty": "ОШИБКА: Укажите пути.",
        "cancel": "Отменено."
    },
    "zh": {
        "label": "中文",
        "title": "TurboCopy",
        "drag_info": "(将文件夹拖放到此处)",
        "source": "来源:",
        "dest": "目标:",
        "browse": "选择",
        "speed_lbl": "速度模式:",
        "speeds": ["🐢 慢速", "🚗 中速", "🚀 急速"],
        "speed_info": "• 慢速: 后台运行，不卡顿。\n• 中速: 标准平衡速度。\n• 急速:以此性能运行 (系统可能卡顿)。",
        "shutdown": "完成后关闭电脑",
        "start_btn": "开始复制",
        "log_ready": "准备就绪...",
        "conflict_title": "冲突设置",
        "conflict_msg": "目标中存在同名文件，如何处理？",
        "btn_overwrite": "1. 覆盖",
        "tip_overwrite": "警告！将强制覆盖目标文件。",
        "btn_skip": "2. 跳过",
        "tip_skip": "忽略现有文件。最快的方法。",
        "btn_update": "3. 智能更新",
        "tip_update": "推荐！仅当源文件较新时复制。",
        "tip_hover": "*将鼠标悬停在按钮上查看详情。",
        "done_title": "完成",
        "done_msg": "复制操作已完成。",
        "err_empty": "错误: 来源或目标不能为空。",
        "cancel": "已取消。"
    }
}

class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

class CTkToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text: return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10
        self.tooltip_window = ctk.CTkToplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        self.tooltip_window.attributes('-topmost', True)
        label = ctk.CTkLabel(self.tooltip_window, text=self.text, fg_color="#333333", 
                             text_color="#FFFFFF", corner_radius=6, width=250, 
                             wraplength=240, padx=10, pady=10)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class ConflictDialog(ctk.CTkToplevel):
    def __init__(self, parent, lang_code="en"):
        super().__init__(parent)
        self.lang = LANGUAGES[lang_code]
        self.title(self.lang["conflict_title"])
        self.geometry("450x400")
        self.resizable(False, False)
        self.choice = None 
        self.transient(parent)
        self.grab_set() 
        self.attributes('-topmost', True)

        ctk.CTkLabel(self, text=self.lang["conflict_msg"], font=("Arial", 16, "bold"), wraplength=400).pack(pady=20)

        btn1 = ctk.CTkButton(self, text=self.lang["btn_overwrite"], fg_color="#C0392B", hover_color="#922B21", height=40,
                             command=lambda: self.set_choice("OVERWRITE"))
        btn1.pack(pady=10, padx=40, fill="x")
        CTkToolTip(btn1, self.lang["tip_overwrite"])

        btn2 = ctk.CTkButton(self, text=self.lang["btn_skip"], fg_color="#F39C12", hover_color="#B9770E", height=40,
                             command=lambda: self.set_choice("SKIP"))
        btn2.pack(pady=10, padx=40, fill="x")
        CTkToolTip(btn2, self.lang["tip_skip"])

        btn3 = ctk.CTkButton(self, text=self.lang["btn_update"], fg_color="#27AE60", hover_color="#1E8449", height=40,
                             command=lambda: self.set_choice("UPDATE"))
        btn3.pack(pady=10, padx=40, fill="x")
        CTkToolTip(btn3, self.lang["tip_update"])
        
        ctk.CTkLabel(self, text=self.lang["tip_hover"], font=("Arial", 10), text_color="gray").pack(pady=20)

    def set_choice(self, choice):
        self.choice = choice
        self.destroy()

class TurboCopyApp(Tk):
    def __init__(self):
        super().__init__()
        
        self.config_file = self.get_config_path()
        self.current_lang = self.load_config()
        
        self.setup_ui_basic()
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.current_process = None
        
        self.auto_start_mode = False
        self.initial_source = ""
        if len(sys.argv) > 1:
            self.initial_source = sys.argv[1]
            self.auto_start_mode = True

        self.create_widgets()
        self.update_language()

        if self.auto_start_mode:
            self.after(500, self.ask_destination_and_start)

    def get_config_path(self):
        if getattr(sys, 'frozen', False):
            app_path = os.path.dirname(sys.executable)
        else:
            app_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(app_path, "config.json")

    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("language", "en")
        except:
            pass
        return "en"

    def save_config(self):
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump({"language": self.current_lang}, f)
        except:
            pass

    def setup_ui_basic(self):
        self.title("TurboCopy v3.2")
        self.geometry("600x700")
        self.resizable(False, False)

    def change_language(self, choice):
        lang_map = {
            "Türkçe": "tr", "English": "en", "العربية": "ar", 
            "Italiano": "it", "日本語": "jp", "Français": "fr", 
            "Русский": "ru", "中文": "zh"
        }
        self.current_lang = lang_map.get(choice, "en")
        
        self.save_config()
        self.update_language()

    def update_language(self):
        L = LANGUAGES[self.current_lang]
        
        self.title(L["title"])
        self.lbl_title.configure(text=L["title"])
        self.lbl_drag_info.configure(text=L["drag_info"])
        self.lbl_source.configure(text=L["source"])
        self.lbl_dest.configure(text=L["dest"])
        self.btn_browse_src.configure(text=L["browse"])
        self.btn_browse_dest.configure(text=L["browse"])
        self.lbl_speed_title.configure(text=L["speed_lbl"])
        self.seg_speed.configure(values=L["speeds"])
        self.seg_speed.set(L["speeds"][1]) 
        self.lbl_speed_info.configure(text=L["speed_info"])
        self.check_shutdown.configure(text=L["shutdown"])
        self.btn_start.configure(text=L["start_btn"])
        
        self.opt_lang.set(L["label"])
        
        current_text = self.textbox_log.get("1.0", "end").strip()
        if not current_text:
            self.log(L["log_ready"])

    def create_widgets(self):
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.pack(pady=(10,0), padx=20, fill="x")
        
        self.lbl_title = ctk.CTkLabel(self.frame_top, text="TurboCopy", font=("Arial", 24, "bold"))
        self.lbl_title.pack(side="left")

        self.opt_lang = ctk.CTkOptionMenu(self.frame_top, width=100,
                                          values=["English", "Türkçe", "العربية", "Italiano", "日本語", "Français", "Русский", "中文"],
                                          command=self.change_language)
        self.opt_lang.pack(side="right")
        
        self.lbl_drag_info = ctk.CTkLabel(self, text="...", font=("Arial", 11), text_color="gray")
        self.lbl_drag_info.pack(pady=(0,10))

        self.frame_source = ctk.CTkFrame(self)
        self.frame_source.pack(pady=5, padx=20, fill="x")
        self.lbl_source = ctk.CTkLabel(self.frame_source, text="Src:", width=60)
        self.lbl_source.pack(side="left", padx=5)
        self.entry_source = ctk.CTkEntry(self.frame_source)
        self.entry_source.pack(side="left", fill="x", expand=True, padx=5, pady=10)
        self.entry_source.drop_target_register(DND_FILES)
        self.entry_source.dnd_bind('<<Drop>>', self.drop_source)
        if self.initial_source: self.entry_source.insert(0, self.initial_source)
        self.btn_browse_src = ctk.CTkButton(self.frame_source, text="...", width=50, command=self.browse_source)
        self.btn_browse_src.pack(side="right", padx=10)

        self.frame_dest = ctk.CTkFrame(self)
        self.frame_dest.pack(pady=5, padx=20, fill="x")
        self.lbl_dest = ctk.CTkLabel(self.frame_dest, text="Dst:", width=60)
        self.lbl_dest.pack(side="left", padx=5)
        self.entry_dest = ctk.CTkEntry(self.frame_dest)
        self.entry_dest.pack(side="left", fill="x", expand=True, padx=5, pady=10)
        self.entry_dest.drop_target_register(DND_FILES)
        self.entry_dest.dnd_bind('<<Drop>>', self.drop_dest)
        self.btn_browse_dest = ctk.CTkButton(self.frame_dest, text="...", width=50, command=self.browse_dest)
        self.btn_browse_dest.pack(side="right", padx=10)

        self.frame_speed = ctk.CTkFrame(self)
        self.frame_speed.pack(pady=10, padx=20, fill="x")
        self.lbl_speed_title = ctk.CTkLabel(self.frame_speed, text="Speed:", font=("Arial", 12, "bold"))
        self.lbl_speed_title.pack(pady=(5,0))
        
        self.seg_speed = ctk.CTkSegmentedButton(self.frame_speed, values=["1", "2", "3"]) 
        self.seg_speed.pack(pady=5, padx=10, fill="x")
        
        self.lbl_speed_info = ctk.CTkLabel(self.frame_speed, text="...", font=("Arial", 10), text_color="gray")
        self.lbl_speed_info.pack(pady=(0, 5))

        self.frame_opts = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_opts.pack(pady=5, padx=20, fill="x")
        self.check_shutdown = ctk.CTkCheckBox(self.frame_opts, text="...", fg_color="#FF4444", hover_color="#8B0000")
        self.check_shutdown.pack(anchor="w", pady=2)

        self.textbox_log = ctk.CTkTextbox(self, height=150)
        self.textbox_log.pack(pady=10, padx=20, fill="both")
        self.btn_start = ctk.CTkButton(self, text="...", fg_color="green", height=45, font=("Arial", 14, "bold"), command=self.initiate_copy_sequence)
        self.btn_start.pack(pady=10, padx=20, fill="x")

    def clean_path(self, path):
        if path.startswith('{') and path.endswith('}'): return path[1:-1]
        return path
    def drop_source(self, event): self.entry_source.delete(0, "end"); self.entry_source.insert(0, self.clean_path(event.data))
    def drop_dest(self, event): self.entry_dest.delete(0, "end"); self.entry_dest.insert(0, self.clean_path(event.data))
    def browse_source(self): 
        p=filedialog.askdirectory()
        if p: self.entry_source.delete(0, "end"); self.entry_source.insert(0, p)
    def browse_dest(self): 
        p=filedialog.askdirectory()
        if p: self.entry_dest.delete(0, "end"); self.entry_dest.insert(0, p)
    def log(self, msg): self.textbox_log.insert("end", msg+"\n"); self.textbox_log.see("end")
    def show_notification(self, t, m): 
        try: notification.notify(title=t, message=m, app_name="TurboCopy", timeout=5) 
        except: pass

    def on_closing(self):
        if self.current_process:
            try: subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.current_process.pid)], creationflags=subprocess.CREATE_NO_WINDOW)
            except: pass
        self.destroy()
        sys.exit()

    def ask_destination_and_start(self):
        self.attributes('-topmost', True)
        dest = filedialog.askdirectory()
        self.attributes('-topmost', False)
        if dest: self.entry_dest.insert(0, dest); self.initiate_copy_sequence()

    def initiate_copy_sequence(self):
        L = LANGUAGES[self.current_lang]
        s, d = self.entry_source.get(), self.entry_dest.get()
        if not s or not d: self.log(L["err_empty"]); return
        
        dialog = ConflictDialog(self, self.current_lang)
        self.wait_window(dialog)
        
        if dialog.choice: self.start_copy_thread(dialog.choice)
        else: self.log(L["cancel"])

    def run_robocopy(self, mode):
        L = LANGUAGES[self.current_lang]
        s, d = self.entry_source.get(), self.entry_dest.get()
        
        selected_speed_text = self.seg_speed.get()
        try:
            speed_index = L["speeds"].index(selected_speed_text)
        except:
            speed_index = 1
        
        cmd = ["robocopy", s, d, "/E", "/R:1", "/W:1"]
        
        if speed_index == 2:
            cmd.append("/MT:32")
        elif speed_index == 1:
            cmd.append("/MT:8")
        else:
            cmd.append("/IPG:5") 

        if mode == "OVERWRITE": cmd.append("/IS") 
        elif mode == "SKIP": cmd.extend(["/XC", "/XN", "/XO"])
        elif mode == "UPDATE": cmd.append("/XO")
        
        self.log(f"Running... Mode: {mode} | Speed: {selected_speed_text}")
        self.log("-" * 40)
        
        self.current_process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True, 
            encoding="cp857",
            errors="replace",
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        for line in self.current_process.stdout: 
            self.log(line.strip())
        
        self.current_process.wait()
        self.current_process = None
        
        self.log("-" * 40); self.log(L["done_msg"])
        self.show_notification(L["title"], L["done_msg"])
        self.btn_start.configure(state="normal")
        if self.check_shutdown.get(): os.system("shutdown /s /t 60")

    def start_copy_thread(self, mode):
        self.btn_start.configure(state="disabled")
        threading.Thread(target=self.run_robocopy, args=(mode,), daemon=True).start()

if __name__ == "__main__":
    app = TurboCopyApp()
    app.mainloop()