#!/usr/bin/env python3
"""
強制顯示版本，專門解決App空白問題
"""

import tkinter as tk
from tkinter import font
import datetime
import sys
import os

print("🚀 強制顯示版本啟動", flush=True)

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.join(os.path.dirname(sys.executable), '..', 'Resources')
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    return os.path.join(base_path, relative_path)

class ForceShowClock:
    def __init__(self):
        print("🔧 創建強制顯示時鐘", flush=True)
        
        # 創建主窗口
        self.root = tk.Tk()
        print("✅ 根窗口創建完成", flush=True)
        
        # 強制設置窗口屬性
        self.root.title("🦈 EVOI時鐘 - 強制顯示版")
        self.root.geometry("400x300+100+100")  # 指定位置
        self.root.configure(bg='#ffffff')  # 白色背景
        
        # 強制置頂和顯示
        self.root.attributes('-topmost', True)  # 置頂
        self.root.lift()  # 提升到最前面
        self.root.focus_force()  # 強制獲得焦點
        
        print("🔧 窗口屬性設置完成", flush=True)
        
        # 立即顯示窗口
        self.root.deiconify()
        self.root.update_idletasks()
        self.root.update()
        
        print("🔧 窗口強制顯示完成", flush=True)
        
        # 創建大號標籤測試
        self.create_test_ui()
        
        # 啟動時間更新
        self.update_time()
        
        print("🔧 初始化完成", flush=True)
    
    def create_test_ui(self):
        print("🎨 創建測試UI", flush=True)
        
        # 大標題
        title_label = tk.Label(
            self.root,
            text="🦈 EVOI時鐘測試",
            font=("Arial", 20, "bold"),
            bg='#ffffff',
            fg='#0066cc',
            pady=20
        )
        title_label.pack()
        
        # 時間顯示
        self.time_label = tk.Label(
            self.root,
            text="--:--:--",
            font=("Arial", 24, "bold"),
            bg='#ffffff',
            fg='#000000',
            pady=10
        )
        self.time_label.pack()
        
        # 狀態標籤
        self.status_label = tk.Label(
            self.root,
            text="如果您看到這個文字，代表App顯示正常！",
            font=("Arial", 12),
            bg='#ffffff',
            fg='#00aa00',
            pady=10
        )
        self.status_label.pack()
        
        # 測試按鈕
        test_button = tk.Button(
            self.root,
            text="點擊測試",
            font=("Arial", 14),
            command=self.on_test_click,
            bg='#4CAF50',
            fg='white',
            pady=5
        )
        test_button.pack(pady=20)
        
        print("✅ UI元件創建完成", flush=True)
    
    def on_test_click(self):
        print("🖱️ 按鈕被點擊！", flush=True)
        self.status_label.config(text="按鈕點擊成功！App功能正常！", fg='#ff6600')
    
    def update_time(self):
        try:
            now = datetime.datetime.now()
            time_str = now.strftime("%H:%M:%S")
            self.time_label.config(text=time_str)
            
            # 每次更新都輸出到控制台
            if now.second % 5 == 0:  # 每5秒輸出一次
                print(f"⏰ 時間更新: {time_str}", flush=True)
                
        except Exception as e:
            print(f"❌ 時間更新錯誤: {e}", flush=True)
        
        # 每秒更新
        self.root.after(1000, self.update_time)
    
    def run(self):
        print("🎯 開始主循環", flush=True)
        
        # 再次確保窗口顯示
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"❌ 主循環錯誤: {e}", flush=True)
        
        print("🏁 主循環結束", flush=True)

if __name__ == "__main__":
    print("=== 強制顯示測試開始 ===", flush=True)
    
    try:
        clock = ForceShowClock()
        clock.run()
    except Exception as e:
        print(f"❌ 測試失敗: {e}", flush=True)
        import traceback
        traceback.print_exc()
    
    print("=== 強制顯示測試結束 ===", flush=True)
