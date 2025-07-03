#!/usr/bin/env python3
"""
最小化測試版本，不使用cnlunar
"""

import tkinter as tk
from tkinter import font
import datetime
import sys
import os

print("🚀 最小化測試開始", flush=True)

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.join(os.path.dirname(sys.executable), '..', 'Resources')
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    full_path = os.path.join(base_path, relative_path)
    print(f"🔍 resource_path({relative_path}) -> {full_path}", flush=True)
    return full_path

class MinimalClock:
    def __init__(self):
        print("🐛 開始初始化MinimalClock", flush=True)
        
        self.root = tk.Tk()
        print("�� Tkinter根窗口創建完成", flush=True)
        
        self.root.title("最小化時鐘測試")
        self.root.geometry("400x200")
        self.root.configure(bg='#f0f0f0')
        
        print("🐛 設置字體", flush=True)
        self.setup_fonts()
        
        print("🐛 創建UI", flush=True)
        self.create_ui()
        
        print("🐛 啟動時鐘更新", flush=True)
        self.update_time()
        
        print("🐛 初始化完成，準備顯示窗口", flush=True)
        self.root.deiconify()  # 確保窗口顯示
        
    def setup_fonts(self):
        try:
            font_path = resource_path("assets/Antonio-Regular.ttf")
            if os.path.exists(font_path):
                # 只是測試，不實際載入
                print(f"✅ 字體文件存在: {font_path}", flush=True)
            else:
                print(f"❌ 字體文件不存在: {font_path}", flush=True)
        except Exception as e:
            print(f"❌ 字體設置錯誤: {e}", flush=True)
    
    def create_ui(self):
        # 創建時間標籤
        self.time_label = tk.Label(
            self.root,
            text="--:--:--",
            font=("Arial", 24, "bold"),
            bg='#f0f0f0',
            fg='black'
        )
        self.time_label.pack(expand=True, pady=20)
        
        # 創建狀態標籤
        self.status_label = tk.Label(
            self.root,
            text="最小化測試運行中",
            font=("Arial", 12),
            bg='#f0f0f0',
            fg='gray'
        )
        self.status_label.pack(pady=10)
        
        print("🐛 UI元件創建完成", flush=True)
    
    def update_time(self):
        try:
            now = datetime.datetime.now()
            time_str = now.strftime("%H:%M:%S")
            self.time_label.config(text=time_str)
            print(f"🔄 時間更新: {time_str}", flush=True)
        except Exception as e:
            print(f"❌ 時間更新錯誤: {e}", flush=True)
        
        # 每秒更新一次
        self.root.after(1000, self.update_time)
    
    def run(self):
        print("🎯 開始主循環", flush=True)
        self.root.mainloop()
        print("🏁 主循環結束", flush=True)

if __name__ == "__main__":
    print("=== 最小化測試開始 ===", flush=True)
    try:
        clock = MinimalClock()
        clock.run()
    except Exception as e:
        print(f"❌ 測試失敗: {e}", flush=True)
        import traceback
        traceback.print_exc()
    print("=== 最小化測試結束 ===", flush=True)
