import numpy as np
from collections import deque
import threading
import time
from config.settings import CONFIG

class CursorSmoother:
    def __init__(self, buffer_size=CONFIG['MOVING_AVG_WINDOW'], alpha=CONFIG['EXPONENTIAL_ALPHA']):
        self.buffer_x = deque(maxlen=buffer_size)
        self.buffer_y = deque(maxlen=buffer_size)
        self.alpha = alpha
        self.prev_x = 0
        self.prev_y = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.initialized = False

    def smooth(self, x, y):
        if not self.initialized:
            self.prev_x, self.prev_y = x, y
            self.initialized = True
            return int(x), int(y)

        # Calculate raw velocity
        v_x = x - self.prev_x
        v_y = y - self.prev_y
        
        # Adaptive alpha based on speed
        speed = np.sqrt(v_x**2 + v_y**2)
        dynamic_alpha = np.interp(speed, (5, 50), (self.alpha, 0.8))

        # Update buffers
        self.buffer_x.append(x)
        self.buffer_y.append(y)
        avg_x = sum(self.buffer_x) / len(self.buffer_x)
        avg_y = sum(self.buffer_y) / len(self.buffer_y)

        # Smooth position
        smooth_x = dynamic_alpha * avg_x + (1 - dynamic_alpha) * self.prev_x
        smooth_y = dynamic_alpha * avg_y + (1 - dynamic_alpha) * self.prev_y

        # Dead zone
        DEAD_ZONE = CONFIG.get('DEAD_ZONE_PX', 2)
        if abs(smooth_x - self.prev_x) < DEAD_ZONE: smooth_x = self.prev_x
        if abs(smooth_y - self.prev_y) < DEAD_ZONE: smooth_y = self.prev_y

        # Store smoothed velocity for interpolation/prediction
        self.velocity_x = smooth_x - self.prev_x
        self.velocity_y = smooth_y - self.prev_y
        
        self.prev_x, self.prev_y = smooth_x, smooth_y
        return int(smooth_x), int(smooth_y)

    def reset(self):
        """Resets the smoothing buffers."""
        self.buffer_x.clear()
        self.buffer_y.clear()
        self.initialized = False

class MouseInterpolator:
    """
    High-frequency interpolation engine to balance low detection FPS.
    Runs at 60Hz-120Hz to provide buttery smooth cursor movement.
    """
    def __init__(self, mouse_controller, update_rate=60):
        self.mouse = mouse_controller
        self.target_x = 0
        self.target_y = 0
        self.current_x = 0
        self.current_y = 0
        self.running = False
        self.update_interval = 1.0 / update_rate
        self.thread = None
        self.lerp_factor = 0.3 # Smoothing between steps

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def set_target(self, x, y):
        self.target_x = x
        self.target_y = y
        # If this is the first update, jump to position
        if self.current_x == 0:
            self.current_x, self.current_y = x, y

    def _run(self):
        while self.running:
            start_tick = time.time()
            
            # Linear Interpolation (LERP) towards target
            # This fills the gaps between low-FPS detection frames
            dx = self.target_x - self.current_x
            dy = self.target_y - self.current_y
            
            if abs(dx) > 0.1 or abs(dy) > 0.1:
                self.current_x += dx * self.lerp_factor
                self.current_y += dy * self.lerp_factor
                self.mouse.move(int(self.current_x), int(self.current_y))
            
            # Maintain fixed high-frequency rate
            elapsed = time.time() - start_tick
            sleep_time = max(0, self.update_interval - elapsed)
            time.sleep(sleep_time)
