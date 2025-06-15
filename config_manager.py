import json
import os
from typing import Dict, Any

class ConfigManager:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self) -> None:
        """載入配置文件"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.create_default_config()
        except Exception as e:
            print(f"載入配置文件時發生錯誤: {e}")
            self.create_default_config()

    def save_config(self) -> None:
        """保存配置到文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置文件時發生錯誤: {e}")

    def create_default_config(self) -> None:
        """創建默認配置"""
        self.config = {
            "window": {
                "position": {"x": 100, "y": 100},
                "opacity": 0.9,
                "always_on_top": True
            },
            "clock": {
                "mode": "NORMAL",
                "font_size": 48,
                "font_family": "Arial",
                "time_format": "%H:%M:%S"
            },
            "quote": {
                "rotation_interval": 300,
                "fade_duration": 1.0
            },
            "system": {
                "auto_start": False,
                "minimize_to_tray": True
            }
        }
        self.save_config()

    def get(self, key: str, default: Any = None) -> Any:
        """獲取配置值"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value

    def set(self, key: str, value: Any) -> None:
        """設置配置值"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config() 