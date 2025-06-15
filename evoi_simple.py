#!/usr/bin/env python3
"""
EVOI時鐘 - 確認版本
簡潔、實用的桌面時鐘
適用於已解決macOS顯示問題的環境
"""

import tkinter as tk
import datetime

print("=== macOS優化版啟動 ===")

# 創建窗口
root = tk.Tk()
root.title("EVOI時鐘")
root.geometry("280x120+200+200")
root.configure(bg='black')  # 純黑背景
root.attributes('-topmost', True)

# 創建主框架
main_frame = tk.Frame(root, bg='black')
main_frame.pack(fill='both', expand=True)

# 創建時間標籤 - 使用macOS系統字體和高對比度
time_label = tk.Label(
    main_frame,
    text="88:88:88",  # 先用固定寬字元測試
    font=('Helvetica', 28, 'bold'),  # macOS系統字體
    fg='lime',  # 亮綠色
    bg='black',
    width=10,  # 固定寬度
    height=2   # 固定高度
)
time_label.pack(pady=20)

# 創建副標題 - 高對比度
subtitle_label = tk.Label(
    main_frame,
    text="定時定法定量好",
    font=('Helvetica', 14),
    fg='yellow',  # 亮黃色
    bg='black'
)
subtitle_label.pack()

# 自動更新函數
def auto_update():
    try:
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M:%S")
        time_label.config(text=time_str)
        print(f"更新時間: {time_str}")
        
        # 強制重繪
        time_label.update_idletasks()
        root.update_idletasks()
        
        # 1秒後再次調用
        root.after(1000, auto_update)
    except Exception as e:
        print(f"錯誤: {e}")

# 測試按鈕 - 手動確認顯示
def test_display():
    time_label.config(text="TEST OK", fg='red')
    print("測試顯示: 文字應該變成紅色的 TEST OK")

test_button = tk.Button(
    main_frame,
    text="測試顯示",
    command=test_display,
    font=('Helvetica', 12),
    bg='white',
    fg='black'
)
test_button.pack(pady=10)

# 拖拽功能
def start_drag(event):
    root.x = event.x
    root.y = event.y

def drag_window(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")

root.bind('<Button-1>', start_drag)
root.bind('<B1-Motion>', drag_window)

# 立即測試顯示
now = datetime.datetime.now()
time_str = now.strftime("%H:%M:%S")
time_label.config(text=time_str)
print(f"初始顯示: {time_str}")

# 強制更新
root.update()

# 啟動自動更新
auto_update()

print("macOS優化說明:")
print("- 使用Helvetica字體（macOS原生）")
print("- 亮綠色時間顯示")
print("- 黃色副標題")
print("- 如果還是看不到，請點擊'測試顯示'按鈕")

root.mainloop()