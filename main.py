"""Pixel desktop companions using only the Python standard library."""
import argparse
import sys
import time
import tkinter as tk
from tkinter import ttk
from aquarium import Aquarium

PATTERNS = {
    'fish': ('......FF.......', '.....FFFF......', '..BBBBBBBB.....',
             '.BBEBBBBBBBB..T', 'BBBBBBBBBBBBTTT', '.BBBBBBBBBBBTTT',
             '..BBBBBBBBB..TT', '.....FFFF......', '......FF.......'),
    'crab': ('C.........C', 'CC.......CC', '.C.BBBBB.C.', '.CBBBBBBBC.',
             '..BEBBBEB..', '..BBBBBBB..', '.L.L.L.L.L.', 'L..L.L.L..L'),
    'shrimp': ('.........AA....', '.......AA......', '...BBBBBBE.....',
               '..BBBBBBBBBAAAA', '.BBBB...BB.....', 'BBB.....LL.....',
               '.BBB...L.L.....', '..TT...........'),
}
COLORS = {
    'goldfish': {'B': '#ffae42', 'F': '#ed7431', 'T': '#ed7431', 'E': '#182535'},
    'bluefish': {'B': '#52c9e8', 'F': '#397cdb', 'T': '#397cdb', 'E': '#182535'},
    'pinkfish': {'B': '#f09ac6', 'F': '#b867b7', 'T': '#b867b7', 'E': '#182535'},
    'crab': {'B': '#f36b50', 'C': '#fba05a', 'L': '#dc5040', 'E': '#182535'},
    'shrimp': {'B': '#ffc4a4', 'A': '#ee977b', 'L': '#ee977b', 'T': '#ed9678', 'E': '#182535'},
}


def enable_click_through(window):
    """Apply the Windows layered, transparent, nonactivating tool-window styles."""
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    user32.GetParent.argtypes = [wintypes.HWND]
    user32.GetParent.restype = wintypes.HWND
    hwnd = user32.GetParent(window.winfo_id()) or window.winfo_id()
    get_style, set_style = user32.GetWindowLongW, user32.SetWindowLongW
    get_style.argtypes = [wintypes.HWND, ctypes.c_int]
    get_style.restype = ctypes.c_long
    set_style.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_long]
    set_style.restype = ctypes.c_long
    style = get_style(hwnd, -20) | 0x80000 | 0x20 | 0x80 | 0x08000000
    ctypes.set_last_error(0)
    result = set_style(hwnd, -20, style)
    if not result and ctypes.get_last_error():
        raise ctypes.WinError(ctypes.get_last_error())


class App:
    def __init__(self, preview=False):
        self.root = tk.Tk()
        self.root.title('Floating Fish controls')
        self.root.resizable(False, False)
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        self.paused = False
        self.pixel_size = tk.IntVar(value=4)
        panel = ttk.Frame(self.root, padding=12)
        panel.pack()
        ttk.Label(panel, text='Your tiny desktop aquarium').pack(pady=(0, 8))
        self.pause_button = ttk.Button(panel, text='Pause', command=self.toggle_pause)
        self.pause_button.pack(fill='x')
        ttk.Label(panel, text='Pixel size').pack(pady=(8, 0))
        ttk.Spinbox(panel, from_=2, to=8, textvariable=self.pixel_size,
                    state='readonly', width=8).pack()
        ttk.Button(panel, text='Quit', command=self.close).pack(fill='x', pady=(8, 0))
        self.overlay = tk.Toplevel(self.root)
        self.overlay.protocol('WM_DELETE_WINDOW', self.close)
        windows_overlay = sys.platform == 'win32' and not preview
        if windows_overlay:
            self.overlay.overrideredirect(True)
            width, height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            background = '#010203'
            self.overlay.geometry(f'{width}x{height}+0+0')
            self.overlay.attributes('-transparentcolor', background)
            self.overlay.attributes('-topmost', True)
        else:
            width, height, background = 900, 550, '#182535'
            self.overlay.title('Floating Fish preview')
            self.overlay.geometry(f'{width}x{height}')
            self.overlay.resizable(False, False)
        self.canvas = tk.Canvas(self.overlay, bg=background, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.world = Aquarium(width, height)
        self.last_time = time.monotonic()
        self.overlay.update_idletasks()
        if windows_overlay:
            enable_click_through(self.overlay)
        self.root.lift()
        self.tick()

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_button.config(text='Resume' if self.paused else 'Pause')

    def draw(self):
        self.canvas.delete('animal')
        scale = self.pixel_size.get()
        for animal in self.world.animals:
            pattern = PATTERNS.get(animal.kind, PATTERNS['fish'])
            x, y = self.world.position(animal)
            for row, line in enumerate(pattern):
                for col, pixel in enumerate(line):
                    if pixel == '.':
                        continue
                    default_direction = 1 if animal.kind == 'shrimp' else -1
                    column = col if animal.direction == default_direction else len(line) - 1 - col
                    left, top = x + column * scale, y + row * scale
                    self.canvas.create_rectangle(left, top, left + scale, top + scale,
                                                 fill=COLORS[animal.kind][pixel], outline='', tags='animal')

    def tick(self):
        now = time.monotonic()
        dt, self.last_time = min(now - self.last_time, .1), now
        if not self.paused:
            self.world.update(dt, sprite_width=15 * self.pixel_size.get())
        self.draw()
        self.root.after(33, self.tick)

    def close(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true', help='Use an ordinary development window')
    App(preview=parser.parse_args().preview).run()
