import os
import sys
import json
import shutil
import subprocess
from datetime import datetime

class Builder:
    def __init__(self):
        self.config = self.load_config()
        self.version = self.config['project']['version']
        self.build_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def load_config(self):
        """載入 MCP 配置"""
        with open('mcp_config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def create_directories(self):
        """創建必要的目錄"""
        dirs = ['dist', 'build', 'logs']
        for d in dirs:
            if not os.path.exists(d):
                os.makedirs(d)
    
    def install_dependencies(self):
        """安裝依賴"""
        print("安裝依賴...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    def run_tests(self):
        """運行測試"""
        print("運行測試...")
        # 這裡可以添加測試代碼
        pass
    
    def build_exe(self):
        """打包應用程序"""
        print("開始打包...")
        
        # 打包命令
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            f"--icon={self.config['build']['icon']}",
            "--add-data", "assets;assets",
            "--name", f"EVOI_Trading_Clock_v{self.version}",
            "main.py"
        ]
        
        # 執行打包
        subprocess.run(cmd)
    
    def copy_files(self):
        """複製必要文件"""
        print("複製文件...")
        # 複製配置文件
        shutil.copy("config.json", f"dist/config.json")
        # 複製圖標
        if os.path.exists("assets/icon.ico"):
            shutil.copy("assets/icon.ico", "dist/icon.ico")
    
    def create_installer(self):
        """創建安裝程序"""
        print("創建安裝程序...")
        # 這裡可以添加創建安裝程序的代碼
        pass
    
    def cleanup(self):
        """清理臨時文件"""
        print("清理臨時文件...")
        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists("__pycache__"):
            shutil.rmtree("__pycache__")
    
    def build(self):
        """執行完整的構建流程"""
        try:
            print(f"開始構建 EVOI Trading Clock v{self.version}")
            print(f"構建時間: {self.build_time}")
            
            self.create_directories()
            self.install_dependencies()
            self.run_tests()
            self.build_exe()
            self.copy_files()
            self.create_installer()
            self.cleanup()
            
            print("\n構建完成！")
            print(f"輸出目錄: {os.path.abspath('dist')}")
            
        except Exception as e:
            print(f"構建過程中發生錯誤: {e}")
            sys.exit(1)

if __name__ == "__main__":
    builder = Builder()
    builder.build() 