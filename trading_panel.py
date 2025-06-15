import tkinter as tk
from tkinter import ttk
from typing import Dict, Optional
from price_tracker import PriceTracker
from datetime import datetime, time

class TradingPanel(ttk.Frame):
    def __init__(self, parent, price_tracker: PriceTracker):
        super().__init__(parent)
        self.price_tracker = price_tracker
        
        # 創建樣式
        self.style = ttk.Style()
        self.style.configure('Price.TLabel', font=('SF Pro Display', 12))
        self.style.configure('KillZone.TLabel', font=('SF Pro Display', 12, 'bold'))
        self.style.configure('Role.TLabel', font=('SF Pro Display', 12, 'italic'))
        
        # 創建界面元素
        self.create_widgets()
        
        # 開始更新
        self.update_panel()
        
    def create_widgets(self):
        """創建界面元素"""
        # 價格水平框架
        self.price_frame = ttk.LabelFrame(self, text="關鍵價位", padding=5)
        self.price_frame.pack(fill='x', padx=5, pady=5)
        
        # 關鍵價位標籤
        self.price_labels = {}
        for level in ['K1', 'K2', 'K3', 'K4']:
            frame = ttk.Frame(self.price_frame)
            frame.pack(fill='x', pady=2)
            
            label = ttk.Label(frame, text=f"{level}:", width=5)
            label.pack(side='left')
            
            value = ttk.Label(frame, text="--", style='Price.TLabel')
            value.pack(side='left', padx=5)
            self.price_labels[level] = value
            
        # Kill Zone 框架
        self.kill_zone_frame = ttk.LabelFrame(self, text="交易時段", padding=5)
        self.kill_zone_frame.pack(fill='x', padx=5, pady=5)
        
        self.kill_zone_label = ttk.Label(
            self.kill_zone_frame,
            text="等待交易時段...",
            style='KillZone.TLabel'
        )
        self.kill_zone_label.pack(fill='x', pady=2)
        
        # 1K角色框架
        self.role_frame = ttk.LabelFrame(self, text="1K角色分析", padding=5)
        self.role_frame.pack(fill='x', padx=5, pady=5)
        
        self.role_label = ttk.Label(
            self.role_frame,
            text="等待分析...",
            style='Role.TLabel'
        )
        self.role_label.pack(fill='x', pady=2)
        
    def update_panel(self):
        """更新面板信息"""
        # 更新價格水平
        levels = self.price_tracker.get_key_levels()
        for level, value in levels.items():
            if value is not None:
                self.price_labels[level].config(text=f"{value:.2f}")
            else:
                self.price_labels[level].config(text="--")
                
        # 更新Kill Zone
        current_time = datetime.now().time()
        kill_zone = self.price_tracker.get_current_kill_zone(current_time)
        if kill_zone:
            self.kill_zone_label.config(
                text=f"當前時段: {kill_zone}",
                foreground='#ff5252' if 'KILL_ZONE' in kill_zone else '#00ff88'
            )
        else:
            self.kill_zone_label.config(text="非交易時段", foreground='#666666')
            
        # 更新1K角色
        current_role = self.price_tracker.get_current_role()
        if current_role:
            self.role_label.config(text=f"當前角色: {current_role}")
        else:
            self.role_label.config(text="等待角色分析...")
            
        # 每秒更新一次
        self.after(1000, self.update_panel) 