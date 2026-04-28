import numpy as np
from screeninfo import get_monitors
from config.settings import CONFIG

def calculate_distance(p1, p2):
    """Calculate Euclidean distance between two points (x, y)."""
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_screen_resolution():
    """Get the primary monitor's resolution."""
    monitors = get_monitors()
    if monitors:
        # Assuming primary monitor is the first one or marked as primary
        primary = next((m for m in monitors if m.is_primary), monitors[0])
        return primary.width, primary.height
    return 1920, 1080  # Default fallback

def map_coordinates(x, y, cam_w, cam_h, screen_w, screen_h):
    """
    Map camera coordinates to screen coordinates using a Control Box for 
    increased sensitivity and edge reach.
    """
    margin = CONFIG.get('CONTROL_BOX_MARGIN', 100)
    
    # Define the active area (Control Box) in pixel space
    # MediaPipe x,y are 0-1, so we convert to cam pixels
    px_x = x * cam_w
    px_y = y * cam_h
    
    # Map the Control Box to the full Screen
    # np.interp clamps the values by default
    screen_x = np.interp(px_x, (margin, cam_w - margin), (0, screen_w))
    screen_y = np.interp(px_y, (margin, cam_h - margin), (0, screen_h))
    
    return int(screen_x), int(screen_y)

def get_finger_states(landmarks):
    """
    Determine if fingers are up or down.
    Returns a list of booleans: [thumb, index, middle, ring, pinky]
    """
    # Landmark IDs:
    # Thumb: tip=4, ip=3
    # Index: tip=8, pip=6
    # Middle: tip=12, pip=10
    # Ring: tip=16, pip=14
    # Pinky: tip=20, pip=18
    
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]
    
    states = []
    
    # Thumb: Check if tip is further left/right than IP joint (depends on hand orientation)
    # Simple check for now: thumb tip y vs IP joint y
    states.append(landmarks[4].y < landmarks[3].y)
    
    # Other 4 fingers: Check if tip is above PIP joint (y is inverted in image space)
    for tip, pip in zip(finger_tips, finger_pips):
        states.append(landmarks[tip].y < landmarks[pip].y)
        
    return states
