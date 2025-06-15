#!/usr/bin/env python3
"""
EVOI多狀態交易時鐘 v2.0 - Python Tkinter版
完整移植HTML SPA版本的所有功能

功能：
- 三種模式：正常/NYAM/金句
- K棒倒數計時
- 階段提醒動畫
- 25句EVOI金句輪播
- 拖拽移動
- 大小切換
- 快捷鍵控制
"""

import tkinter as tk
from tkinter import font
import datetime
import random
import threading
import time

class EVOIMultiStateClock:
    def __init__(self):
        # ===============================
        # 初始化變數
        # ===============================
        self.root = tk.Tk()
        self.setup_window()
        
        # 狀態管理
        self.current_mode = 'normal'  # normal, nyam, quote
        self.is_minimized = False
        self.quote_index = 0
        self.quote_start_time = 0
        self.current_quotes = []
        self.animation_running = False
        
        # 拖拽變數
        self.drag_data = {"x": 0, "y": 0}
        
        # 顏色主題
        self.themes = {
            'normal': {
                'bg': '#1e222d',
                'border': '#4c9eff',
                'time_color': '#ffffff',
                'subtitle_color': '#ffffff',
                'glow_color': 'cyan'
            },
            'nyam': {
                'bg': '#1e222d', 
                'border': '#00ff88',
                'time_color': '#00ff88',
                'subtitle_color': '#ffffff',
                'glow_color': 'lime'
            },
            'quote': {
                'bg': '#1e222d',
                'border': '#9c27b0', 
                'time_color': '#e1bee7',
                'subtitle_color': '#9c27b0',
                'glow_color': 'magenta'
            }
        }
        
        # EVOI交易金句庫
        self.trading_quotes = [
            '三單停手不貪法', '定時定法定量好', '跟隨鯊魚去交易', '展開運鈔車人生',
            '機構創造流動性', '機構清除流動性', '機構創造不平衡', '機構平衡不平衡',
            '建立盤前偏見', '識別鯊魚覓食區', '建立盤中方向', '識別鯊魚去那裡',
            '一單一口不用貪', '連輸二單必停手', '頭頭高底底高', '頭頭低底底低',
            '上漲盤整猜上漲', '下跌盤整猜下跌', '識別慣性要練習', '慣性延續不要怕',
            '慣性改變有線索', '二百美金真的夠', '細水常流比氣長',
            '我是來市場賺錢', '不是來賭場輸錢'
        ]
        
        self.setup_ui()
        self.setup_bindings()
        self.start_clock()
        
    def setup_window(self):
        """設置主視窗"""
        self.root.title("EVOI多狀態交易時鐘")
        self.root.geometry("200x80+100+100")
        self.root.configure(bg='#1e222d')
        self.root.overrideredirect(True)  # 無邊框
        self.root.attributes('-topmost', True)  # 置頂
        
        # macOS 透明度支持
        try:
            self.root.attributes('-alpha', 0.95)
        except:
            pass
            
    def setup_ui(self):
        """設置UI界面"""
        # 主容器
        self.main_frame = tk.Frame(
            self.root,
            bg='#1e222d',
            relief='solid',
            bd=2,
            highlightbackground='#4c9eff',
            highlightthickness=2
        )
        self.main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # 控制按鈕
        self.control_btn = tk.Button(
    self.main_frame,
    text="─",
    font=('Helvetica', 10, 'bold'),
    bg='#2d2d2d',
    fg='#888888', 
    bd=1,
    relief='flat',              # ← 新增：扁平樣式
    highlightthickness=0,       # ← 新增：無高亮邊框
    activebackground='#1e222d', # ← 新增：點擊時背景色
    activeforeground='#4c9eff', # ← 新增：點擊時文字色
    command=self.toggle_size,
    cursor='hand2'
)
        
        # 時間顯示
        self.time_label = tk.Label(
            self.main_frame,
            text="00:00:00",
            font=('Helvetica', 30, 'bold'),
            fg='#ffffff',
            bg='#1e222d'
        )
        self.time_label.pack(pady=(5, 0))
        
        # 副標題/倒數計時q
        self.subtitle_label = tk.Label(
            self.main_frame,
            text="定時-定法-定量好",
            font=('Helvetica', 15),
            fg='#ffa726',
            bg='#1e222d'
        )
        self.subtitle_label.pack(pady=(0))  # 上方0間距，下方5間距
        
        # 金句顯示（初始隱藏）
        self.quote_label = tk.Label(
            self.main_frame,
            text="",
            font=('Helvetica', 24, 'bold'),
            fg='#e1bee7',
            bg='#1e222d',
            wraplength=180,
            justify='center'
        )
        
        # 金句時間顯示
        self.quote_time_label = tk.Label(
            self.main_frame,
            text="",
            font=('Helvetica', 15),
            fg='#9c27b0',
            bg='#1e222d'
        )
        
    def setup_bindings(self):
        """設置事件綁定"""
        # 拖拽功能
        self.main_frame.bind("<Button-1>", self.start_drag)
        self.main_frame.bind("<B1-Motion>", self.do_drag)
        self.time_label.bind("<Button-1>", self.start_drag)
        self.time_label.bind("<B1-Motion>", self.do_drag)
        self.subtitle_label.bind("<Button-1>", self.start_drag)
        self.subtitle_label.bind("<B1-Motion>", self.do_drag)
        
        # 快捷鍵
        self.root.bind('<F11>', lambda e: self.toggle_size())
        self.root.bind('<F12>', lambda e: self.toggle_visibility())
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()  # 確保能接收鍵盤事件
        
    def start_drag(self, event):
        """開始拖拽"""
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        
    def do_drag(self, event):
        """執行拖拽"""
        x = (self.root.winfo_x() + event.x - self.drag_data["x"])
        y = (self.root.winfo_y() + event.y - self.drag_data["y"])
        self.root.geometry(f"+{x}+{y}")
        
    def on_key_press(self, event):
        """鍵盤事件處理"""
        if event.keysym == 'F11':
            self.toggle_size()
        elif event.keysym == 'F12':
            self.toggle_visibility()
        elif event.keysym == 'Escape':
            self.root.quit()
            
    def toggle_size(self):
        """切換大小"""
        self.is_minimized = not self.is_minimized
        
        if self.is_minimized:
            self.root.geometry("140x45")
            self.time_label.config(font=('Helvetica', 16, 'bold'))
            self.subtitle_label.pack_forget()
            self.control_btn.config(text="+")
            self.control_btn.place(x=100, y=2)
        else:
            self.root.geometry("200x80")
            self.time_label.config(font=('Helvetica', 20, 'bold'))
            if self.current_mode != 'quote':
                self.subtitle_label.pack()
            self.control_btn.config(text="─")
            self.control_btn.place(x=180, y=2)
            
    def toggle_visibility(self):
        """切換顯示/隱藏"""
        if self.root.winfo_viewable():
            self.root.withdraw()
        else:
            self.root.deiconify()
            
    # ===============================
    # 時間檢測函數
    # ===============================
    def is_nyam_time(self, now):
        """檢查是否為NYAM時段 (21:30-23:00)"""
        total_minutes = now.hour * 60 + now.minute
        return 1290 <= total_minutes < 1380  # 21:30-23:00
        
    def is_quote_time(self, now):
        """檢查是否為金句時間（每小時:10,:20,:30,:40,:50分）"""
        return (now.minute % 10 == 0 and 
                now.minute != 0 and 
                now.second < 60)
                
    def get_clock_mode(self, now):
        """獲取當前時鐘模式"""
        if self.is_nyam_time(now):
            return 'nyam'
        elif self.is_quote_time(now):
            return 'quote'
        else:
            return 'normal'
            
    # ===============================
    # 金句系統
    # ===============================
    def select_random_quotes(self):
        """隨機選擇4句金句"""
        shuffled = self.trading_quotes.copy()
        random.shuffle(shuffled)
        return shuffled[:4]
        
    def start_quote_mode(self, now):
        """開始金句模式"""
        print("🎯 啟動金句模式")
        self.current_mode = 'quote'
        self.current_quotes = self.select_random_quotes()
        self.quote_index = 0
        self.quote_start_time = now.second
        
        # 應用金句主題
        self.apply_theme('quote')
        
        # 切換顯示
        if not self.is_minimized:
            self.time_label.pack_forget()
            self.subtitle_label.pack_forget()
            self.quote_label.pack(pady=(15, 5))
            self.quote_time_label.pack()
        
        # 開始顯示金句
        self.root.after(1000, self.show_next_quote)
        
    def show_next_quote(self):
        """顯示下一句金句"""
        if self.current_mode != 'quote':
            return
            
        quote = self.current_quotes[self.quote_index]
        
        # 翻頁效果（簡化版）
        self.quote_label.config(text="")
        self.root.after(200, lambda: self.quote_label.config(text=quote))
        
        self.quote_index = (self.quote_index + 1) % 4
        print(f"📝 顯示金句: {quote}")
        
    def end_quote_mode(self):
        """結束金句模式"""
        print("🔚 結束金句模式")
        self.current_mode = 'normal'
        
        # 恢復正常顯示
        if not self.is_minimized:
            self.quote_label.pack_forget()
            self.quote_time_label.pack_forget()
            self.time_label.pack(pady=(15, 5))
            self.subtitle_label.pack()
            
        # 應用正常主題
        self.apply_theme('normal')
        
    # ===============================
    # 主題系統
    # ===============================
    def apply_theme(self, theme_name):
        """應用主題"""
        theme = self.themes[theme_name]
        
        # 更新邊框顏色
        self.main_frame.config(highlightbackground=theme['border'])
        
        # 更新文字顏色
        self.time_label.config(fg=theme['time_color'])
        self.subtitle_label.config(fg=theme['subtitle_color'])
        
        if theme_name == 'quote':
            self.quote_label.config(fg=theme['time_color'])
            self.quote_time_label.config(fg=theme['subtitle_color'])
            
    # ===============================
    # 時鐘更新函數
    # ===============================
    def update_nyam_clock(self, now):
        """更新NYAM時鐘"""
        time_str = now.strftime("%H:%M:%S")
        self.time_label.config(text=time_str)
        
        # K棒倒數計時
        seconds_to_next = 60 - now.second
        
        if not self.is_minimized:
            self.subtitle_label.config(text=f"⏱️ 下一K棒: {seconds_to_next}s")
            
        # 階段提醒動畫
        self.handle_stage_warning(seconds_to_next)
        
    def update_normal_clock(self, now):
        """更新正常時鐘"""
        time_str = now.strftime("%H:%M:%S")
        self.time_label.config(text=time_str)
        
        if not self.is_minimized:
            self.subtitle_label.config(text="定時定法定量好")
            
    def update_quote_clock(self, now):
        """更新金句時鐘"""
        time_str = now.strftime("%H:%M:%S")
        if not self.is_minimized:
            self.quote_time_label.config(text=time_str)
        
        # 金句輪播邏輯
        elapsed = now.second - self.quote_start_time
        if elapsed > 0 and elapsed % 10 == 0 and elapsed <= 50:
            self.show_next_quote()
            
        # 檢查是否結束金句時間
        if not self.is_quote_time(now):
            self.end_quote_mode()
            
    def handle_stage_warning(self, seconds_to_next):
        """處理階段提醒動畫"""
        if seconds_to_next <= 3:
            # 紅色閃爍
            self.start_warning_animation('#ff5252')
        elif seconds_to_next % 15 == 0 and seconds_to_next <= 45:
            # 橙色提醒
            self.start_warning_animation('#ffa726')
        else:
            self.stop_warning_animation()
            
    def start_warning_animation(self, color):
        """開始警告動畫"""
        if not self.animation_running:
            self.animation_running = True
            self.animate_border(color, 0)
            
    def animate_border(self, color, count):
        """邊框閃爍動畫"""
        if not self.animation_running or count >= 6:
            self.animation_running = False
            self.apply_theme(self.current_mode)
            return
            
        if count % 2 == 0:
            self.main_frame.config(highlightbackground=color)
        else:
            self.main_frame.config(highlightbackground='#00ff88')
            
        self.root.after(200, lambda: self.animate_border(color, count + 1))
        
    def stop_warning_animation(self):
        """停止警告動畫"""
        self.animation_running = False
        
    # ===============================
    # 主更新循環
    # ===============================
    def update_clock(self):
        """主時鐘更新函數"""
        try:
            now = datetime.datetime.now()
            new_mode = self.get_clock_mode(now)
            
            # 模式切換檢測
            if new_mode != self.current_mode:
                print(f"🔄 模式切換: {self.current_mode} -> {new_mode}")
                
                if new_mode == 'quote':
                    self.start_quote_mode(now)
                elif self.current_mode == 'quote':
                    self.end_quote_mode()
                else:
                    self.current_mode = new_mode
                    self.apply_theme(new_mode)
                    
            # 根據當前模式更新顯示
            if self.current_mode == 'nyam':
                self.update_nyam_clock(now)
            elif self.current_mode == 'normal':
                self.update_normal_clock(now)
            elif self.current_mode == 'quote':
                self.update_quote_clock(now)
                
        except Exception as e:
            print(f"❌ 更新錯誤: {e}")
            
        # 安排下次更新
        self.root.after(100, self.update_clock)
        
    def start_clock(self):
        """啟動時鐘"""
        print("🚀 EVOI多狀態交易時鐘啟動")
        print("💡 快捷鍵: F11=切換大小, F12=隱藏/顯示, Esc=退出")
        print("🕐 NYAM時段: 21:30-23:00")
        print("📝 金句時間: 每小時 :10, :20, :30, :40, :50 分")
        
        # 初始模式設置
        now = datetime.datetime.now()
        initial_mode = self.get_clock_mode(now)
        self.current_mode = initial_mode
        self.apply_theme(initial_mode)
        
        # 如果啟動時就是金句時間，立即進入金句模式
        if initial_mode == 'quote':
            self.start_quote_mode(now)
            
        # 開始更新循環
        self.update_clock()
        
    def run(self):
        """運行應用"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("程序被用戶中斷")
        except Exception as e:
            print(f"運行錯誤: {e}")

def main():
    """主函數"""
    print("=" * 50)
    print("🕒 EVOI多狀態交易時鐘 v2.0 - Python版")
    print("📈 鮣魚交易法推廣版")
    print("=" * 50)
    
    try:
        app = EVOIMultiStateClock()
        app.run()
    except Exception as e:
        print(f"應用啟動失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()