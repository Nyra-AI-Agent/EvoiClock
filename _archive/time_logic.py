import time
from datetime import datetime, timedelta, time
from typing import Optional, List, Dict, Tuple
import random
import pytz

class TimeLogic:
    def __init__(self):
        self.current_mode = "NORMAL"
        self.quotes = [
            "交易是等待的遊戲",
            "紀律勝過預測",
            "保護資金第一",
            "順勢而為",
            "控制風險，讓利潤奔跑"
        ]
        self.current_quote_index = 0
        
        # 定義交易時段
        self.trading_sessions = {
            'NYAM': {
                'start': time(21, 30),  # 21:30 CST
                'end': time(23, 0),     # 23:00 CST
                'kill_zones': [
                    (time(21, 30), time(22, 0)),  # 第一個 Kill Zone
                    (time(22, 30), time(23, 0))   # 第二個 Kill Zone
                ]
            }
        }
        
        # 設置時區
        self.local_tz = pytz.timezone('Asia/Taipei')
        self.ny_tz = pytz.timezone('America/New_York')
        
        # 初始化時間（使用本地時區）
        self.last_quote_time = datetime.now(self.local_tz)
        self.quote_interval = timedelta(minutes=5)
        self.current_quote = random.choice(self.quotes)
        
        # NYAM 時間段
        self.nyam_start = datetime.strptime("09:30", "%H:%M").time()
        self.nyam_end = datetime.strptime("16:00", "%H:%M").time()
        
        # 警告時間段
        self.warning_start = datetime.strptime("15:45", "%H:%M").time()
        self.critical_start = datetime.strptime("15:55", "%H:%M").time()

    def get_current_time(self) -> str:
        """獲取當前時間"""
        now = datetime.now()
        return now.strftime("%H:%M:%S")

    def get_time_until_nyam(self) -> Optional[Tuple[int, int, int]]:
        """計算距離 NYAM 開始的剩餘時間"""
        now = datetime.now()
        today_nyam = datetime.combine(now.date(), self.trading_sessions['NYAM']['start'])
        
        # 如果 NYAM 已經開始，返回 None
        if now.time() >= self.trading_sessions['NYAM']['start']:
            return None
            
        # 計算時間差
        time_diff = today_nyam - now
        hours = time_diff.seconds // 3600
        minutes = (time_diff.seconds % 3600) // 60
        seconds = time_diff.seconds % 60
        
        return (hours, minutes, seconds)

    def is_nyam_session(self) -> bool:
        """檢查是否在 NYAM 交易時段"""
        current_time = datetime.now().time()
        nyam = self.trading_sessions['NYAM']
        return nyam['start'] <= current_time <= nyam['end']

    def is_kill_zone(self) -> bool:
        """檢查是否在 Kill Zone"""
        current_time = datetime.now().time()
        nyam = self.trading_sessions['NYAM']
        
        for start, end in nyam['kill_zones']:
            if start <= current_time <= end:
                return True
        return False

    def get_current_kill_zone(self) -> Optional[Tuple[time, time]]:
        """獲取當前 Kill Zone 時段"""
        current_time = datetime.now().time()
        nyam = self.trading_sessions['NYAM']
        
        for start, end in nyam['kill_zones']:
            if start <= current_time <= end:
                return (start, end)
        return None

    def get_session_progress(self) -> float:
        """獲取當前交易時段的進度（0-1）"""
        if not self.is_nyam_session():
            return 0.0
            
        current_time = datetime.now().time()
        nyam = self.trading_sessions['NYAM']
        
        total_seconds = (nyam['end'].hour * 3600 + nyam['end'].minute * 60) - \
                       (nyam['start'].hour * 3600 + nyam['start'].minute * 60)
        current_seconds = (current_time.hour * 3600 + current_time.minute * 60 + current_time.second) - \
                         (nyam['start'].hour * 3600 + nyam['start'].minute * 60)
                         
        return min(1.0, max(0.0, current_seconds / total_seconds))

    def set_mode(self, mode: str):
        """設置時鐘模式"""
        self.current_mode = mode

    def get_current_quote(self) -> str:
        """獲取當前名言"""
        return self.quotes[self.current_quote_index]

    def next_quote(self):
        """切換到下一句名言"""
        self.current_quote_index = (self.current_quote_index + 1) % len(self.quotes)

    def check_warning(self) -> Optional[str]:
        """檢查是否需要警告"""
        if self.is_kill_zone():
            return "critical"
        elif self.is_nyam_session():
            return "stage"
        return None 