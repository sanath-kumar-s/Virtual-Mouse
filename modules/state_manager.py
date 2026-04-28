import time
from config.settings import CONFIG

class StateManager:
    def __init__(self):
        self.state = "IDLE"
        self.pinch_start_time = 0
        self.last_click_time = 0
        
        # Toggle control
        self.control_enabled = True
        self.fist_hold_start = None
        self.last_toggle_time = 0

    def update_toggle_state(self, is_fist):
        """
        Check if right hand fist is held for 3 seconds to toggle control.
        """
        current_time = time.time() * 1000
        
        # Check cooldown
        if (current_time - self.last_toggle_time) < CONFIG.get('TOGGLE_COOLDOWN_MS', 1000):
            return False
        
        if is_fist:
            if self.fist_hold_start is None:
                self.fist_hold_start = current_time
            
            hold_duration = current_time - self.fist_hold_start
            
            if hold_duration >= CONFIG.get('TOGGLE_HOLD_DURATION_MS', 3000):
                self.control_enabled = not self.control_enabled
                self.last_toggle_time = current_time
                self.fist_hold_start = None
                return True
        else:
            self.fist_hold_start = None
            
        return False

    def update(self, gesture, landmarks=None):
        """
        Updates the state machine based on the current gesture.
        Returns the new state and any actions to take.
        """
        curr_time = time.time()
        action = None

        if not self.control_enabled:
            self.state = "IDLE"
            return "IDLE", None

        # State Transitions
        if self.state == "IDLE":
            if gesture == "MOVE":
                self.state = "MOVE"
            elif gesture == "PINCH":
                self.state = "CLICK_READY"
                self.pinch_start_time = curr_time
            elif gesture == "SCROLL":
                self.state = "SCROLLING"

        elif self.state == "MOVE":
            if gesture == "PINCH":
                self.state = "CLICK_READY"
                self.pinch_start_time = curr_time
            elif gesture == "SCROLL":
                self.state = "SCROLLING"
            elif gesture == "NONE":
                self.state = "IDLE"

        elif self.state == "CLICK_READY":
            if gesture == "PINCH":
                # Check for Drag (Held for > 500ms)
                if (curr_time - self.pinch_start_time) > (CONFIG.get('DRAG_HOLD_TIME_MS', 500) / 1000):
                    self.state = "DRAGGING"
                    action = "MOUSE_DOWN"
            else:
                # Released before drag threshold -> Click
                if (curr_time - self.last_click_time) > (CONFIG.get('CLICK_COOLDOWN_MS', 300) / 1000):
                    action = "CLICK"
                    self.last_click_time = curr_time
                self.state = "IDLE"

        elif self.state == "DRAGGING":
            if gesture != "PINCH":
                self.state = "IDLE"
                action = "MOUSE_UP"

        elif self.state == "SCROLLING":
            if gesture != "SCROLL":
                self.state = "IDLE"

        return self.state, action
