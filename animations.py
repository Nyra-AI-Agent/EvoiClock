import tkinter as tk
from typing import Optional, Callable
import time

class AnimationManager:
    def __init__(self):
        self.fade_speed = 0.1
        self.flash_speed = 0.1
        self.flash_count = 3
        self.current_animation: Optional[Callable] = None
        self.animation_running = False

    def fade_out(self, widget: tk.Widget):
        """淡出動畫"""
        if self.animation_running:
            return
        
        self.animation_running = True
        alpha = 1.0
        
        def fade_step():
            nonlocal alpha
            if alpha > 0 and self.animation_running:
                widget.configure(foreground=self._adjust_alpha(widget.cget("foreground"), alpha))
                alpha -= self.fade_speed
                widget.after(10, fade_step)
            else:
                self.animation_running = False
        
        fade_step()

    def fade_in(self, widget: tk.Widget):
        """淡入動畫"""
        if self.animation_running:
            return
        
        self.animation_running = True
        alpha = 0.0
        
        def fade_step():
            nonlocal alpha
            if alpha < 1 and self.animation_running:
                widget.configure(foreground=self._adjust_alpha(widget.cget("foreground"), alpha))
                alpha += self.fade_speed
                widget.after(10, fade_step)
            else:
                self.animation_running = False
        
        fade_step()

    def flash_warning(self, widget: tk.Widget, color: str):
        """閃爍警告"""
        if self.animation_running:
            return
        
        self.animation_running = True
        original_color = widget.cget("bg")
        flash_count = 0
        
        def flash_step():
            nonlocal flash_count
            if flash_count < self.flash_count * 2 and self.animation_running:
                if flash_count % 2 == 0:
                    widget.configure(bg=color)
                else:
                    widget.configure(bg=original_color)
                flash_count += 1
                widget.after(int(self.flash_speed * 1000), flash_step)
            else:
                widget.configure(bg=original_color)
                self.animation_running = False
        
        flash_step()

    def _adjust_alpha(self, color: str, alpha: float) -> str:
        """調整顏色透明度"""
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            return f'#{r:02x}{g:02x}{b:02x}'
        return color

    def stop_current_animation(self):
        """停止當前動畫"""
        self.animation_running = False 