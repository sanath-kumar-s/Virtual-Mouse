# Directive: Run Hand Gesture System

## Goal
Launch the Hand Gesture Detection system with dual-window interface (Status Dashboard and Hand Rig Visualization).

## Prerequisites
- Python 3.10+
- Webcam connected
- Dependencies installed (`pip install -r requirements.txt`)

## Tools to Use
- `execution/run_app.py`

## Steps
1. Ensure the camera is not being used by another application.
2. Run the execution script: `python execution/run_app.py`
3. Observe two windows:
   - **Status Dashboard**: Shows gesture info, FPS, and system state.
   - **Hand Rig**: Shows the skeletal tracking visualization.
4. To stop the system, close either window or press `Ctrl+C` in the terminal.

## Edge Cases & Troubleshooting
- **Camera Not Found**: Ensure `CAMERA_ID` in `config/settings.py` is correct (usually `0` or `1`).
- **Low FPS**: Ensure you are in a well-lit environment.
- **Gesture Lag**: The system uses a smoothing algorithm; check `CONFIG['SMOOTHING_FACTOR']` if lag is excessive.
