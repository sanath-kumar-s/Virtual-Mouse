import sys
import cv2

class ErrorHandler:
    @staticmethod
    def handle_camera_error(cap):
        if not cap.isOpened():
            print("[ERROR] Could not open webcam. Please check connection.")
            return False
        return True

    @staticmethod
    def handle_mediapipe_error(e):
        print(f"[ERROR] MediaPipe Initialization Failed: {e}")
        sys.exit(1)

    @staticmethod
    def show_warning(img, message):
        """Displays a warning message on the OpenCV frame."""
        h, w, _ = img.shape
        cv2.putText(img, message, (w // 4, h // 2), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return img

    @staticmethod
    def log_event(message, level="INFO"):
        print(f"[{level}] {message}")
