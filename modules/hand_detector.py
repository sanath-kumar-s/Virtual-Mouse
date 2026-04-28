import mediapipe as mp
import cv2
from config.settings import CONFIG

class HandDetector:
    def __init__(self, 
                 mode=False, 
                 max_hands=CONFIG['MAX_NUM_HANDS'], 
                 complexity=CONFIG['MODEL_COMPLEXITY'],
                 detection_con=CONFIG['MIN_DETECTION_CONFIDENCE'], 
                 track_con=CONFIG['MIN_TRACKING_CONFIDENCE']):
        
        self.mode = mode
        self.max_hands = max_hands
        self.complexity = complexity
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            model_complexity=self.complexity,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        """Processes the image and finds hands."""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks and draw:
            for hand_lms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def detect_hands(self, frame):
        """
        Detect hands and return separate left/right hand landmarks
        
        Returns:
            dict: {
                'left': {'landmarks': [...], 'handedness': 'Left', 'confidence': 0.9},
                'right': {'landmarks': [...], 'handedness': 'Right', 'confidence': 0.9}
            }
        """
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        detected_hands = {'left': None, 'right': None}
        
        if self.results.multi_hand_landmarks and self.results.multi_handedness:
            for hand_landmarks, handedness in zip(
                self.results.multi_hand_landmarks,
                self.results.multi_handedness
            ):
                # Get hand label ('Left' or 'Right')
                hand_label = handedness.classification[0].label
                confidence = handedness.classification[0].score
                
                # Store landmarks with handedness info
                hand_data = {
                    'landmarks': hand_landmarks.landmark, # Store the landmark list
                    'raw_landmarks': hand_landmarks,      # Store the full object for some utils
                    'handedness': hand_label,
                    'confidence': confidence
                }
                
                # Assign to correct hand
                if hand_label == 'Left':
                    detected_hands['left'] = hand_data
                elif hand_label == 'Right':
                    detected_hands['right'] = hand_data
        
        return detected_hands

    def find_position(self, img, hand_no=0):
        """Extracts landmark positions for a specific hand."""
        lm_list = []
        if self.results and self.results.multi_hand_landmarks and len(self.results.multi_hand_landmarks) > hand_no:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                # We return both normalized (0-1) and pixel coordinates
                lm_list.append({
                    'id': id,
                    'x': lm.x,
                    'y': lm.y,
                    'z': lm.z,
                    'px_x': int(lm.x * w),
                    'px_y': int(lm.y * h)
                })
        return lm_list

    def get_raw_landmarks(self, hand_no=0):
        """Returns the raw landmarks object from MediaPipe."""
        if self.results and self.results.multi_hand_landmarks and len(self.results.multi_hand_landmarks) > hand_no:
            return self.results.multi_hand_landmarks[hand_no].landmark
        return None

    def get_palm_center(self, hand_no=0):
        """Calculates the center of the palm based on specific landmarks."""
        if not self.results or not self.results.multi_hand_landmarks or len(self.results.multi_hand_landmarks) <= hand_no:
            return None
            
        my_hand = self.results.multi_hand_landmarks[hand_no]
        # Landmarks for palm: 0 (wrist), 5 (index MCP), 9 (middle MCP), 13 (ring MCP), 17 (pinky MCP)
        palm_indices = [0, 5, 9, 13, 17]
        
        avg_x = sum([my_hand.landmark[i].x for i in palm_indices]) / len(palm_indices)
        avg_y = sum([my_hand.landmark[i].y for i in palm_indices]) / len(palm_indices)
        
        return {'x': avg_x, 'y': avg_y}

    def get_hand_palm_center(self, landmarks):
        """Calculates palm center for a specific landmark list."""
        palm_indices = [0, 5, 9, 13, 17]
        avg_x = sum([landmarks[i].x for i in palm_indices]) / len(palm_indices)
        avg_y = sum([landmarks[i].y for i in palm_indices]) / len(palm_indices)
        return {'x': avg_x, 'y': avg_y}
