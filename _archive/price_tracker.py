import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional
import json
from datetime import datetime, time

class PriceTracker:
    def __init__(self):
        self.key_levels = {
            'K1': None,  # EMA
            'K2': None,  # VWAP
            'K3': None,  # Open
            'K4': None   # ICT Smart Money
        }
        self.kill_zones = {
            'NYAM': (time(21, 30), time(23, 0)),  # NYAM trading session
            'KILL_ZONE_1': (time(21, 30), time(22, 0)),  # First kill zone
            'KILL_ZONE_2': (time(22, 30), time(23, 0))   # Second kill zone
        }
        self.role_analysis = {
            'current_role': None,
            'role_history': []
        }
        
    def update_key_levels(self, levels: Dict[str, float]):
        """Update key price levels"""
        self.key_levels.update(levels)
        
    def get_key_levels(self) -> Dict[str, float]:
        """Get current key price levels"""
        return self.key_levels
        
    def is_kill_zone(self, current_time: time) -> bool:
        """Check if current time is in a kill zone"""
        for zone_name, (start, end) in self.kill_zones.items():
            if start <= current_time <= end:
                return True
        return False
        
    def get_current_kill_zone(self, current_time: time) -> Optional[str]:
        """Get current kill zone name if any"""
        for zone_name, (start, end) in self.kill_zones.items():
            if start <= current_time <= end:
                return zone_name
        return None
        
    def update_role_analysis(self, role: str):
        """Update 1K role analysis"""
        self.role_analysis['current_role'] = role
        self.role_analysis['role_history'].append({
            'role': role,
            'timestamp': datetime.now().isoformat()
        })
        
    def get_current_role(self) -> Optional[str]:
        """Get current 1K role"""
        return self.role_analysis['current_role']
        
    def save_state(self, filename: str = 'price_state.json'):
        """Save current state to file"""
        state = {
            'key_levels': self.key_levels,
            'role_analysis': self.role_analysis
        }
        with open(filename, 'w') as f:
            json.dump(state, f)
            
    def load_state(self, filename: str = 'price_state.json'):
        """Load state from file"""
        try:
            with open(filename, 'r') as f:
                state = json.load(f)
                self.key_levels = state['key_levels']
                self.role_analysis = state['role_analysis']
        except FileNotFoundError:
            pass 