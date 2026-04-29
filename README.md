# 🖐️ Virtual Mouse : Gesture Control System

![Hand Gesture Hero](C:\Users\Anjana Enterprises\.gemini\antigravity\brain\c016b3d7-b10a-4edd-8040-95eb5f37a090\hand_gesture_hero_1777397596711.png)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-teal.svg?style=for-the-badge&logo=google&logoColor=white)](https://mediapipe.dev/)
[![PySide6](https://img.shields.io/badge/PySide6-6.6.1-green.svg?style=for-the-badge&logo=qt&logoColor=white)](https://www.qt.io/qt-for-python)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**HandGestureDetector** is a premium, AI-powered virtual mouse system that transforms your webcam into a sophisticated input device. Leveraging MediaPipe and high-performance interpolation, it offers smooth, desktop-grade cursor control and a rich set of multi-hand gestures.

---

## ✨ Key Features

-   **🎯 Stable Palm-Based Tracking**: Unlike traditional fingertip tracking, our system uses the palm's center of mass for a rock-solid, jitter-free cursor experience.
-   **🤝 Multi-Hand Differentiation**: Independently detects and differentiates between left and right hands, enabling complex dual-hand interactions.
-   **🚀 High-Performance Interpolation**: Operates with a 120Hz interpolation layer, providing a buttery-smooth cursor movement that rivals high-end gaming mice.
-   **🌊 Velocity-Based Smooth Scrolling**: Natural-feeling scroll mechanics with acceleration and dead-zone management for precise document navigation.
-   **🖥️ Dual-Window Dashboard**:
    -   **Status Dashboard**: Real-time telemetry, gesture status, FPS, and latency monitoring.
    -   **Hand-Rig Visualization**: A dedicated dark-themed window showing a live digital skeleton of your hand movements.
-   **🛡️ Toggle Protection**: Prevent accidental inputs by holding a right-hand fist for 3 seconds to enable/disable the system.

---

## 🎮 Gesture Guide

| Gesture | Hand(s) | Action | Description |
| :--- | :--- | :--- | :--- |
| **Move** | Right | **Cursor Movement** | Index finger up only. Uses palm-center for stability. |
| **Pinch** | Right | **Left Click / Drag** | Thumb + Index pinch. Hold to drag. |
| **Pinch** | Left | **Right Click** | Thumb + Index pinch with the left hand. |
| **Index + Middle UP** | Right | **Scroll** | Move hand up/down to scroll vertically. |
| **Dual Pinch** | Both | **Minimize Window** | Pinch both hands simultaneously to hide the active app. |
| **Double Dual Pinch**| Both | **Open Terminal** | Pinch both hands twice in quick succession. |
| **Closed Fist (3s)** | Right | **Toggle System** | Hold a fist for 3 seconds to enable/disable control. |

---

## 🏗️ 3-Layer Architecture

The project follows a self-annealing, 3-layer architecture for maximum stability and maintainability:

1.  **📜 Directives (SOPs)**: Markdown-based operating procedures located in `/directives` that define *what* the system should do.
2.  **🎼 Orchestration**: The core logic in `main.py` and `/modules` that manages the data flow between sensors and executors.
3.  **🔨 Execution**: Deterministic scripts in `/execution` that handle environment-specific tasks like window management and OS calls.

---

## 🛠️ Tech Stack

-   **Core**: Python 3.10+
-   **AI/Vision**: MediaPipe (Hand Landmarking), OpenCV
-   **GUI**: PySide6 (Qt for Python)
-   **Input Emulation**: pynput
-   **Window Management**: pygetwindow, screeninfo

---

## 🚀 Getting Started

### 1. Prerequisites
-   Python 3.8 or higher.
-   A functional webcam.

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/HandGestureDetector.git
cd HandGestureDetector

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the App
On Windows, you can simply run the provided batch file:
```bash
./run.bat
```
Or execute manually:
```bash
python main.py
```

---

## ⚙️ Configuration

Customization options are available in `config/settings.py`. You can adjust:
-   **Sensitivity**: Cursor and scroll multipliers.
-   **Smoothing**: Frame buffer sizes for the smoothing algorithm.
-   **Thresholds**: Distance requirements for pinch detection.
-   **Display**: Camera resolution and mirroring options.

---

## 📂 Project Structure

```text
HandGestureDetector/
├── config/             # System settings and constants
├── directives/         # Standard Operating Procedures (Markdown)
├── execution/          # Deterministic execution scripts
├── modules/            # Core logic (Hand detection, Gestures, GUI)
├── utils/              # Helper functions and visualizations
├── main.py             # Application entry point
├── run.bat             # Windows launcher
└── requirements.txt    # Project dependencies
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<p align="center">
  Developed with ❤️ for a more intuitive desktop experience.
</p>
