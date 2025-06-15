#!/usr/bin/env python3
"""
EVOI Trading Clock v1.0
專業NQ期貨交易時鐘 - 主程式

功能：
- NYAM時段倒數計時 (21:30-23:00)
- K1-K4關鍵價位追蹤
- Kill Zone時段警告
- 交易狀態監控
- 風險管理提醒
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
import time
import threading
from typing import Optional, Dict, List
import json
import os

class EVOITradingClock:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_variables()
        self.setup_ui()
        self.setup_bindings()
        self.load_settings()
        self.start_clock()
        
    def setup_window(self):
        """設置主視窗"""
        self.root.title("EVOI Trading Clock v1.0")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(True, True)
        
        # 設置圖標（如果有的話）
        try:
            self.root.iconbitmap('evoi_icon.ico')
        except:
            pass
    
    def setup_variables(self):
        """初始化變數"""
        # 時間相關
        self.current_time = tk.StringVar()
        self.nyam_status = tk.StringVar()
        self.countdown = tk.StringVar()
        
        # 關鍵價位
        self.key_levels = {
            'K1': tk.DoubleVar(value=0.0),  # 前日高點
            'K2': tk.DoubleVar(value=0.0),  # 亞洲高點  
            'K3': tk.DoubleVar(value=0.0),  # 亞洲低點
            'K4': tk.DoubleVar(value=0.0),  # 開盤價
        }
        
        self.current_price = tk.DoubleVar(value=0.0)
        
        # 交易狀態
        self.trades_today = tk.IntVar(value=0)
        self.consecutive_losses = tk.IntVar(value=0)
        self.daily_pnl = tk.DoubleVar(value=0.0)
        self.can_trade = tk.BooleanVar(value=True)
        
        # Kill Zone時段定義 (台北時間)
        self.kill_zones = {
            'Asian Session': {'start': '07:00', 'end': '11:00', 'color': '#FF6B6B'},
            'London Open': {'start': '15:00', 'end': '18:00', 'color': '#4ECDC4'},
            'NYAM': {'start': '21:30', 'end': '23:00', 'color': '#45B7D1'},
            'NY Lunch': {'start': '23:00', 'end': '00:30', 'color': '#FFA07A'},
            'NYPM': {'start': '00:30', 'end': '04:00', 'color': '#98D8C8'},
        }
        
        # 運行狀態
        self.clock_running = True
        
    def setup_ui(self):
        """設置用戶介面"""
        # 主框架
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 上方：時鐘和倒數計時
        self.setup_clock_frame(main_frame)
        
        # 中間：關鍵價位
        self.setup_levels_frame(main_frame)
        
        # 下方：交易狀態
        self.setup_status_frame(main_frame)
        
        # 右鍵選單
        self.setup_context_menu()
        
    def setup_clock_frame(self, parent):
        """設置時鐘顯示區域"""
        clock_frame = tk.LabelFrame(parent, text="EVOI Trading Clock", 
                                   bg='#2d2d2d', fg='#ffffff', font=('Arial', 12, 'bold'))
        clock_frame.pack(fill='x', pady=(0, 10))
        
        # 當前時間
        time_label = tk.Label(clock_frame, textvariable=self.current_time,
                             font=('Courier New', 24, 'bold'), 
                             bg='#2d2d2d', fg='#00ff00')
        time_label.pack(pady=5)
        
        # NYAM狀態
        status_label = tk.Label(clock_frame, textvariable=self.nyam_status,
                               font=('Arial', 14, 'bold'),
                               bg='#2d2d2d', fg='#ffff00')
        status_label.pack(pady=2)
        
        # 倒數計時
        countdown_label = tk.Label(clock_frame, textvariable=self.countdown,
                                  font=('Arial', 16),
                                  bg='#2d2d2d', fg='#ff6666')
        countdown_label.pack(pady=2)
        
        # Kill Zone指示
        self.killzone_frame = tk.Frame(clock_frame, bg='#2d2d2d')
        self.killzone_frame.pack(fill='x', pady=5)
        
        self.killzone_labels = {}
        for zone_name in self.kill_zones:
            label = tk.Label(self.killzone_frame, text=zone_name[:4],
                           font=('Arial', 8), bg='#2d2d2d', fg='#666666',
                           width=8, height=2, relief='solid', bd=1)
            label.pack(side='left', padx=2)
            self.killzone_labels[zone_name] = label
    
    def setup_levels_frame(self, parent):
        """設置關鍵價位區域"""
        levels_frame = tk.LabelFrame(parent, text="關鍵價位 (Key Levels)", 
                                    bg='#2d2d2d', fg='#ffffff', font=('Arial', 12, 'bold'))
        levels_frame.pack(fill='x', pady=(0, 10))
        
        # 當前價格輸入
        price_frame = tk.Frame(levels_frame, bg='#2d2d2d')
        price_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(price_frame, text="當前價格:", bg='#2d2d2d', fg='#ffffff', 
                font=('Arial', 10)).pack(side='left')
        
        price_entry = tk.Entry(price_frame, textvariable=self.current_price, 
                              font=('Courier New', 12), width=10, justify='center')
        price_entry.pack(side='left', padx=(10, 0))
        
        update_btn = tk.Button(price_frame, text="更新", command=self.update_distances,
                              bg='#4CAF50', fg='white', font=('Arial', 10))
        update_btn.pack(side='left', padx=(10, 0))
        
        # 關鍵價位表格
        self.setup_levels_table(levels_frame)
        
    def setup_levels_table(self, parent):
        """設置關鍵價位表格"""
        table_frame = tk.Frame(parent, bg='#2d2d2d')
        table_frame.pack(fill='x', padx=10, pady=5)
        
        # 表頭
        headers = ['價位', '數值', '距離', '操作']
        header_frame = tk.Frame(table_frame, bg='#2d2d2d')
        header_frame.pack(fill='x', pady=(0, 5))
        
        for i, header in enumerate(headers):
            label = tk.Label(header_frame, text=header, bg='#404040', fg='#ffffff',
                           font=('Arial', 10, 'bold'), relief='raised', bd=1)
            label.grid(row=0, column=i, sticky='ew', padx=1)
        
        header_frame.grid_columnconfigure(1, weight=1)
        
        # 價位行
        self.level_entries = {}
        self.distance_labels = {}
        
        descriptions = {
            'K1': '前日高點',
            'K2': '亞洲高點', 
            'K3': '亞洲低點',
            'K4': '開盤價'
        }
        
        for i, (level, desc) in enumerate(descriptions.items()):
            row_frame = tk.Frame(table_frame, bg='#2d2d2d')
            row_frame.pack(fill='x', pady=1)
            
            # 價位名稱
            name_label = tk.Label(row_frame, text=f"{level}\n{desc}", 
                                 bg='#3d3d3d', fg='#ffffff', font=('Arial', 9),
                                 width=12, height=2, relief='solid', bd=1)
            name_label.grid(row=0, column=0, sticky='ew', padx=(0, 1))
            
            # 數值輸入
            entry = tk.Entry(row_frame, textvariable=self.key_levels[level],
                           font=('Courier New', 11), justify='center', width=12)
            entry.grid(row=0, column=1, sticky='ew', padx=1)
            self.level_entries[level] = entry
            
            # 距離顯示
            distance_label = tk.Label(row_frame, text="--", bg='#3d3d3d', fg='#ffff00',
                                    font=('Courier New', 10), width=12, height=2,
                                    relief='solid', bd=1)
            distance_label.grid(row=0, column=2, sticky='ew', padx=1)
            self.distance_labels[level] = distance_label
            
            # 快速設置按鈕
            set_btn = tk.Button(row_frame, text="設為當前", 
                               command=lambda l=level: self.set_current_price_as_level(l),
                               bg='#2196F3', fg='white', font=('Arial', 8), width=8)
            set_btn.grid(row=0, column=3, sticky='ew', padx=(1, 0))
            
            row_frame.grid_columnconfigure(1, weight=1)
    
    def setup_status_frame(self, parent):
        """設置交易狀態區域"""
        status_frame = tk.LabelFrame(parent, text="交易狀態監控", 
                                    bg='#2d2d2d', fg='#ffffff', font=('Arial', 12, 'bold'))
        status_frame.pack(fill='both', expand=True)
        
        # 左側：統計資料
        left_frame = tk.Frame(status_frame, bg='#2d2d2d')
        left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        stats = [
            ("今日交易次數", self.trades_today, "3"),
            ("連續虧損", self.consecutive_losses, "2"),
            ("今日損益", self.daily_pnl, "USD"),
        ]
        
        for i, (label_text, variable, unit) in enumerate(stats):
            frame = tk.Frame(left_frame, bg='#3d3d3d', relief='raised', bd=2)
            frame.pack(fill='x', pady=5)
            
            tk.Label(frame, text=label_text, bg='#3d3d3d', fg='#ffffff',
                    font=('Arial', 11)).pack(pady=2)
            
            value_frame = tk.Frame(frame, bg='#3d3d3d')
            value_frame.pack()
            
            if variable == self.daily_pnl:
                value_text = f"${variable.get():.2f}"
                color = '#00ff00' if variable.get() >= 0 else '#ff4444'
            else:
                value_text = f"{variable.get()}/{unit}"
                if variable == self.trades_today:
                    color = '#ff4444' if variable.get() >= 3 else '#ffff00'
                elif variable == self.consecutive_losses:
                    color = '#ff4444' if variable.get() >= 2 else '#00ff00'
                else:
                    color = '#ffffff'
            
            tk.Label(value_frame, text=value_text, bg='#3d3d3d', fg=color,
                    font=('Courier New', 14, 'bold')).pack()
        
        # 右側：風險控制
        right_frame = tk.Frame(status_frame, bg='#2d2d2d')
        right_frame.pack(side='right', fill='y', padx=10, pady=10)
        
        # 交易規則提醒
        rules_frame = tk.LabelFrame(right_frame, text="風險管理規則",
                                   bg='#2d2d2d', fg='#ffffff', font=('Arial', 10, 'bold'))
        rules_frame.pack(fill='both', expand=True)
        
        rules = [
            "✓ 止損: $75",
            "✓ 止盈: $500", 
            "✓ 日限: 3單",
            "✓ 連虧停手: 2單",
            "✓ 一口一單",
            "✓ NYAM時段: 21:30-23:00"
        ]
        
        for rule in rules:
            tk.Label(rules_frame, text=rule, bg='#2d2d2d', fg='#00ff00',
                    font=('Arial', 9), anchor='w').pack(fill='x', padx=5, pady=1)
        
        # 控制按鈕
        btn_frame = tk.Frame(right_frame, bg='#2d2d2d')
        btn_frame.pack(fill='x', pady=(10, 0))
        
        tk.Button(btn_frame, text="記錄交易", command=self.record_trade,
                 bg='#4CAF50', fg='white', font=('Arial', 10)).pack(fill='x', pady=2)
        
        tk.Button(btn_frame, text="重置計數", command=self.reset_counters,
                 bg='#FF9800', fg='white', font=('Arial', 10)).pack(fill='x', pady=2)
        
        tk.Button(btn_frame, text="保存設置", command=self.save_settings,
                 bg='#2196F3', fg='white', font=('Arial', 10)).pack(fill='x', pady=2)
    
    def setup_context_menu(self):
        """設置右鍵選單"""
        self.context_menu = tk.Menu(self.root, tearoff=0, bg='#2d2d2d', fg='#ffffff')
        self.context_menu.add_command(label="置頂顯示", command=self.toggle_topmost)
        self.context_menu.add_command(label="透明度設置", command=self.set_transparency)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="關於EVOI", command=self.show_about)
        
    def setup_bindings(self):
        """設置快捷鍵"""
        self.root.bind('<Button-3>', self.show_context_menu)
        self.root.bind('<F1>', lambda e: self.show_about())
        self.root.bind('<F5>', lambda e: self.update_distances())
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
        # 綁定Enter鍵更新距離
        for entry in self.level_entries.values():
            entry.bind('<Return>', lambda e: self.update_distances())
    
    def start_clock(self):
        """啟動時鐘更新"""
        self.update_clock()
        
    def update_clock(self):
        """更新時鐘顯示"""
        if not self.clock_running:
            return
            
        now = datetime.datetime.now()
        
        # 更新當前時間
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%Y-%m-%d %A")
        self.current_time.set(f"{time_str}\n{date_str}")
        
        # 更新NYAM狀態和倒數計時
        self.update_nyam_status(now)
        
        # 更新Kill Zone狀態
        self.update_killzone_status(now)
        
        # 安排下次更新
        self.root.after(1000, self.update_clock)
    
    def update_nyam_status(self, now):
        """更新NYAM時段狀態"""
        nyam_start = now.replace(hour=21, minute=30, second=0, microsecond=0)
        nyam_end = now.replace(hour=23, minute=0, second=0, microsecond=0)
        
        # 處理跨日情況
        if now.hour < 12:  # 深夜/凌晨
            nyam_start = nyam_start - datetime.timedelta(days=1)
            nyam_end = nyam_end - datetime.timedelta(days=1)
        
        if nyam_start <= now <= nyam_end:
            # 在NYAM時段內
            remaining = nyam_end - now
            total_duration = nyam_end - nyam_start
            progress = (total_duration - remaining) / total_duration * 100
            
            self.nyam_status.set(f"🔥 NYAM交易時段進行中 ({progress:.1f}%)")
            self.countdown.set(f"剩餘時間: {remaining.seconds//3600:02d}:{(remaining.seconds%3600)//60:02d}:{remaining.seconds%60:02d}")
            
        elif now < nyam_start:
            # NYAM還未開始
            time_to_nyam = nyam_start - now
            self.nyam_status.set("⏰ 等待NYAM開盤")
            self.countdown.set(f"距離開盤: {time_to_nyam.seconds//3600:02d}:{(time_to_nyam.seconds%3600)//60:02d}:{time_to_nyam.seconds%60:02d}")
            
        else:
            # NYAM已結束
            next_nyam = nyam_start + datetime.timedelta(days=1)
            time_to_next = next_nyam - now
            self.nyam_status.set("📊 NYAM已結束，覆盤分析")
            self.countdown.set(f"距離明日: {time_to_next.seconds//3600:02d}:{(time_to_next.seconds%3600)//60:02d}:{time_to_next.seconds%60:02d}")
    
    def update_killzone_status(self, now):
        """更新Kill Zone狀態"""
        current_time = now.strftime("%H:%M")
        
        for zone_name, zone_info in self.kill_zones.items():
            label = self.killzone_labels[zone_name]
            
            start_time = datetime.datetime.strptime(zone_info['start'], "%H:%M").time()
            end_time = datetime.datetime.strptime(zone_info['end'], "%H:%M").time()
            current_time_obj = now.time()
            
            # 處理跨日情況
            if start_time > end_time:  # 跨日時段
                is_active = current_time_obj >= start_time or current_time_obj <= end_time
            else:
                is_active = start_time <= current_time_obj <= end_time
            
            if is_active:
                label.config(bg=zone_info['color'], fg='white', font=('Arial', 8, 'bold'))
            else:
                label.config(bg='#2d2d2d', fg='#666666', font=('Arial', 8))
    
    def update_distances(self):
        """更新價位距離"""
        current = self.current_price.get()
        if current == 0:
            return
            
        for level_name, level_var in self.key_levels.items():
            level_value = level_var.get()
            if level_value == 0:
                self.distance_labels[level_name].config(text="未設置", fg='#666666')
                continue
                
            distance = level_value - current
            distance_points = distance * 4  # NQ每點$5，每0.25=$1.25
            
            if abs(distance) < 5:  # 接近警告
                color = '#ff4444'
                text = f"{distance:+.2f}\n⚠️{distance_points:+.0f}pts"
            elif distance > 0:  # 上方阻力
                color = '#ff6666'
                text = f"{distance:+.2f}\n↑{distance_points:+.0f}pts"
            else:  # 下方支撐
                color = '#66ff66'
                text = f"{distance:+.2f}\n↓{distance_points:+.0f}pts"
                
            self.distance_labels[level_name].config(text=text, fg=color)
    
    def set_current_price_as_level(self, level):
        """將當前價格設置為指定關鍵價位"""
        current = self.current_price.get()
        if current > 0:
            self.key_levels[level].set(current)
            self.update_distances()
    
    def record_trade(self):
        """記錄交易"""
        if self.trades_today.get() >= 3:
            messagebox.showwarning("交易限制", "今日已達3單上限！")
            return
            
        if self.consecutive_losses.get() >= 2:
            messagebox.showwarning("風險控制", "連續虧損2單，建議停止交易！")
            return
        
        # 簡單的交易記錄對話框
        result = simpledialog.askstring("記錄交易", "輸入交易結果 (格式: +500 或 -75):")
        if result:
            try:
                pnl = float(result)
                self.trades_today.set(self.trades_today.get() + 1)
                self.daily_pnl.set(self.daily_pnl.get() + pnl)
                
                if pnl < 0:
                    self.consecutive_losses.set(self.consecutive_losses.get() + 1)
                else:
                    self.consecutive_losses.set(0)
                    
                # 檢查停止交易條件
                if self.trades_today.get() >= 3:
                    messagebox.showinfo("交易提醒", "今日已完成3單，建議結束交易！")
                elif self.consecutive_losses.get() >= 2:
                    messagebox.showwarning("風險控制", "連續虧損2單，必須停止交易！")
                    
            except ValueError:
                messagebox.showerror("輸入錯誤", "請輸入有效的數字格式")
    
    def reset_counters(self):
        """重置計數器"""
        if messagebox.askyesno("確認重置", "確定要重置今日交易計數嗎？"):
            self.trades_today.set(0)
            self.consecutive_losses.set(0)
            self.daily_pnl.set(0.0)
    
    def save_settings(self):
        """保存設置到文件"""
        settings = {
            'key_levels': {k: v.get() for k, v in self.key_levels.items()},
            'current_price': self.current_price.get(),
            'trades_today': self.trades_today.get(),
            'consecutive_losses': self.consecutive_losses.get(),
            'daily_pnl': self.daily_pnl.get(),
        }
        
        try:
            with open('evoi_settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("保存成功", "設置已保存到 evoi_settings.json")
        except Exception as e:
            messagebox.showerror("保存失敗", f"無法保存設置: {e}")
    
    def load_settings(self):
        """從文件載入設置"""
        try:
            if os.path.exists('evoi_settings.json'):
                with open('evoi_settings.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # 載入關鍵價位
                for k, v in settings.get('key_levels', {}).items():
                    if k in self.key_levels:
                        self.key_levels[k].set(v)
                
                # 載入其他設置
                self.current_price.set(settings.get('current_price', 0.0))
                self.trades_today.set(settings.get('trades_today', 0))
                self.consecutive_losses.set(settings.get('consecutive_losses', 0))
                self.daily_pnl.set(settings.get('daily_pnl', 0.0))
                
        except Exception as e:
            print(f"載入設置失敗: {e}")
    
    def show_context_menu(self, event):
        """顯示右鍵選單"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def toggle_topmost(self):
        """切換置頂顯示"""
        current = self.root.attributes('-topmost')
        self.root.attributes('-topmost', not current)
    
    def set_transparency(self):
        """設置透明度"""
        alpha = simpledialog.askfloat("透明度設置", "輸入透明度 (0.1-1.0):", 
                                     initialvalue=1.0, minvalue=0.1, maxvalue=1.0)
        if alpha:
            self.root.attributes('-alpha', alpha)
    
    def show_about(self):
        """顯示關於信息"""
        about_text = """EVOI Trading Clock v1.0

專業NQ期貨交易時鐘
━━━━━━━━━━━━━━━━━━

核心功能：
• NYAM時段管理 (21:30-23:00)
• K1-K4關鍵價位追蹤
• Kill Zone時段監控
• 風險管理提醒
• 交易統計記錄

風險管理規則：
• 止損: $75
• 止盈: $500  
• 日限: 3單
• 連虧停手: 2單

快捷鍵：
• F1: 關於
• F5: 更新距離
• Esc: 退出

© 2024 EVOI Trading System
鮣魚交易法 - 運鈔車人生"""
        
        messagebox.showinfo("關於 EVOI Trading Clock", about_text)
    
    def run(self):
        """啟動應用"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.clock_running = False
            print("程序被用戶中斷")
        except Exception as e:
            messagebox.showerror("運行錯誤", f"應用運行時發生錯誤: {e}")
        finally:
            self.save_settings()

def main():
    """主函數"""
    print("🚀 啟動 EVOI Trading Clock v1.0")
    print("專業NQ期貨交易時鐘")
    print("━━━━━━━━━━━━━━━━━━━━")
    
    try:
        app = EVOITradingClock()
        app.run()
    except Exception as e:
        print(f"應用啟動失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()