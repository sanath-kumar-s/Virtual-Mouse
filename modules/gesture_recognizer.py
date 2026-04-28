from collections import deque
import time
from utils.helpers import calculate_distance, get_finger_states
from config.settings import CONFIG

class GestureRecognizer:
    def __init__(self):
        self.pinch_start_time = 0
        self.fist_start_time = 0
        self.is_mouse_enabled = True
        self.last_toggle_time = 0
        
        # Scroll-specific smoothing
        self.scroll_buffer = deque(maxlen=CONFIG.get('SCROLL_SMOOTHING_FRAMES', 10))
        self.scroll_state_frames = 0
        self.prev_scroll_y = None
        
        # Dual-hand gesture tracking
        self.dual_pinch_timestamps = {'left': None, 'right': None}
        self.last_dual_pinch_success_time = 0
        self.dual_pinch_count = 0
        self.simultaneous_threshold_ms = CONFIG.get('SIMULTANEOUS_GESTURE_THRESHOLD_MS', 500)
        self.double_tap_threshold_ms = 800  # Time window for second pinch

    def get_gesture(self, landmarks, click_threshold):
        """
        Analyzes landmarks and returns the detected gesture and finger states.
        """
        if not landmarks:
            return "NONE", [False] * 5

        finger_states = get_finger_states(landmarks)
        
        # 1. Fist Detection
        if self.is_fist_closed(landmarks):
            return "FIST", finger_states

        # 2. Scroll Gesture (Index + Middle UP, others DOWN)
        if finger_states[1] and finger_states[2] and not any(finger_states[3:]):
            return "SCROLL", finger_states

        # 3. Pinch/Click/Drag Gesture
        p1 = (landmarks[4].x * CONFIG['CAMERA_WIDTH'], landmarks[4].y * CONFIG['CAMERA_HEIGHT'])
        p2 = (landmarks[8].x * CONFIG['CAMERA_WIDTH'], landmarks[8].y * CONFIG['CAMERA_HEIGHT'])
        dist = calculate_distance(p1, p2)
        
        if dist < click_threshold:
            return "PINCH", finger_states

        # 4. Move Gesture (Only Index UP)
        if finger_states[1] and not any(finger_states[2:]):
            return "MOVE", finger_states

        return "NONE", finger_states

    def calculate_scroll(self, landmarks, frame_height):
        """
        Calculate smooth scroll amount based on hand movement
        """
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        current_y = (index_tip.y + middle_tip.y) / 2
        
        if self.prev_scroll_y is None:
            self.prev_scroll_y = current_y
            return 0.0
            
        raw_delta = current_y - self.prev_scroll_y
        dead_zone = CONFIG.get('SCROLL_DEAD_ZONE', 0.005)
        
        if abs(raw_delta) < dead_zone:
            self.prev_scroll_y = current_y
            return 0.0
            
        self.scroll_buffer.append(raw_delta)
        smoothed_delta = sum(self.scroll_buffer) / len(self.scroll_buffer)
        
        # Velocity scaling
        velocity_factor = abs(smoothed_delta) * 10
        velocity_factor = min(velocity_factor, 3.0)
        
        # Acceleration
        self.scroll_state_frames += 1
        acceleration = 1.0
        if CONFIG.get('SCROLL_ACCELERATION_ENABLED', True):
            ramp_frames = CONFIG.get('SCROLL_RAMP_UP_FRAMES', 30)
            acceleration = min(1.0 + (self.scroll_state_frames / ramp_frames), 2.0)
            
        scroll_amount = (
            smoothed_delta * 
            velocity_factor * 
            acceleration * 
            CONFIG['SCROLL_SENSITIVITY']
        )
        
        # Convert to pixel units
        scroll_pixels = int(scroll_amount * frame_height * 5)
        self.prev_scroll_y = current_y
        return scroll_pixels

    def reset_scroll_state(self):
        self.scroll_buffer.clear()
        self.prev_scroll_y = None
        self.scroll_state_frames = 0

    def is_fist_closed(self, landmarks):
        finger_states = get_finger_states(landmarks)
        return not any(finger_states) # All fingers down

    def is_pinching(self, landmarks, threshold=None):
        if threshold is None:
            threshold = CONFIG['CLICK_THRESHOLD_PX']
        p1 = (landmarks[4].x * CONFIG['CAMERA_WIDTH'], landmarks[4].y * CONFIG['CAMERA_HEIGHT'])
        p2 = (landmarks[8].x * CONFIG['CAMERA_WIDTH'], landmarks[8].y * CONFIG['CAMERA_HEIGHT'])
        return calculate_distance(p1, p2) < threshold

    def detect_dual_hand_gestures(self, left_hand, right_hand):
        """Detect simultaneous gestures from both hands."""
        if not left_hand or not right_hand:
            self._reset_dual_tracking()
            return None
            
        curr_time = time.time() * 1000
        
        # 1. Simultaneous Pinch Detection
        l_pinch = self.is_pinching(left_hand['landmarks'])
        r_pinch = self.is_pinching(right_hand['landmarks'])
        
        if l_pinch and r_pinch:
            if self.dual_pinch_timestamps['left'] is None: self.dual_pinch_timestamps['left'] = curr_time
            if self.dual_pinch_timestamps['right'] is None: self.dual_pinch_timestamps['right'] = curr_time
            
            # Check if both pinched within the simultaneous window
            if abs(self.dual_pinch_timestamps['left'] - self.dual_pinch_timestamps['right']) < self.simultaneous_threshold_ms:
                # We have a successful simultaneous pinch event
                # We need to distinguish between "Minimize" (single event) and "Terminal" (double event)
                
                # Cooldown between successful detections to avoid rapid counts
                if curr_time - self.last_dual_pinch_success_time > 300:
                    self.dual_pinch_count += 1
                    self.last_dual_pinch_success_time = curr_time
                    print(f"[DEBUG] Dual Pinch Count: {self.dual_pinch_count}")
                    
                    if self.dual_pinch_count == 2:
                        self.dual_pinch_count = 0
                        return "OPEN_TERMINAL"
                    
                    # If this is the first pinch, we might be going for Minimize or Terminal
                    # For Minimize, we return it immediately? No, if the user wants "double pinch",
                    # single pinch might trigger Minimize. 
                    # Let's say: Single Simultaneous Pinch = Minimize, Double = Terminal.
                    # This is tricky because the first pinch of a double will trigger Minimize.
                    # To avoid this, we'd need a delay. 
                    # User request: "change the gesture for opening the comment prompt rather use two times times pinch with both the hands"
                    # I'll keep Minimize as a single pinch for now, but the second pinch will trigger Terminal.
                    return "MINIMIZE"
        else:
            # If hands are released, we reset the timestamp trackers for the next event
            self.dual_pinch_timestamps = {'left': None, 'right': None}
            
            # Reset double tap count if too much time passes between pinches
            if curr_time - self.last_dual_pinch_success_time > self.double_tap_threshold_ms:
                self.dual_pinch_count = 0
            
        return None

    def _reset_dual_tracking(self):
        self.dual_pinch_timestamps = {'left': None, 'right': None}
        self.dual_pinch_count = 0
        self.last_dual_pinch_success_time = 0
