import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
import subprocess
import threading
import sys
import os
from tkinter import filedialog
from plyer import notification

# --- Arayüz Ayarları ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- DnD Wrapper (Sürükle Bırak için) ---
class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

# --- Tooltip (İpucu Baloncuğu) Sınıfı ---
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

# --- Özel Soru Penceresi (Çakışma Yönetimi) ---
class ConflictDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Çakışma Ayarı")
        self.geometry("450x380")
        self.resizable(False, False)
        self.choice = None 
        self.transient(parent)
        self.grab_set() 
        self.attributes('-topmost', True)

        ctk.CTkLabel(self, text="Hedefte aynı isimde dosya varsa\nne yapılsın?", font=("Arial", 16, "bold")).pack(pady=20)

        # Buton 1: Üzerine Yaz
        btn1 = ctk.CTkButton(self, text="1. Üzerine Yaz", fg_color="#C0392B", hover_color="#922B21", height=40,
                             command=lambda: self.set_choice("OVERWRITE"))
        btn1.pack(pady=10, padx=40, fill="x")
        CTkToolTip(btn1, "DİKKAT! Hedefteki dosya ile kaynak aynı olsa bile hedefi ezer. En garanti ama yavaş yöntemdir.")

        # Buton 2: Atla
        btn2 = ctk.CTkButton(self, text="2. Atla (Pas Geç)", fg_color="#F39C12", hover_color="#B9770E", height=40,
                             command=lambda: self.set_choice("SKIP"))
        btn2.pack(pady=10, padx=40, fill="x")
        CTkToolTip(btn2, "Hedefte dosya varsa (eski/yeni fark etmez) dokunmaz. En hızlı yöntemdir.")

        # Buton 3: Akıllı Güncelleme
        btn3 = ctk.CTkButton(self, text="3. Akıllı Güncelleme", fg_color="#27AE60", hover_color="#1E8449", height=40,
                             command=lambda: self.set_choice("UPDATE"))
        btn3.pack(pady=10, padx=40, fill="x")
        CTkToolTip(btn3, "ÖNERİLEN! Sadece kaynak dosya daha YENİ ise kopyalar. Eski dosyalara dokunmaz.")
        
        ctk.CTkLabel(self, text="*Detay görmek için fareyi butonların üzerinde tutun.", font=("Arial", 11), text_color="gray").pack(pady=20)

    def set_choice(self, choice):
        self.choice = choice
        self.destroy()

# --- Ana Uygulama ---
class TurboCopyApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("TurboCopy Safe")
        self.geometry("600x600")
        self.resizable(False, False)
        self.auto_start_mode = False
        self.initial_source = ""
        
        if len(sys.argv) > 1:
            self.initial_source = sys.argv[1]
            self.auto_start_mode = True

        self.create_widgets()
        if self.auto_start_mode:
            self.after(500, self.ask_destination_and_start)

    def create_widgets(self):
        ctk.CTkLabel(self, text="TurboCopy", font=("Arial", 24, "bold")).pack(pady=15)
        ctk.CTkLabel(self, text="(Klasörleri kutucuklara sürükleyebilirsiniz)", font=("Arial", 11), text_color="gray").pack(pady=(0,10))

        # Kaynak
        self.frame_source = ctk.CTkFrame(self)
        self.frame_source.pack(pady=5, padx=20, fill="x")
        ctk.CTkLabel(self.frame_source, text="Kaynak:", width=60).pack(side="left", padx=5)
        self.entry_source = ctk.CTkEntry(self.frame_source, placeholder_text="Kaynak Klasör")
        self.entry_source.pack(side="left", fill="x", expand=True, padx=5, pady=10)
        self.entry_source.drop_target_register(DND_FILES)
        self.entry_source.dnd_bind('<<Drop>>', self.drop_source)
        if self.initial_source: self.entry_source.insert(0, self.initial_source)
        ctk.CTkButton(self.frame_source, text="Seç", width=50, command=self.browse_source).pack(side="right", padx=10)

        # Hedef
        self.frame_dest = ctk.CTkFrame(self)
        self.frame_dest.pack(pady=5, padx=20, fill="x")
        ctk.CTkLabel(self.frame_dest, text="Hedef:", width=60).pack(side="left", padx=5)
        self.entry_dest = ctk.CTkEntry(self.frame_dest, placeholder_text="Hedef Klasör")
        self.entry_dest.pack(side="left", fill="x", expand=True, padx=5, pady=10)
        self.entry_dest.drop_target_register(DND_FILES)
        self.entry_dest.dnd_bind('<<Drop>>', self.drop_dest)
        ctk.CTkButton(self.frame_dest, text="Seç", width=50, command=self.browse_dest).pack(side="right", padx=10)

        # Ayarlar
        self.frame_opts = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_opts.pack(pady=5, padx=20, fill="x")
        
        self.check_shutdown = ctk.CTkCheckBox(self.frame_opts, text="İşlem bitince bilgisayarı kapat", fg_color="#FF4444", hover_color="#8B0000")
        self.check_shutdown.pack(anchor="w", pady=2)

        # Log ve Başlat
        self.textbox_log = ctk.CTkTextbox(self, height=180)
        self.textbox_log.pack(pady=10, padx=20, fill="both")
        self.btn_start = ctk.CTkButton(self, text="KOPYALAMAYI BAŞLAT", fg_color="green", height=45, font=("Arial", 14, "bold"), command=self.initiate_copy_sequence)
        self.btn_start.pack(pady=10, padx=20, fill="x")

    def clean_path(self, path):
        if path.startswith('{') and path.endswith('}'): return path[1:-1]
        return path

    def drop_source(self, event): 
        self.entry_source.delete(0, "end")
        self.entry_source.insert(0, self.clean_path(event.data))

    def drop_dest(self, event): 
        self.entry_dest.delete(0, "end")
        self.entry_dest.insert(0, self.clean_path(event.data))

    def browse_source(self): 
        p = filedialog.askdirectory()
        if p: 
            self.entry_source.delete(0, "end")
            self.entry_source.insert(0, p)

    def browse_dest(self): 
        p = filedialog.askdirectory()
        if p: 
            self.entry_dest.delete(0, "end")
            self.entry_dest.insert(0, p)

    def log(self, msg): 
        self.textbox_log.insert("end", msg+"\n")
        self.textbox_log.see("end")

    def show_notification(self, t, m): 
        try: notification.notify(title=t, message=m, app_name="TurboCopy", timeout=5) 
        except: pass

    def ask_destination_and_start(self):
        self.attributes('-topmost', True)
        dest = filedialog.askdirectory(title="Hedef Klasör Seç")
        self.attributes('-topmost', False)
        if dest: 
            self.entry_dest.insert(0, dest)
            self.initiate_copy_sequence()

    def initiate_copy_sequence(self):
        s, d = self.entry_source.get(), self.entry_dest.get()
        if not s or not d: 
            self.log("HATA: Kaynak/Hedef boş.")
            return
        
        dialog = ConflictDialog(self)
        self.wait_window(dialog)
        
        if dialog.choice: 
            self.start_copy_thread(dialog.choice)
        else: 
            self.log("İptal edildi.")

    def run_robocopy(self, mode):
        s, d = self.entry_source.get(), self.entry_dest.get()
        cmd = ["robocopy", s, d, "/E", "/MT:32", "/R:1", "/W:1"]
        
        if mode == "OVERWRITE": cmd.append("/IS") 
        elif mode == "SKIP": cmd.extend(["/XC", "/XN", "/XO"])
        elif mode == "UPDATE": cmd.append("/XO")
        
        self.log(f"Başlıyor... Mod: {mode}")
        self.log("-" * 40)
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="cp857", errors="replace", creationflags=subprocess.CREATE_NO_WINDOW)
        for line in process.stdout: 
            self.log(line.strip())
        process.wait()
        
        self.log("-" * 40)
        self.log("BİTTİ.")
        self.show_notification("TurboCopy", "Kopyalama Tamamlandı")
        self.btn_start.configure(state="normal")
        
        if self.check_shutdown.get(): 
            os.system("shutdown /s /t 60")

    def start_copy_thread(self, mode):
        self.btn_start.configure(state="disabled")
        threading.Thread(target=self.run_robocopy, args=(mode,), daemon=True).start()

if __name__ == "__main__":
    app = TurboCopyApp()
    app.mainloop()