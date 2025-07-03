#!/usr/bin/env python3
import tkinter as tk
import sys
import os

print("🚀 開始簡單測試")

def test_basic_window():
    print("🪟 創建基本窗口...")
    root = tk.Tk()
    root.title("簡單測試窗口")
    root.geometry("300x200")
    
    label = tk.Label(root, text="如果您看到這個文字，代表基本tkinter功能正常", 
                     wraplength=250, justify='center')
    label.pack(expand=True)
    
    button = tk.Button(root, text="點擊我", command=lambda: print("按鈕被點擊了！"))
    button.pack(pady=10)
    
    print("✅ 窗口創建完成，準備顯示...")
    root.after(5000, root.quit)
    
    print("🎯 開始主循環...")
    root.mainloop()
    print("🏁 主循環結束")

if __name__ == "__main__":
    print("=== 簡單測試開始 ===")
    test_basic_window()
    print("=== 簡單測試結束 ===")
