import cv2
import time
import numpy as np
from config.settings import CONFIG
from utils.helpers import calculate_distance

class CalibrationWizard:
    def __init__(self, detector):
        self.detector = detector
        self.calibrated_threshold = CONFIG['CLICK_THRESHOLD_PX']
        self.is_calibrated = False

    def run(self, cap):
        """
        Runs a 5-second calibration phase.
        Asks user to pinch their thumb and index finger.
        """
        print("[INFO] Starting Calibration... Please PINCH your thumb and index finger now.")
        start_time = time.time()
        distances = []

        while time.time() - start_time < 5:
            success, img = cap.read()
            if not success: break
            
            if CONFIG['MIRROR_VIDEO']:
                img = cv2.flip(img, 1)

            img = self.detector.find_hands(img)
            lm_list = self.detector.find_position(img)

            if lm_list:
                # Landmark 4: Thumb Tip, 8: Index Tip
                p1 = (lm_list[4]['px_x'], lm_list[4]['px_y'])
                p2 = (lm_list[8]['px_x'], lm_list[8]['px_y'])
                dist = calculate_distance(p1, p2)
                distances.append(dist)
                
                # Visual Feedback
                cv2.line(img, p1, p2, (0, 255, 0), 3)
                cv2.putText(img, f"Calibrating: {5 - int(time.time() - start_time)}s", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(img, f"Current Dist: {int(dist)}", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow("Calibration Wizard", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if distances:
            # Set threshold to 1.5x the average pinched distance
            avg_dist = sum(distances) / len(distances)
            self.calibrated_threshold = int(avg_dist * 1.5)
            self.is_calibrated = True
            print(f"[INFO] Calibration Complete. New Click Threshold: {self.calibrated_threshold}")
        else:
            print("[WARNING] Calibration failed: No hand detected.")

        cv2.destroyWindow("Calibration Wizard")
        return self.calibrated_threshold
