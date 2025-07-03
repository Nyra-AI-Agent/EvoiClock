#!/usr/bin/env python3
"""
無 GUI 字體管理器 - 專為容器化和生產環境設計
不依賴 Tkinter 或任何 GUI 庫
"""

import os
import sys
import platform
import subprocess
import tempfile
import shutil

class HeadlessFontManager:
    """無 GUI 字體管理器"""
    
    def __init__(self):
        self.system = platform.system()
        self.font_paths = self._get_font_paths()
        self.antonio_fonts = {}
        
    def _get_font_paths(self):
        """獲取系統字體路徑"""
        paths = []
        
        if self.system == "Linux":
            paths = [
                '/usr/share/fonts/',
                '/usr/local/share/fonts/',
                '/home/.fonts/',
                '/root/.fonts/'
            ]
        elif self.system == "Windows":
            paths = [
                'C:/Windows/Fonts/',
                os.path.expanduser('~/AppData/Local/Microsoft/Windows/Fonts/')
            ]
        elif self.system == "Darwin":
            paths = [
                '/System/Library/Fonts/',
                '/Library/Fonts/',
                os.path.expanduser('~/Library/Fonts/')
            ]
        
        return [p for p in paths if os.path.exists(p)]
    
    def resource_path(self, relative_path):
        """獲取資源絕對路徑"""
        if getattr(sys, 'frozen', False):
            if hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.join(os.path.dirname(sys.executable), '..', 'Resources')
        else:
            base_path = os.getcwd()
        return os.path.join(base_path, relative_path)
    
    def install_antonio_fonts(self):
        """安裝 Antonio 字體到系統"""
        print(f"🔧 在 {self.system} 上安裝 Antonio 字體...")
        
        font_files = [
            'assets/Antonio-Light.ttf',
            'assets/Antonio-Regular.ttf',
            'assets/Antonio-Bold.ttf'
        ]
        
        installed_count = 0
        
        for font_file in font_files:
            source_path = self.resource_path(font_file)
            if not os.path.exists(source_path):
                print(f"  ❌ 源文件不存在: {source_path}")
                continue
                
            if self._install_single_font(source_path, os.path.basename(font_file)):
                installed_count += 1
                self.antonio_fonts[os.path.basename(font_file)] = source_path
        
        print(f"✅ 成功安裝 {installed_count}/3 個 Antonio 字體")
        return installed_count > 0
    
    def _install_single_font(self, source_path, font_name):
        """安裝單個字體文件"""
        try:
            if self.system == "Linux":
                return self._install_font_linux(source_path, font_name)
            elif self.system == "Windows":
                return self._install_font_windows(source_path, font_name)
            elif self.system == "Darwin":
                return self._install_font_macos(source_path, font_name)
            else:
                print(f"  ⚠️  不支援的系統: {self.system}")
                return False
        except Exception as e:
            print(f"  ❌ 安裝 {font_name} 失敗: {e}")
            return False
    
    def _install_font_linux(self, source_path, font_name):
        """Linux 字體安裝"""
        # 優先使用用戶字體目錄
        user_fonts_dir = '/root/.fonts'
        if not os.path.exists(user_fonts_dir):
            os.makedirs(user_fonts_dir, exist_ok=True)
        
        dest_path = os.path.join(user_fonts_dir, font_name)
        shutil.copy2(source_path, dest_path)
        
        # 更新字體快取
        try:
            subprocess.run(['fc-cache', '-fv'], capture_output=True, check=True)
            print(f"  ✅ {font_name} 安裝到 {dest_path}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            # 即使 fc-cache 失敗，字體文件也已複製
            print(f"  ⚠️  {font_name} 複製成功，但無法更新字體快取")
            return True
    
    def _install_font_windows(self, source_path, font_name):
        """Windows 字體安裝"""
        fonts_dir = os.path.expanduser('~/AppData/Local/Microsoft/Windows/Fonts/')
        os.makedirs(fonts_dir, exist_ok=True)
        
        dest_path = os.path.join(fonts_dir, font_name)
        shutil.copy2(source_path, dest_path)
        print(f"  ✅ {font_name} 安裝到 {dest_path}")
        return True
    
    def _install_font_macos(self, source_path, font_name):
        """macOS 字體安裝"""
        user_fonts_dir = os.path.expanduser('~/Library/Fonts/')
        os.makedirs(user_fonts_dir, exist_ok=True)
        
        dest_path = os.path.join(user_fonts_dir, font_name)
        shutil.copy2(source_path, dest_path)
        print(f"  ✅ {font_name} 安裝到 {dest_path}")
        return True
    
    def get_available_fonts(self):
        """獲取可用字體清單（無 GUI 版本）"""
        fonts = {
            'primary': self._get_primary_font(),
            'mono': 'Antonio' if self.antonio_fonts else self._get_fallback_mono_font()
        }
        return fonts
    
    def _get_primary_font(self):
        """獲取主要字體"""
        if self.system == "Darwin":
            return 'SF Pro Display'
        elif self.system == "Windows":
            return 'Segoe UI'
        else:
            return 'DejaVu Sans'  # Linux 預設
    
    def _get_fallback_mono_font(self):
        """獲取回退等寬字體"""
        if self.system == "Darwin":
            return 'Menlo'
        elif self.system == "Windows":
            return 'Consolas'
        else:
            return 'DejaVu Sans Mono'  # Linux 預設
    
    def test_fonts(self):
        """測試字體系統"""
        print("\n📋 字體系統測試報告:")
        print(f"  🖥️  系統: {self.system}")
        print(f"  📁 字體路徑: {self.font_paths}")
        
        # 測試 Antonio 字體
        if self.install_antonio_fonts():
            fonts = self.get_available_fonts()
            print(f"  ✅ 主要字體: {fonts['primary']}")
            print(f"  ✅ 等寬字體: {fonts['mono']}")
            print(f"  📊 Antonio 字體: {len(self.antonio_fonts)} 個已安裝")
            return True
        else:
            print("  ❌ Antonio 字體安裝失敗")
            return False

def main():
    """主程式"""
    print("🔤 EvoiClock 無 GUI 字體管理器測試")
    print("=" * 50)
    
    fm = HeadlessFontManager()
    success = fm.test_fonts()
    
    if success:
        print("\n🎉 字體系統在容器環境中正常工作！")
        return 0
    else:
        print("\n❌ 字體系統需要調整")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 