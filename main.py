#!/usr/bin/env python3
"""
EVOI Trading Clock - 主程式入口
整合現有組件：clock_widget, time_logic, trading_panel
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """檢查必要的組件檔案"""
    required_files = [
        'clock_widget.py',
        'time_logic.py', 
        'trading_panel.py',
        'config_manager.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"⚠️  缺少組件檔案: {', '.join(missing_files)}")
        return False
    
    return True

def main():
    """主函數 - 啟動 EVOI Trading Clock"""
    print("🚀 啟動 EVOI Trading Clock")
    print("=" * 30)
    
    # 檢查組件
    if not check_dependencies():
        print("請確認所有組件檔案存在")
        return
    
    try:
        # 嘗試導入並啟動時鐘組件
        if os.path.exists('clock_widget.py'):
            print("📦 載入時鐘組件...")
            # 動態導入clock_widget
            import importlib.util
            spec = importlib.util.spec_from_file_location("clock_widget", "clock_widget.py")
            clock_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(clock_module)
            
            # 嘗試啟動主應用
            if hasattr(clock_module, 'main'):
                print("✅ 啟動時鐘主程式")
                clock_module.main()
            elif hasattr(clock_module, 'ClockWidget'):
                print("✅ 啟動時鐘組件")
                root = tk.Tk()
                app = clock_module.ClockWidget(root)
                root.mainloop()
            else:
                print("⚠️  未找到主函數，嘗試直接執行模組")
                exec(open('clock_widget.py').read())
        
        else:
            # 如果沒有clock_widget，創建簡單的時鐘
            print("📦 啟動簡單時鐘...")
            create_simple_clock()
            
    except ImportError as e:
        print(f"❌ 導入錯誤: {e}")
        print("嘗試啟動簡單版本...")
        create_simple_clock()
        
    except Exception as e:
        print(f"❌ 啟動錯誤: {e}")
        print("嘗試啟動簡單版本...")
        create_simple_clock()

def create_simple_clock():
    """創建簡單的EVOI時鐘"""
    import datetime
    
    root = tk.Tk()
    root.title("EVOI Trading Clock - 簡單版")
    root.geometry("600x400")
    root.configure(bg='#1a1a1a')
    
    # 標題
    title_label = tk.Label(root, text="EVOI Trading Clock", 
                          font=('Arial', 20, 'bold'),
                          bg='#1a1a1a', fg='#00ff00')
    title_label.pack(pady=20)
    
    # 時間顯示
    time_var = tk.StringVar()
    time_label = tk.Label(root, textvariable=time_var,
                         font=('Courier New', 18),
                         bg='#1a1a1a', fg='#ffffff')
    time_label.pack(pady=10)
    
    # NYAM狀態
    nyam_var = tk.StringVar()
    nyam_label = tk.Label(root, textvariable=nyam_var,
                         font=('Arial', 14),
                         bg='#1a1a1a', fg='#ffff00')
    nyam_label.pack(pady=10)
    
    # 關鍵價位框架
    levels_frame = tk.LabelFrame(root, text="關鍵價位", 
                                bg='#2d2d2d', fg='#ffffff')
    levels_frame.pack(fill='x', padx=20, pady=20)
    
    # K1-K4輸入
    for i, level in enumerate(['K1', 'K2', 'K3', 'K4']):
        frame = tk.Frame(levels_frame, bg='#2d2d2d')
        frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(frame, text=f"{level}:", bg='#2d2d2d', fg='#ffffff',
                width=4).pack(side='left')
        
        entry = tk.Entry(frame, font=('Courier New', 12), width=15)
        entry.pack(side='left', padx=10)
    
    # 交易狀態
    status_frame = tk.LabelFrame(root, text="交易狀態",
                                bg='#2d2d2d', fg='#ffffff')
    status_frame.pack(fill='x', padx=20, pady=10)
    
    status_text = "今日交易: 0/3 | 連續虧損: 0/2 | 損益: $0.00"
    tk.Label(status_frame, text=status_text, bg='#2d2d2d', fg='#00ff00',
            font=('Arial', 12)).pack(pady=10)
    
    def update_time():
        """更新時間顯示"""
        now = datetime.datetime.now()
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        time_var.set(time_str)
        
        # 檢查NYAM時段
        if 21 <= now.hour < 23 or (now.hour == 21 and now.minute >= 30):
            nyam_var.set("🔥 NYAM 交易時段")
        else:
            nyam_var.set("⏰ 等待 NYAM 時段 (21:30-23:00)")
        
        root.after(1000, update_time)
    
    # 啟動時間更新
    update_time()
    
    # 按鈕框架
    btn_frame = tk.Frame(root, bg='#1a1a1a')
    btn_frame.pack(pady=20)
    
    tk.Button(btn_frame, text="測試完整版", 
             command=lambda: test_full_version(),
             bg='#4CAF50', fg='white', font=('Arial', 12)).pack(side='left', padx=10)
    
    tk.Button(btn_frame, text="關於", 
             command=lambda: show_about(),
             bg='#2196F3', fg='white', font=('Arial', 12)).pack(side='left', padx=10)
    
    def test_full_version():
        """測試完整版組件"""
        try:
            exec(open('clock_widget.py').read())
        except Exception as e:
            messagebox.showerror("錯誤", f"無法啟動完整版: {e}")
    
    def show_about():
        """顯示關於信息"""
        about_text = """EVOI Trading Clock 簡單版
        
這是一個備用版本，當主要組件無法啟動時使用。

功能：
• 基本時間顯示
• NYAM時段檢測
• 關鍵價位輸入
• 交易狀態顯示

如需完整功能，請確認以下檔案存在：
• clock_widget.py
• time_logic.py
• trading_panel.py"""
        
        messagebox.showinfo("關於", about_text)
    
    print("✅ 簡單版時鐘已啟動")
    root.mainloop()

if __name__ == "__main__":
    main()