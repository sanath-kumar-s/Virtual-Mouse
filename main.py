import sys
import os

# Suppress Qt monitor interface errors and force Windows platform
os.environ["QT_QPA_PLATFORM"] = "windows"
os.environ["QT_LOGGING_RULES"] = "qt.qpa.screen=false"

import cv2
import time
import numpy as np
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread, Signal, Slot

from config.settings import CONFIG
from modules.hand_detector import HandDetector
from modules.mouse_controller import MouseController
from modules.cursor_smoother import CursorSmoother
from modules.gesture_recognizer import GestureRecognizer
from modules.state_manager import StateManager
from modules.gui import StatusDashboard, RigWindow
from utils.visualization import Visualizer
from utils.error_handler import ErrorHandler
from utils.helpers import map_coordinates

class TrackingThread(QThread):
    status_updated = Signal(str, str, int, float)  # gesture, state, fps, latency
    rig_updated = Signal(np.ndarray)
    
    def __init__(self):
        super().__init__()
        self.running = True
        
    def run(self):
        # Initialize Camera
        cap = cv2.VideoCapture(CONFIG['CAMERA_ID'])
        cap.set(3, CONFIG['CAMERA_WIDTH'])
        cap.set(4, CONFIG['CAMERA_HEIGHT'])
        
        if not cap.isOpened():
            print("[ERROR] Camera not found")
            return

        # Initialize Modules
        detector = HandDetector()
        visualizer = Visualizer()
        mouse = MouseController()
        smoother = CursorSmoother()
        from modules.cursor_smoother import MouseInterpolator
        interpolator = MouseInterpolator(mouse, update_rate=120) # 120Hz interpolation
        interpolator.start()
        
        recognizer = GestureRecognizer()
        state_manager = StateManager()
        
        screen_w, screen_h = mouse.screen_w, mouse.screen_h
        click_threshold = CONFIG['CLICK_THRESHOLD_PX']
        
        prev_time = time.time()
        
        while self.running:
            success, img = cap.read()
            if not success:
                print("[ERROR] Failed to capture frame from camera.")
                break
            
            if img is None or img.size == 0:
                print("[WARNING] Empty frame received.")
                continue

            if CONFIG['MIRROR_VIDEO']:
                img = cv2.flip(img, 1)

            start_time = time.time()
            
            # 1. Detect Both Hands
            hands = detector.detect_hands(img)
            left_hand = hands['left']
            right_hand = hands['right']
            
            current_gesture = "NONE"
            current_state = "IDLE"
            
            # 2. Toggle Logic (Right Hand Fist hold for 3s)
            if right_hand:
                is_fist = recognizer.is_fist_closed(right_hand['landmarks'])
                if state_manager.update_toggle_state(is_fist):
                    print(f"[INFO] Virtual Mouse: {'ENABLED' if state_manager.control_enabled else 'DISABLED'}")
            
            # 3. Process Gestures (If enabled)
            if state_manager.control_enabled:
                # Right Hand (Primary Control)
                if right_hand:
                    # Cursor Movement (Palm Center)
                    palm = detector.get_hand_palm_center(right_hand['landmarks'])
                    raw_x, raw_y = palm['x'], palm['y']
                    
                    screen_x, screen_y = map_coordinates(raw_x, raw_y, 
                                                        CONFIG['CAMERA_WIDTH'], 
                                                        CONFIG['CAMERA_HEIGHT'], 
                                                        screen_w, screen_h)
                    
                    smooth_x, smooth_y = smoother.smooth(screen_x, screen_y)
                    # Instead of moving mouse directly, we set the target for high-FPS interpolator
                    interpolator.set_target(smooth_x, smooth_y)
                    
                    # Gesture Recognition
                    current_gesture, _ = recognizer.get_gesture(right_hand['landmarks'], click_threshold)
                    current_state, action = state_manager.update(current_gesture, right_hand['landmarks'])
                    
                    # Execute Actions
                    if action == "CLICK": mouse.click()
                    elif action == "MOUSE_DOWN": mouse.press()
                    elif action == "MOUSE_UP": mouse.release()
                    
                    # Optimized Scrolling
                    if current_state == "SCROLLING":
                        scroll_amount = recognizer.calculate_scroll(right_hand['landmarks'], img.shape[0])
                        mouse.scroll(scroll_amount)
                    else:
                        recognizer.reset_scroll_state()
                else:
                    current_state = "IDLE"
                    current_gesture = "NONE"
                    
                # Dual Hand Gestures
                if left_hand and right_hand:
                    dual_gesture = recognizer.detect_dual_hand_gestures(left_hand, right_hand)
                    if dual_gesture == "MINIMIZE":
                        mouse.minimize_current_window()
                        time.sleep(0.5)
                    elif dual_gesture == "OPEN_TERMINAL":
                        mouse.open_terminal()
                        time.sleep(0.5)
                
                # Left Hand Gestures (Secondary Control)
                elif left_hand:
                    if recognizer.is_pinching(left_hand['landmarks'], click_threshold):
                        if (time.time() - getattr(self, 'last_left_pinch_time', 0)) > 0.5:
                            from pynput.mouse import Button
                            mouse.click(Button.right)
                            self.last_left_pinch_time = time.time()
                            print("[ACTION] Right Click (Left Hand Pinch)")
            else:
                current_state = "DISABLED"
                current_gesture = "DISABLED"

            # 4. Rig Visualization (On separate black window)
            rig_img = visualizer.draw_hand_rig(img.shape, hands)
            self.rig_updated.emit(rig_img)
            
            # Stats & Timing
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
            prev_time = curr_time
            latency = (time.time() - start_time) * 1000
            
            self.status_updated.emit(current_gesture, current_state, int(fps), latency)
            
            # Small sleep to prevent high CPU usage in the thread
            time.sleep(0.01)

        interpolator.stop()
        cap.release()

    def stop(self):
        self.running = False
        self.wait()

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # Dark theme friendly style
    
    dashboard = StatusDashboard()
    rig_window = RigWindow()
    
    tracking_thread = TrackingThread()
    tracking_thread.status_updated.connect(dashboard.update_status)
    tracking_thread.rig_updated.connect(rig_window.update_image)
    
    dashboard.show()
    rig_window.show()
    
    # Position windows nicely
    rig_window.move(100, 100)
    dashboard.move(rig_window.x() + rig_window.width() + 20, rig_window.y())
    
    tracking_thread.start()
    
    # Ensure graceful shutdown
    def on_exit():
        tracking_thread.stop()
    
    app.aboutToQuit.connect(on_exit)
    
    try:
        sys.exit(app.exec())
    except SystemExit:
        pass

if __name__ == "__main__":
    main()
