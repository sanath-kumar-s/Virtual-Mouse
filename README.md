# AI Virtual Mouse - Hand Gesture Recognition

A production-ready, real-time hand gesture recognition system that replaces traditional mouse interactions using webcam input.

## 🚀 Features
- **Smooth Cursor Movement**: Moving average + Exponential smoothing.
- **Gesture Set**:
  - **Move**: Index finger extended.
  - **Left Click**: Pinch (Thumb + Index) - Right Hand.
  - **Right Click**: Pinch (Thumb + Index) - Left Hand.
  - **Drag & Drop**: Sustained Pinch (>500ms) - Right Hand.
  - **Scroll**: Two fingers (Index + Middle) - Right Hand.
  - **Toggle Control**: Closed fist for 3 seconds - Right Hand.
  - **Minimize Window**: Simultaneous Pinch - Both Hands.
  - **Open Terminal**: Double Simultaneous Pinch - Both Hands.
- **Robustness**: Error handling for webcam/MediaPipe, dashboard UI, and rig visualization.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd HandGestureDetector
   ```

2. **Run the setup script (Windows)**:
   ```bash
   run.bat
   ```
   *This will create a virtual environment, install dependencies, and launch the application.*

## 🎮 Usage
- Show your hand to the webcam.
- The status dashboard will show detected gestures and current state.
- Use the **Index Finger** to move the cursor.
- **Pinch** to click or hold to drag.
- **Two fingers** up to scroll.

## ⚙️ Configuration
Modify `config/settings.py` to adjust:
- `CLICK_THRESHOLD_PX`: Sensitivity of the pinch gesture.
- `EXPONENTIAL_ALPHA`: Smoothness of cursor movement.
- `SCROLL_SENSITIVITY`: Speed of scrolling.

## 📦 Dependencies
- mediapipe
- opencv-python
- pynput
- numpy
- screeninfo
