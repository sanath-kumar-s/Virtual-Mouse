import cv2
import os
import sys

# Add root to path so we can import modules
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from modules.hand_detector import HandDetector
from utils.calibration import CalibrationWizard
from config.settings import CONFIG

def main():
    print("[EXECUTION] Initializing Calibration Wizard...")
    
    # Initialize Camera
    cap = cv2.VideoCapture(CONFIG['CAMERA_ID'])
    cap.set(3, CONFIG['CAMERA_WIDTH'])
    cap.set(4, CONFIG['CAMERA_HEIGHT'])
    
    if not cap.isOpened():
        print("[ERROR] Camera not found. Please check CAMERA_ID in config/settings.py")
        return

    # Initialize Modules
    detector = HandDetector()
    wizard = CalibrationWizard(detector)
    
    try:
        new_threshold = wizard.run(cap)
        print(f"\n[SUCCESS] Recommended CLICK_THRESHOLD_PX: {new_threshold}")
        print("[ACTION] Please update 'CLICK_THRESHOLD_PX' in 'config/settings.py' with this value.")
    except Exception as e:
        print(f"[ERROR] Calibration failed: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
