import subprocess
import platform
from pynput.mouse import Button, Controller
from utils.helpers import get_screen_resolution
from config.settings import CONFIG

class MouseController:
    def __init__(self):
        self.mouse = Controller()
        self.screen_w, self.screen_h = get_screen_resolution()
        self.is_pressed = False
        self.scroll_accumulator = 0.0

    def move(self, x, y):
        """Move cursor to absolute coordinates (x, y)."""
        # Ensure coordinates are within screen bounds
        x = max(0, min(x, self.screen_w))
        y = max(0, min(y, self.screen_h))
        self.mouse.position = (x, y)

    def click(self, button=Button.left):
        """Perform a single click."""
        self.mouse.click(button, 1)

    def press(self, button=Button.left):
        """Press and hold mouse button."""
        if not self.is_pressed:
            self.mouse.press(button)
            self.is_pressed = True

    def release(self, button=Button.left):
        """Release mouse button."""
        if self.is_pressed:
            self.mouse.release(button)
            self.is_pressed = False

    def scroll(self, amount):
        """
        Smooth scroll with fractional accumulation.
        amount > 0: Scroll Up
        amount < 0: Scroll Down
        """
        self.scroll_accumulator += amount
        
        if abs(self.scroll_accumulator) >= 1.0:
            scroll_steps = int(self.scroll_accumulator)
            # pynput scroll: (0, 1) is UP, (0, -1) is DOWN
            self.mouse.scroll(0, scroll_steps)
            self.scroll_accumulator -= scroll_steps

    def minimize_current_window(self):
        """Minimize the currently active window."""
        system = platform.system()
        try:
            if system == 'Windows':
                import pygetwindow as gw
                active_window = gw.getActiveWindow()
                if active_window:
                    active_window.minimize()
            elif system == 'Linux':
                subprocess.run(['wmctrl', '-r', ':ACTIVE:', '-b', 'add,hidden'])
            print("[ACTION] Window minimized")
        except Exception as e:
            print(f"[ERROR] Failed to minimize window: {e}")

    def open_terminal(self):
        """Open system terminal."""
        system = platform.system()
        try:
            if system == 'Windows':
                try:
                    subprocess.Popen(['wt.exe'])  # Windows Terminal
                except FileNotFoundError:
                    subprocess.Popen(['cmd.exe'])  # Fallback
            elif system == 'Linux':
                terminals = ['gnome-terminal', 'konsole', 'xterm']
                for term in terminals:
                    try:
                        subprocess.Popen([term])
                        break
                    except FileNotFoundError:
                        continue
            print("[ACTION] Terminal opened")
        except Exception as e:
            print(f"[ERROR] Failed to open terminal: {e}")

    def get_position(self):
        """Get current mouse position."""
        return self.mouse.position
