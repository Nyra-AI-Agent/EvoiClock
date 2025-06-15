import tkinter as tk
from tkinter import font
import time
from datetime import datetime
import cnlunar
import os

# --- Constants ---
BG_COLOR = "#000000"
FG_COLOR = "#FFFFFF"
CARD_COLOR = "#1c1c1c"
WINDOW_WIDTH = 350
WINDOW_HEIGHT = 140
DIGIT_WIDTH = 35
DIGIT_HEIGHT = 70

# --- Quotes ---
QUOTES = {
    "morning": "一日之計在於晨，新的一天，新的開始。",
    "afternoon": "午後的陽光正好，稍作休息，繼續前行。",
    "evening": "夜幕降臨，願你卸下一天的疲憊，享受此刻的寧靜。",
    "night": "深夜了，放下執著，好好休息，夢裡什麼都有。"
}

# --- Main Application Class ---
class ClockApp:
    def __init__(self, root):
        self.root = root
        self.font_name = self.load_font("assets/Antonio-Regular.ttf", 75)
        self.root.title("EVOI NYAM 三單不貪停手")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.digits_frame = tk.Frame(root, bg=BG_COLOR)
        self.create_widgets()
        self.update_time()
        self.update_subtitle()
        self.update_quote()

    def load_font(self, font_path, size):
        abs_font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), font_path)
        try:
            font.Font(family="Antonio", size=12) # Check if already installed
            return "Antonio"
        except tk.TclError:
            try:
                # This is a bit of a hack for custom fonts in Tkinter on some systems
                self.root.tk.call('font', 'create', 'antonio_font', '-family', 'Antonio', '-size', '12')
                self.root.tk.call('font', 'configure', 'antonio_font', '-family', 'Antonio')
                return "Antonio"
            except:
                return "Arial" # Fallback

    def create_widgets(self):
        self.digits = []
        for i in range(8): # H H : M M : S S
            if i == 2 or i == 5:
                # Create Colon
                colon_frame = tk.Frame(self.digits_frame, bg=BG_COLOR)
                dot1 = tk.Label(colon_frame, text="•", bg=CARD_COLOR, fg=FG_COLOR, font=(self.font_name, 12, 'bold'))
                dot1.pack(pady=2)
                dot2 = tk.Label(colon_frame, text="•", bg=CARD_COLOR, fg=FG_COLOR, font=(self.font_name, 12, 'bold'))
                dot2.pack(pady=2)
                self.digits.append(colon_frame)
            else:
                digit = StaticDigit(self.digits_frame, self.font_name, CARD_COLOR)
                self.digits.append(digit)
            
            self.digits[i].pack(side='left', padx=2)

        self.subtitle_label = tk.Label(self.root, text="", bg=BG_COLOR, fg=FG_COLOR, font=(self.font_name, 12))
        self.quote_label = tk.Label(self.root, text="", bg=BG_COLOR, fg=FG_COLOR, font=(self.font_name, 14), wraplength=330, justify="center")

        # Layout using place for more control
        self.digits_frame.place(relx=0.5, rely=0.35, anchor='center')
        self.subtitle_label.place(relx=0.5, rely=0.7, anchor='center')
        self.quote_label.place(relx=0.5, rely=0.9, anchor='s', width=WINDOW_WIDTH-20)


    def update_time(self):
        current_time = time.strftime('%H%M%S')
        self.digits[0].set_digit(current_time[0])
        self.digits[1].set_digit(current_time[1])
        self.digits[3].set_digit(current_time[2])
        self.digits[4].set_digit(current_time[3])
        self.digits[6].set_digit(current_time[4])
        self.digits[7].set_digit(current_time[5])
        self.root.after(200, self.update_time)

    def update_subtitle(self):
        now = datetime.now()
        lunar_date = cnlunar.Lunar(now)
        
        western_date_str = now.strftime("%Y-%m-%d")
        lunar_info = f"{lunar_date.month_str}月{lunar_date.day_str}"
        jie_qi_str = lunar_date.jie_qi_str
        if jie_qi_str:
            jie_qi_str = f" {jie_qi_str}"

        # In Python's strftime, %w is 0 for Sunday. In weekday(), Monday is 0.
        weekday_map = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
        weekday_str = weekday_map[int(now.strftime("%w"))]

        subtitle_text = f"{western_date_str} ({lunar_info}) {weekday_str}{jie_qi_str}"
        self.subtitle_label.config(text=subtitle_text)
        self.root.after(60000, self.update_subtitle) # Update every minute

    def update_quote(self):
        current_hour = time.localtime().tm_hour
        quote = ""
        if 5 <= current_hour < 12:
            quote = QUOTES["morning"]
        elif 12 <= current_hour < 18:
            quote = QUOTES["afternoon"]
        elif 18 <= current_hour < 23:
            quote = QUOTES["evening"]
        else:
            quote = QUOTES["night"]
        
        if self.quote_label.cget("text") != quote:
            self.quote_label.config(text=quote)
        self.root.after(60000, self.update_quote) # Update every minute

    def on_close(self):
        self.root.destroy()

# --- Static Digit Class ---
class StaticDigit:
    def __init__(self, parent, font_name, card_color):
        self.canvas = tk.Canvas(parent, width=DIGIT_WIDTH, height=DIGIT_HEIGHT, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()
        self.font_name = font_name
        self.card_color = card_color
        self.digit = ""

    def set_digit(self, digit):
        if self.digit != digit:
            self.digit = digit
            self.draw_digit()

    def draw_digit(self):
        self.canvas.delete("all")
        # Draw the black card
        self.canvas.create_rectangle(0, 0, DIGIT_WIDTH, DIGIT_HEIGHT, fill=self.card_color, outline="")
        
        # Draw the digit text
        font_size = int(DIGIT_HEIGHT * 0.7)
        self.canvas.create_text(DIGIT_WIDTH / 2, DIGIT_HEIGHT / 2, text=self.digit,
                                fill=FG_COLOR, font=(self.font_name, font_size, 'normal'))

    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)

# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ClockApp(root)
    root.mainloop()