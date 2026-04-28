# Directive: Calibrate System

## Goal
Calibrate the click threshold based on the user's specific hand size and pinch distance.

## Tools to Use
- `execution/calibrate.py`

## Steps
1. Run the calibration script: `python execution/calibrate.py`
2. A window titled "Calibration Wizard" will appear.
3. **Pinch** your thumb and index finger together and hold for 5 seconds.
4. Keep your hand within the camera's view.
5. Once the countdown finishes, the new `CLICK_THRESHOLD_PX` will be printed.
6. The system will automatically update the configuration (or prompt you to update `config/settings.py`).

## Expected Output
- A numerical value representing the optimal pixel distance for a "click" gesture.
- Improved accuracy in click detection.
