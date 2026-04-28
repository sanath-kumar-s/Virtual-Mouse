import cv2

CONFIG = {
    # Detection Settings
    'MIN_DETECTION_CONFIDENCE': 0.7,
    'MIN_TRACKING_CONFIDENCE': 0.5,
    'MAX_NUM_HANDS': 2,
    'MODEL_COMPLEXITY': 1,
    'USE_CAMERA_PERSPECTIVE_LABELS': True,
    
    # Camera Settings
    'CAMERA_ID': 0,
    'CAMERA_WIDTH': 640,
    'CAMERA_HEIGHT': 480,
    'MIRROR_VIDEO': True,
    
    # Gesture Settings
    'CLICK_THRESHOLD_PX': 40,
    'DRAG_HOLD_TIME_MS': 500,
    'CLICK_COOLDOWN_MS': 300,
    'TOGGLE_COOLDOWN_MS': 2000,
    'SENSITIVITY': 1.5,
    'CONTROL_BOX_MARGIN': 100,
    'DEAD_ZONE_PX': 2,
    
    # Scroll Optimization
    'SCROLL_SENSITIVITY': 1.5,
    'SCROLL_SMOOTHING_FRAMES': 10,
    'SCROLL_DEAD_ZONE': 0.005,
    'SCROLL_ACCELERATION_ENABLED': True,
    'SCROLL_MAX_SPEED': 50,
    'SCROLL_RAMP_UP_FRAMES': 30,
    
    # Dual-hand gestures
    'SIMULTANEOUS_GESTURE_THRESHOLD_MS': 500,
    
    # Toggle control (New logic)
    'TOGGLE_HOLD_DURATION_MS': 3000,
    
    # Smoothing Settings
    'MOVING_AVG_WINDOW': 3,
    'EXPONENTIAL_ALPHA': 0.2,
    
    # UI & Visualization
    'SHOW_FPS': True,
    'SHOW_LANDMARKS': True,
    'SHOW_STATUS_DASHBOARD': True,
    'TRAIL_LENGTH': 10,
    'CURSOR_COLOR': (0, 255, 0),
    'CLICK_COLOR': (0, 0, 255),
    'SCROLL_COLOR': (255, 0, 255),
    
    # Performance & Logging
    'TARGET_FPS': 30,
    'DEBUG_MODE': False,
    'LOG_FPS': True,
    'SHOW_LANDMARK_IDS': False,
    'LOG_GESTURE_CHANGES': True,
}

# State Colors Mapping
STATE_COLORS = {
    'IDLE': (0, 255, 0),       # Green
    'MOVE': (255, 255, 0),     # Cyan-ish
    'CLICK_READY': (0, 255, 255), # Yellow
    'CLICKING': (0, 0, 255),   # Red
    'DRAGGING': (0, 0, 255),   # Red
    'SCROLLING': (255, 0, 255) # Purple
}
