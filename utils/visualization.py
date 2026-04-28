import cv2
import time
import numpy as np
from config.settings import CONFIG, STATE_COLORS

from collections import deque

class Visualizer:
    def __init__(self):
        self.prev_time = 0
        self.fps = 0
        self.trail = deque(maxlen=CONFIG['TRAIL_LENGTH'])
        self.pulse_radius = 0
        self.pulse_dir = 1

    def draw_fps(self, img):
        curr_time = time.time()
        dt = curr_time - self.prev_time
        if dt > 0:
            self.fps = 1 / dt
        self.prev_time = curr_time
        
        cv2.putText(img, f"FPS: {int(self.fps)}", (CONFIG['CAMERA_WIDTH'] - 120, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        return img

    def draw_trail(self, img, pos):
        """Draws a trail following the cursor position."""
        self.trail.append(pos)
        for i in range(1, len(self.trail)):
            thickness = int(np.sqrt(CONFIG['TRAIL_LENGTH'] / float(i + 1)) * 2.5)
            cv2.line(img, self.trail[i-1], self.trail[i], CONFIG['CURSOR_COLOR'], thickness)
        return img

    def draw_pulse(self, img, pos, state):
        """Draws a pulsing circle when clicking or dragging."""
        if state in ['CLICKING', 'DRAGGING', 'CLICK_READY']:
            color = STATE_COLORS.get(state)
            self.pulse_radius += 2 * self.pulse_dir
            if self.pulse_radius > 30 or self.pulse_radius < 10:
                self.pulse_dir *= -1
            
            cv2.circle(img, pos, self.pulse_radius, color, 2)
        else:
            self.pulse_radius = 15
        return img

    def draw_control_box(self, img):
        """Draws the active Control Box area for reference."""
        margin = CONFIG.get('CONTROL_BOX_MARGIN', 100)
        h, w, _ = img.shape
        cv2.rectangle(img, (margin, margin), (w - margin, h - margin), (255, 255, 255), 1)
        cv2.putText(img, "ACTIVE ZONE", (margin + 5, margin + 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        return img

    def draw_dashboard(self, img, gesture, state, latency=0):
        """Draws a status dashboard on the frame."""
        h, w, _ = img.shape
        overlay = img.copy()
        
        # Dashboard Background (Semi-transparent)
        cv2.rectangle(overlay, (10, 10), (250, 160), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)
        
        # Dashboard Text
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.6
        color = (255, 255, 255)
        thickness = 1
        
        cv2.putText(img, "VIRTUAL MOUSE - STATUS", (20, 35), font, 0.7, (0, 255, 255), 2)
        cv2.line(img, (20, 45), (240, 45), (255, 255, 255), 1)
        
        cv2.putText(img, f"FPS: {int(self.fps)}", (20, 70), font, scale, color, thickness)
        cv2.putText(img, f"Gesture: {gesture}", (20, 95), font, scale, color, thickness)
        
        state_color = STATE_COLORS.get(state, (255, 255, 255))
        cv2.putText(img, f"State: {state}", (20, 120), font, scale, state_color, 2)
        cv2.putText(img, f"Latency: {int(latency)}ms", (20, 145), font, scale, color, thickness)
        
        return img

    def draw_gesture_indicator(self, img, pos, state):
        """Draws a visual indicator (circle) at the cursor position."""
        color = STATE_COLORS.get(state, (0, 255, 0))
        
        # Draw Trail
        img = self.draw_trail(img, pos)
        
        # Draw Pulse for interaction states
        img = self.draw_pulse(img, pos, state)
        
        # Main Cursor Circle
        cv2.circle(img, pos, 10, color, cv2.FILLED)
        cv2.circle(img, pos, 15, (255, 255, 255), 2)
        return img

    def draw_hand_rig(self, shape, hands_dict, connections=None):
        """Draws ONLY the hand rig on a clean black background with left/right differentiation."""
        rig_img = np.zeros(shape, dtype=np.uint8)
        
        if not hands_dict:
            return rig_img
            
        import mediapipe as mp
        mp_draw = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands
        
        for side, hand_data in hands_dict.items():
            if hand_data is None:
                continue
                
            landmarks_obj = hand_data['raw_landmarks']
            handedness = hand_data['handedness']
            
            # Color coding: Green for Left, Cyan for Right
            if handedness == 'Left':
                color = (0, 255, 0)
                label = "LEFT"
            else:
                color = (255, 255, 0)
                label = "RIGHT"
                
            landmark_style = mp_draw.DrawingSpec(color=color, thickness=2, circle_radius=3)
            connection_style = mp_draw.DrawingSpec(color=(255, 255, 255), thickness=2)
            
            mp_draw.draw_landmarks(
                rig_img, 
                landmarks_obj, 
                mp_hands.HAND_CONNECTIONS,
                landmark_style,
                connection_style
            )
            
            # Add label at wrist
            h, w, _ = shape
            wrist = landmarks_obj.landmark[0]
            label_pos = (int(wrist.x * w), int(wrist.y * h) - 20)
            cv2.putText(rig_img, label, label_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
        return rig_img
