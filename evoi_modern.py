#!/usr/bin/env python3
"""
EVOI多狀態交易時鐘 v2.5 - 現代化字體版
基於原版功能完整移植，升級界面設計和字體系統

核心功能保持：
✅ 三種模式自動切換 (Normal/NYAM/Quote)
✅ NYAM時段K棒倒數計時 (21:30-23:00)  
✅ 25句交易金句輪播系統
✅ 階段提醒動畫 (3秒紅閃/15秒橙提醒)
✅ 智能主題切換 (藍/綠/紫)
✅ 快捷鍵控制 (F11/F12/Esc)
✅ 拖拽移動 + 置頂顯示
✅ 大小切換模式

新增功能：
🆕 現代化字體系統 (Inter/SF Pro/Segoe UI)
🆕 優化的翻頁數字界面
🆕 增強的視覺效果
🆕 更精準的佈局控制
"""

import tkinter as tk
from tkinter import font
import datetime
import random
import platform
import sys

class ModernFontManager:
    """現代化字體管理器"""
    
    def __init__(self):
        self.fonts = self._load_fonts()
        
    def _load_fonts(self):
        """載入高品質字體"""
        fonts = {}
        
        # 檢測作業系統並選擇最佳字體
        system = platform.system()
        
        if system == "Darwin":  # macOS
            fonts.update({
                'primary': 'SF Pro Display',
                'mono': 'SF Mono',
                'fallback': 'Helvetica Neue'
            })
        elif system == "Windows":  # Windows
            fonts.update({
                'primary': 'Segoe UI',
                'mono': 'Consolas', 
                'fallback': 'Arial'
            })
        else:  # Linux
            fonts.update({
                'primary': 'Inter',
                'mono': 'JetBrains Mono',
                'fallback': 'DejaVu Sans'
            })
            
        # 通用現代化字體備選
        fonts.update({
            'modern_sans': ['Inter', 'SF Pro Display', 'Segoe UI', 'Roboto', 'Helvetica Neue'],
            'modern_mono': ['JetBrains Mono', 'Fira Code', 'SF Mono', 'Consolas', 'Monaco'],
            'digit_display': ['SF Pro Display', 'Segoe UI', 'Inter', 'Roboto']
        })
        
        return fonts
        
    def get_font(self, font_type, size, weight='normal'):
        """獲取指定類型的字體"""
        font_families = self.fonts.get(font_type, ['Arial'])
        
        if not isinstance(font_families, list):
            font_families = [font_families]
            
        # 嘗試每個字體直到找到可用的
        for family in font_families:
            try:
                test_font = font.Font(family=family, size=size, weight=weight)
                return test_font
            except:
                continue
                
        # 如果都失敗，使用系統默認
        return font.Font(family='TkDefaultFont', size=size, weight=weight)

class DigitDisplay:
    """現代化數字顯示組件"""
    
    def __init__(self, parent, font_manager, width=50, height=60):
        self.font_manager = font_manager
        self.current_value = "0"
        
        # 創建容器框架
        self.frame = tk.Frame(
            parent,
            bg='#1c1c1e',
            relief='flat',
            bd=0,
            width=width,
            height=height,
            highlightthickness=0
        )
        self.frame.pack_propagate(False)
        
        # 創建數字標籤
        self.label = tk.Label(
            self.frame,
            text="0",
            font=self.font_manager.get_font('digit_display', 36, 'bold'),
            fg='#ffffff',
            bg='#1c1c1e',
            justify='center'
        )
        self.label.pack(expand=True)
        
        # 添加圓角效果（通過Canvas實現）
        self._add_rounded_effect()
        
    def _add_rounded_effect(self):
        """添加圓角效果"""
        # 使用Canvas創建圓角矩形背景
        self.canvas = tk.Canvas(
            self.frame,
            width=self.frame['width'],
            height=self.frame['height'],
            bg='#1c1c1e',
            highlightthickness=0,
            bd=0
        )
        self.canvas.place(x=0, y=0)
        
        # 繪製圓角矩形
        self._draw_rounded_rect(0, 0, int(self.frame['width']), int(self.frame['height']), 8, '#1c1c1e')
        
        # 確保標籤在Canvas上方
        self.label.lift()
        
    def _draw_rounded_rect(self, x1, y1, x2, y2, radius, fill_color):
        """繪製圓角矩形"""
        # 創建圓角矩形
        self.canvas.create_rectangle(
            x1 + radius, y1, x2 - radius, y2,
            fill=fill_color, outline=fill_color
        )
        self.canvas.create_rectangle(
            x1, y1 + radius, x2, y2 - radius,
            fill=fill_color, outline=fill_color
        )
        
        # 添加圓角
        for corner_x, corner_y, start, extent in [
            (x1, y1, 90, 90),  # 左上角
            (x2 - 2*radius, y1, 0, 90),  # 右上角
            (x2 - 2*radius, y2 - 2*radius, 270, 90),  # 右下角
            (x1, y2 - 2*radius, 180, 90)  # 左下角
        ]:
            self.canvas.create_arc(
                corner_x, corner_y, corner_x + 2*radius, corner_y + 2*radius,
                start=start, extent=extent, fill=fill_color, outline=fill_color
            )
        
    def update_value(self, new_value):
        """更新數字並添加翻頁效果"""
        if str(new_value) != self.current_value:
            self.current_value = str(new_value)
            
            # 簡單的閃爍效果模擬翻頁
            self.label.config(fg='#666666')
            self.frame.after(50, lambda: self.label.config(text=self.current_value))
            self.frame.after(100, lambda: self.label.config(fg='#ffffff'))
            
    def set_color_theme(self, fg_color='#ffffff', bg_color='#1c1c1e', border_color='#1c1c1e'):
        """設置顏色主題"""
        self.frame.config(bg=bg_color)
        self.label.config(fg=fg_color, bg=bg_color)
        if hasattr(self, 'canvas'):
            self.canvas.config(bg=bg_color)
            self.canvas.delete('all')
            self._draw_rounded_rect(0, 0, int(self.frame['width']), int(self.frame['height']), 8, bg_color)

class EVOIMultiStateClock:
    """EVOI多狀態交易時鐘主類"""
    
    def __init__(self):
        # 初始化字體管理器
        self.font_manager = ModernFontManager()
        
        # 初始化主窗口
        self.root = tk.Tk()
        self.setup_window()
        
        # 狀態管理變數
        self.current_mode = 'normal'  # normal, nyam, quote
        self.is_minimized = False
        self.quote_index = 0
        self.quote_start_time = 0
        self.current_quotes = []
        self.animation_running = False
        
        # 拖拽變數
        self.drag_data = {"x": 0, "y": 0}
        
        # 顏色主題定義
        self.themes = {
            'normal': {
                'bg': '#f5f5f7',
                'border': '#007aff',
                'digit_fg': '#ffffff',
                'digit_bg': '#1c1c1e',
                'digit_border': '#1c1c1e',
                'subtitle_color': '#ff9500',
                'separator_color': '#1c1c1e'
            },
            'nyam': {
                'bg': '#f5f5f7',
                'border': '#00c896', 
                'digit_fg': '#ffffff',
                'digit_bg': '#1c1c1e',
                'digit_border': '#1c1c1e',
                'subtitle_color': '#34c759',
                'separator_color': '#1c1c1e'
            },
            'quote': {
                'bg': '#f5f5f7',
                'border': '#af52de',
                'digit_fg': '#ffffff',
                'digit_bg': '#1c1c1e', 
                'digit_border': '#1c1c1e',
                'subtitle_color': '#af52de',
                'separator_color': '#1c1c1e'
            }
        }
        
        # EVOI交易金句庫（完整保留）
        self.trading_quotes = [
            '三單停手不貪法', '定時定法定量好', '跟隨鯊魚去交易', '展開運鈔車人生',
            '機構創造流動性', '機構清除流動性', '機構創造不平衡', '機構平衡不平衡',
            '建立盤前偏見', '識別鯊魚覓食區', '建立盤中方向', '識別鯊魚去那裡',
            '一單一口不用貪', '連輸二單必停手', '頭頭高底底高', '頭頭低底底低',
            '上漲盤整猜上漲', '下跌盤整猜下跌', '識別慣性要練習', '慣性延續不要怕',
            '慣性改變有線索', '二百美金真的夠', '細水常流比氣長',
            '我是來市場賺錢', '不是來賭場輸錢'
        ]
        
        # 初始化界面和事件
        self.setup_ui()
        self.setup_bindings()
        self.start_clock()
        
    def setup_window(self):
        """設置主視窗屬性"""
        self.root.title("EVOI多狀態交易時鐘 v2.5")
        self.root.geometry("390x150+100+100")
        self.root.configure(bg='#f5f5f7')
        self.root.overrideredirect(True)  # 無邊框
        self.root.attributes('-topmost', True)  # 置頂
        
        # 透明度設置（跨平台兼容）
        try:
            self.root.attributes('-alpha', 0.95)
        except:
            pass
            
    def setup_ui(self):
        """設置現代化用戶界面"""
        # 主容器框架
        self.main_frame = tk.Frame(
            self.root,
            bg='#f5f5f7',
            relief='solid',
            bd=2,
            highlightbackground='#007aff',
            highlightthickness=2
        )
        self.main_frame.pack(fill='both', expand=True, padx=4, pady=4)
        
        # 控制按鈕（優化設計）
        self.control_btn = tk.Button(
            self.main_frame,
            text="─",
            font=self.font_manager.get_font('primary', 10, 'bold'),
            bg='#ffffff',
            fg='#666666',
            bd=0,
            relief='flat',
            highlightthickness=0,
            activebackground='#007aff',
            activeforeground='#ffffff',
            command=self.toggle_size,
            cursor='hand2',
            width=3,
            height=1
        )
        self.control_btn.place(x=350, y=10)
        
        # 數字時鐘容器
        self.clock_frame = tk.Frame(self.main_frame, bg='#f5f5f7')
        self.clock_frame.pack(pady=(25, 15))
        
        # 創建數字顯示組件
        self.digits = {}
        self.separators = {}
        
        # 小時數字
        self.digits['h1'] = DigitDisplay(self.clock_frame, self.font_manager, 50, 60)
        self.digits['h1'].frame.pack(side='left', padx=3)
        
        self.digits['h2'] = DigitDisplay(self.clock_frame, self.font_manager, 50, 60)
        self.digits['h2'].frame.pack(side='left', padx=3)
        
        # 分隔符 ":"
        self.separators['colon1'] = tk.Label(
            self.clock_frame,
            text=":",
            font=self.font_manager.get_font('digit_display', 36, 'bold'),
            fg='#1c1c1e',
            bg='#f5f5f7'
        )
        self.separators['colon1'].pack(side='left', padx=8)
        
        # 分鐘數字
        self.digits['m1'] = DigitDisplay(self.clock_frame, self.font_manager, 50, 60)
        self.digits['m1'].frame.pack(side='left', padx=3)
        
        self.digits['m2'] = DigitDisplay(self.clock_frame, self.font_manager, 50, 60)
        self.digits['m2'].frame.pack(side='left', padx=3)
        
        # 分隔符 ":"
        self.separators['colon2'] = tk.Label(
            self.clock_frame,
            text=":",
            font=self.font_manager.get_font('digit_display', 36, 'bold'),
            fg='#1c1c1e',
            bg='#f5f5f7'
        )
        self.separators['colon2'].pack(side='left', padx=8)
        
        # 秒鐘數字
        self.digits['s1'] = DigitDisplay(self.clock_frame, self.font_manager, 50, 60)
        self.digits['s1'].frame.pack(side='left', padx=3)
        
        self.digits['s2'] = DigitDisplay(self.clock_frame, self.font_manager, 50, 60)
        self.digits['s2'].frame.pack(side='left', padx=3)
        
        # 副標題/倒數計時顯示
        self.subtitle_label = tk.Label(
            self.main_frame,
            text="三單停手法 [NYAM] 不貪不爆倉",
            font=self.font_manager.get_font('primary', 14, 'bold'),
            fg='#ff9500',
            bg='#f5f5f7'
        )
        self.subtitle_label.pack(pady=(0, 20))
        
        # 金句顯示區域（初始隱藏）
        self.quote_label = tk.Label(
            self.main_frame,
            text="",
            font=self.font_manager.get_font('primary', 18, 'bold'),
            fg='#af52de',
            bg='#f5f5f7',
            wraplength=350,
            justify='center'
        )
        
        # 金句時間顯示
        self.quote_time_label = tk.Label(
            self.main_frame,
            text="",
            font=self.font_manager.get_font('mono', 16, 'normal'),
            fg='#af52de',
            bg='#f5f5f7'
        )
        
    def setup_bindings(self):
        """設置事件綁定"""
        # 拖拽功能綁定
        widgets_for_drag = [
            self.main_frame, self.clock_frame, self.subtitle_label
        ]
        
        for widget in widgets_for_drag:
            widget.bind("<Button-1>", self.start_drag)
            widget.bind("<B1-Motion>", self.do_drag)
            
        # 為數字組件添加拖拽
        for digit in self.digits.values():
            digit.frame.bind("<Button-1>", self.start_drag)
            digit.frame.bind("<B1-Motion>", self.do_drag)
            
        # 快捷鍵綁定
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.focus_set()
        
    def start_drag(self, event):
        """開始拖拽"""
        self.drag_data["x"] = event.x_root - self.root.winfo_x()
        self.drag_data["y"] = event.y_root - self.root.winfo_y()
        
    def do_drag(self, event):
        """執行拖拽"""
        x = event.x_root - self.drag_data["x"]
        y = event.y_root - self.drag_data["y"]
        self.root.geometry(f"+{x}+{y}")
        
    def on_key_press(self, event):
        """快捷鍵處理"""
        if event.keysym == 'F11':
            self.toggle_size()
        elif event.keysym == 'F12':
            self.toggle_visibility()
        elif event.keysym == 'Escape':
            self.root.quit()
            
    def toggle_size(self):
        """切換大小模式"""
        self.is_minimized = not self.is_minimized
        
        if self.is_minimized:
            # 縮小模式
            self.root.geometry("280x90")
            self.subtitle_label.pack_forget()
            self.control_btn.config(text="+")
            self.control_btn.place(x=240, y=8)
            
            # 調整數字大小
            for digit in self.digits.values():
                digit.frame.config(width=35, height=40)
                digit.label.config(font=self.font_manager.get_font('digit_display', 24, 'bold'))
                if hasattr(digit, 'canvas'):
                    digit.canvas.config(width=35, height=40)
                    digit.canvas.delete('all')
                    digit._draw_rounded_rect(0, 0, 35, 40, 6, '#1c1c1e')
                
            # 調整分隔符大小
            for sep in self.separators.values():
                sep.config(font=self.font_manager.get_font('digit_display', 24, 'bold'))
                
        else:
            # 標準模式
            self.root.geometry("390x150")
            if self.current_mode != 'quote':
                self.subtitle_label.pack(pady=(0, 20))
            self.control_btn.config(text="─")
            self.control_btn.place(x=350, y=10)
            
            # 恢復數字大小
            for digit in self.digits.values():
                digit.frame.config(width=50, height=60)
                digit.label.config(font=self.font_manager.get_font('digit_display', 36, 'bold'))
                if hasattr(digit, 'canvas'):
                    digit.canvas.config(width=50, height=60)
                    digit.canvas.delete('all')
                    digit._draw_rounded_rect(0, 0, 50, 60, 8, '#1c1c1e')
                
            # 恢復分隔符大小
            for sep in self.separators.values():
                sep.config(font=self.font_manager.get_font('digit_display', 36, 'bold'))
                
    def toggle_visibility(self):
        """切換顯示/隱藏"""
        if self.root.winfo_viewable():
            self.root.withdraw()
        else:
            self.root.deiconify()
            
    # ===============================
    # 時間檢測函數（完整保留原版邏輯）
    # ===============================
    def is_nyam_time(self, now):
        """檢查是否為NYAM時段 (21:30-23:00)"""
        total_minutes = now.hour * 60 + now.minute
        return 1290 <= total_minutes < 1380
        
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
    # 金句系統（完整保留原版邏輯）
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
            self.clock_frame.pack_forget()
            self.subtitle_label.pack_forget()
            self.quote_label.pack(pady=(40, 15))
            self.quote_time_label.pack()
        
        # 開始顯示金句
        self.root.after(1000, self.show_next_quote)
        
    def show_next_quote(self):
        """顯示下一句金句"""
        if self.current_mode != 'quote':
            return
            
        quote = self.current_quotes[self.quote_index]
        
        # 翻頁效果
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
            self.clock_frame.pack(pady=(25, 15))
            self.subtitle_label.pack(pady=(0, 20))
            
        # 應用正常主題
        self.apply_theme('normal')
        
    # ===============================
    # 主題系統
    # ===============================
    def apply_theme(self, theme_name):
        """應用主題顏色"""
        theme = self.themes[theme_name]
        
        # 更新主框架
        self.main_frame.config(
            bg=theme['bg'],
            highlightbackground=theme['border']
        )
        self.root.config(bg=theme['bg'])
        self.clock_frame.config(bg=theme['bg'])
        
        # 更新數字顯示主題
        for digit in self.digits.values():
            digit.set_color_theme(
                fg_color=theme['digit_fg'],
                bg_color=theme['digit_bg'],
                border_color=theme['digit_border']
            )
            
        # 更新分隔符顏色  
        for sep in self.separators.values():
            sep.config(fg=theme['separator_color'], bg=theme['bg'])
            
        # 更新文字顏色
        self.subtitle_label.config(fg=theme['subtitle_color'], bg=theme['bg'])
        
        if theme_name == 'quote':
            self.quote_label.config(fg=theme['subtitle_color'], bg=theme['bg'])
            self.quote_time_label.config(fg=theme['subtitle_color'], bg=theme['bg'])
            
    # ===============================
    # 時鐘更新函數（保留原版邏輯）
    # ===============================
    def update_time_display(self, time_str):
        """更新數字時鐘顯示"""
        parts = time_str.split(':')
        if len(parts) == 3:
            hour, minute, second = parts
            
            # 更新每個數字
            self.digits['h1'].update_value(hour[0])
            self.digits['h2'].update_value(hour[1])
            self.digits['m1'].update_value(minute[0])
            self.digits['m2'].update_value(minute[1])
            self.digits['s1'].update_value(second[0])
            self.digits['s2'].update_value(second[1])
            
    def update_nyam_clock(self, now):
        """更新NYAM時鐘"""
        time_str = now.strftime("%H:%M:%S")
        self.update_time_display(time_str)
        
        # K棒倒數計時
        seconds_to_next = 60 - now.second
        
        if not self.is_minimized:
            self.subtitle_label.config(text=f"⏱️ 下一K棒: {seconds_to_next}s")
            
        # 階段提醒動畫
        self.handle_stage_warning(seconds_to_next)
        
    def update_normal_clock(self, now):
        """更新正常時鐘"""
        time_str = now.strftime("%H:%M:%S")
        self.update_time_display(time_str)
        
        if not self.is_minimized:
            self.subtitle_label.config(text="三單停手法 [NYAM] 不貪不爆倉")
            
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
            self.start_warning_animation('#ff5252')
        elif seconds_to_next % 15 == 0 and seconds_to_next <= 45:
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
            self.main_frame.config(highlightbackground=self.themes[self.current_mode]['border'])
            
        self.root.after(200, lambda: self.animate_border(color, count + 1))
        
    def stop_warning_animation(self):
        """停止警告動畫"""
        self.animation_running = False
        
    # ===============================
    # 主更新循環（完整保留原版邏輯）
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
        print("🚀 EVOI多狀態交易時鐘 v2.5 現代化版啟動")
        print("✨ 新功能：現代化字體系統 + 優化界面")
        print("💡 快捷鍵: F11=切換大小, F12=隱藏/顯示, Esc=退出")
        print("🕐 NYAM時段: 21:30-23:00")
        print("📝 金句時間: 每小時 :10, :20, :30, :40, :50 分")
        print(f"🔤 使用字體: {self.font_manager.fonts}")
        
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
        """運行應用程序"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("程序被用戶中斷")
        except Exception as e:
            print(f"運行錯誤: {e}")

def main():
    """主函數"""
    print("=" * 70)
    print("🕒 EVOI多狀態交易時鐘 v2.5 - 現代化字體版")
    print("📈 鮣魚交易法推廣版 - 功能完整保留 + 界面升級")
    print("🔤 智能字體系統 - 跨平台現代化設計")
    print("=" * 70)
    
    try:
        app = EVOIMultiStateClock()
        app.run()
    except Exception as e:
        print(f"應用啟動失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()