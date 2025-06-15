import pystray
from PIL import Image
import os
from typing import Callable, Optional

class TrayManager:
    def __init__(self, icon_path: str = "assets/tray_icon.ico"):
        self.icon_path = icon_path
        self.icon: Optional[pystray.Icon] = None
        self.on_quit: Optional[Callable] = None
        self.on_show: Optional[Callable] = None
        self.on_hide: Optional[Callable] = None

    def create_icon(self) -> None:
        """創建系統托盤圖標"""
        try:
            if os.path.exists(self.icon_path):
                image = Image.open(self.icon_path)
            else:
                # 創建一個默認的圖標
                image = Image.new('RGB', (32, 32), color='black')
            
            menu = pystray.Menu(
                pystray.MenuItem('顯示', self._on_show),
                pystray.MenuItem('隱藏', self._on_hide),
                pystray.MenuItem('退出', self._on_quit)
            )
            
            self.icon = pystray.Icon("evoi_clock", image, "EVOI Trading Clock", menu)
        except Exception as e:
            print(f"創建系統托盤圖標時發生錯誤: {e}")

    def run(self) -> None:
        """運行系統托盤圖標"""
        if self.icon:
            self.icon.run()

    def stop(self) -> None:
        """停止系統托盤圖標"""
        if self.icon:
            self.icon.stop()

    def _on_quit(self) -> None:
        """退出處理"""
        if self.on_quit:
            self.on_quit()
        self.stop()

    def _on_show(self) -> None:
        """顯示處理"""
        if self.on_show:
            self.on_show()

    def _on_hide(self) -> None:
        """隱藏處理"""
        if self.on_hide:
            self.on_hide()

    def set_callbacks(self, on_quit: Callable, on_show: Callable, on_hide: Callable) -> None:
        """設置回調函數"""
        self.on_quit = on_quit
        self.on_show = on_show
        self.on_hide = on_hide 