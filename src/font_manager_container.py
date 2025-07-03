import os
import sys
import platform
import ctypes
import ctypes.util
import tkinter as tk
from tkinter import font
import shutil
import tempfile

def resource_path(relative_path):
    """獲取資源絕對路徑，支援開發環境、打包環境和容器環境"""
    if getattr(sys, 'frozen', False):
        # 打包環境 (PyInstaller/py2app)
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.join(os.path.dirname(sys.executable), '..', 'Resources')
    else:
        # 開發環境和容器環境
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(script_dir, '..')

    return os.path.join(base_path, relative_path)

def load_font_for_linux(font_path):
    """為Linux容器註冊字體 (使用fontconfig)"""
    if not os.path.exists(font_path):
        print(f"字體文件不存在: {font_path}")
        return False
    
    try:
        # 方法1: 複製到系統字體目錄
        system_font_dir = "/usr/share/fonts/truetype/"
        user_font_dir = os.path.expanduser("~/.fonts/")
        
        # 嘗試用戶目錄 (更安全)
        target_dir = user_font_dir
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
        
        font_name = os.path.basename(font_path)
        target_path = os.path.join(target_dir, font_name)
        
        if not os.path.exists(target_path):
            shutil.copy2(font_path, target_path)
            print(f"✅ 已複製字體到: {target_path}")
        
        # 更新字體緩存
        os.system("fc-cache -fv")
        print(f"✅ 已更新字體緩存: {font_name}")
        return True
        
    except Exception as e:
        print(f"❌ Linux字體註冊失敗: {e}")
        return False

def load_font_for_macos(font_path):
    """為macOS註冊字體 (原有邏輯)"""
    if not os.path.exists(font_path):
        print(f"字體文件不存在: {font_path}")
        return False

    core_text_path = ctypes.util.find_library('CoreText')
    if not core_text_path:
        print("CoreText框架未找到")
        return False
    
    try:
        CoreText = ctypes.CDLL(core_text_path)
        
        CFURLCreateFromFileSystemRepresentation = CoreText.CFURLCreateFromFileSystemRepresentation
        CFURLCreateFromFileSystemRepresentation.restype = ctypes.c_void_p
        CFURLCreateFromFileSystemRepresentation.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_long, ctypes.c_bool]

        CTFontManagerRegisterFontsForURL = CoreText.CTFontManagerRegisterFontsForURL
        CTFontManagerRegisterFontsForURL.restype = ctypes.c_bool
        CTFontManagerRegisterFontsForURL.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p]

        font_path_bytes = font_path.encode('utf-8')
        font_url = CFURLCreateFromFileSystemRepresentation(None, font_path_bytes, len(font_path_bytes), False)

        if not font_url:
            print("創建CFURL失敗")
            return False

        if CTFontManagerRegisterFontsForURL(font_url, 1, None):
            print(f"✅ macOS字體註冊成功: {os.path.basename(font_path)}")
            return True
        else:
            print("❌ macOS字體註冊失敗")
            return False
            
    except Exception as e:
        print(f"❌ macOS字體註冊異常: {e}")
        return False

def load_font_for_windows(font_path):
    """為Windows註冊字體"""
    if not os.path.exists(font_path):
        print(f"字體文件不存在: {font_path}")
        return False
    
    try:
        import winreg
        from ctypes import wintypes
        
        # 註冊字體到註冊表
        gdi32 = ctypes.windll.gdi32
        if gdi32.AddFontResourceW(font_path):
            print(f"✅ Windows字體註冊成功: {os.path.basename(font_path)}")
            
            # 通知系統更新字體
            user32 = ctypes.windll.user32
            user32.SendMessageW(0xFFFF, 0x001D, 0, 0)  # WM_FONTCHANGE
            return True
        else:
            print("❌ Windows字體註冊失敗")
            return False
            
    except Exception as e:
        print(f"❌ Windows字體註冊異常: {e}")
        return False

class ContainerFontManager:
    """支援容器化的字體管理器"""
    
    def __init__(self):
        self.system = platform.system()
        self.fonts_loaded = False
        self._setup_fonts()
        self.fonts = self._load_fonts()
        
    def _setup_fonts(self):
        """根據平台設置字體"""
        antonio_regular = resource_path("assets/Antonio-Regular.ttf")
        
        if self.system == "Darwin":
            self.fonts_loaded = load_font_for_macos(antonio_regular)
        elif self.system == "Linux":
            self.fonts_loaded = load_font_for_linux(antonio_regular)
        elif self.system == "Windows":
            self.fonts_loaded = load_font_for_windows(antonio_regular)
        else:
            print(f"⚠️  未知平台: {self.system}")
            self.fonts_loaded = False

    def _load_fonts(self):
        """根據平台和字體載入狀態選擇字體"""
        
        # 如果Antonio字體載入成功，所有平台都用Antonio
        if self.fonts_loaded:
            return {
                'primary': 'Antonio',  # 統一使用Antonio
                'mono': 'Antonio'
            }
        
        # 字體載入失敗時的回退方案
        if self.system == "Darwin":
            return {'primary': 'SF Pro Display', 'mono': 'Monaco'}
        elif self.system == "Windows":
            return {'primary': 'Segoe UI', 'mono': 'Consolas'}
        elif self.system == "Linux":
            return {'primary': 'DejaVu Sans', 'mono': 'DejaVu Sans Mono'}
        else:
            return {'primary': 'TkDefaultFont', 'mono': 'TkFixedFont'}
    
    def get_font(self, font_type, size, **kwargs):
        """獲取字體對象，帶容錯機制"""
        family = self.fonts.get(font_type, 'TkDefaultFont')
        
        try:
            # 首選字體
            return font.Font(family=family, size=size, **kwargs)
        except tk.TclError as e:
            print(f"⚠️  字體 '{family}' 不可用: {e}")
            
            # 回退到系統默認字體
            try:
                fallback_family = 'TkFixedFont' if font_type == 'mono' else 'TkDefaultFont'
                return font.Font(family=fallback_family, size=size, **kwargs)
            except tk.TclError:
                # 最後回退
                return font.Font(size=size, **kwargs)
    
    def test_fonts(self):
        """測試字體可用性"""
        print("\n🔍 字體測試報告:")
        print(f"平台: {self.system}")
        print(f"Antonio字體載入: {'✅ 成功' if self.fonts_loaded else '❌ 失敗'}")
        
        for font_type, family in self.fonts.items():
            try:
                test_font = font.Font(family=family, size=12)
                actual_family = test_font.actual('family')
                print(f"{font_type}: {family} → {actual_family}")
            except tk.TclError as e:
                print(f"{font_type}: {family} → ❌ 不可用 ({e})")

# 測試函數
def test_container_fonts():
    """測試容器字體系統"""
    import tkinter as tk
    
    root = tk.Tk()
    root.withdraw()
    
    font_manager = ContainerFontManager()
    font_manager.test_fonts()
    
    # 創建測試窗口
    test_window = tk.Toplevel(root)
    test_window.title("字體測試")
    test_window.geometry("400x200")
    
    # 測試主要字體
    primary_font = font_manager.get_font('primary', 16)
    primary_label = tk.Label(test_window, text="主要字體測試 (Primary Font)", font=primary_font)
    primary_label.pack(pady=10)
    
    # 測試等寬字體  
    mono_font = font_manager.get_font('mono', 24, weight='bold')
    mono_label = tk.Label(test_window, text="12:34:56", font=mono_font)
    mono_label.pack(pady=10)
    
    # 顯示字體信息
    info_text = f"平台: {font_manager.system}\nAntonio載入: {font_manager.fonts_loaded}"
    info_label = tk.Label(test_window, text=info_text)
    info_label.pack(pady=10)
    
    test_window.deiconify()
    root.mainloop()

if __name__ == "__main__":
    test_container_fonts() 