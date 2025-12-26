import os
import sys
import shutil
import winreg
import ctypes
import subprocess
from tkinter import messagebox, Tk

log_file = os.path.join(os.getenv('TEMP'), 'turbocopy_install_log.txt')
sys.stdout = open(log_file, 'w')
sys.stderr = open(log_file, 'w')

def log(msg):
    try:
        print(msg)
        sys.stdout.flush()
    except:
        pass

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def make_shortcut_vbs(target_exe, shortcut_path, description):
    vbs_content = f"""
    Set oWS = WScript.CreateObject("WScript.Shell")
    sLinkFile = "{shortcut_path}"
    Set oLink = oWS.CreateShortcut(sLinkFile)
    oLink.TargetPath = "{target_exe}"
    oLink.WorkingDirectory = "{os.path.dirname(target_exe)}"
    oLink.Description = "{description}"
    oLink.IconLocation = "{target_exe}"
    oLink.Save
    """
    
    vbs_path = os.path.join(os.getenv('TEMP'), "create_shortcut.vbs")
    try:
        with open(vbs_path, "w") as file:
            file.write(vbs_content)
        
        subprocess.call(['cscript', '//Nologo', vbs_path], shell=True)
        os.remove(vbs_path)
        return True
    except Exception as e:
        log(f"Shortcut creation error: {e}")
        return False

def install():
    root = Tk()
    root.withdraw()

    if not is_admin():
        messagebox.showerror("Permission Denied", "Administrator privileges required.\nPlease RIGHT-CLICK the installer and select 'Run as Administrator'.")
        return

    log("Installation started...")

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    source_exe = os.path.join(base_path, "turbocopy.exe")
    
    if not os.path.exists(source_exe):
        local_source = os.path.join(os.path.dirname(sys.argv[0]), "turbocopy.exe")
        if os.path.exists(local_source):
            source_exe = local_source
        else:
            messagebox.showerror("Error", "turbocopy.exe not found!\nThe setup package might be corrupted.")
            return

    program_files = os.environ.get("ProgramFiles")
    install_dir = os.path.join(program_files, "TurboCopy")
    target_exe = os.path.join(install_dir, "turbocopy.exe")

    try:
        if not os.path.exists(install_dir):
            os.makedirs(install_dir)
        shutil.copy2(source_exe, target_exe)
        log(f"File copied to: {target_exe}")
    except Exception as e:
        messagebox.showerror("Installation Error", f"Failed to copy files.\nError: {e}")
        return

    try:
        try: winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\TurboCopy\command")
        except: pass
        try: winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\TurboCopy")
        except: pass

        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\TurboCopy")
        winreg.SetValue(key, "", winreg.REG_SZ, "Copy with TurboCopy")
        winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, target_exe)
        winreg.CloseKey(key)

        cmd_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\TurboCopy\command")
        winreg.SetValue(cmd_key, "", winreg.REG_SZ, f'"{target_exe}" "%1"')
        winreg.CloseKey(cmd_key)
        log("Registry updated successfully.")
    except Exception as e:
        messagebox.showerror("Registry Error", f"Failed to add context menu item.\nError: {e}")

    try:
        desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        shortcut_path = os.path.join(desktop_path, "TurboCopy.lnk")
        make_shortcut_vbs(target_exe, shortcut_path, "High Performance File Copier")
        log("Shortcut created.")
    except Exception as e:
        log(f"Failed to create shortcut: {e}")

    messagebox.showinfo("Success", "Installation Complete!\n\n1. Shortcut added to Desktop.\n2. Added to Right-Click Context Menu.")

if __name__ == "__main__":
    install()