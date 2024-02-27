import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2)
        self.mp_drawing = mp.solutions.drawing_utils
        self.frame_counter = 0
        self.cooldown_frames = 15
        self.smooth_cooldown_frames = 5

    def detect_raised_fingers(self, lst, hand_type):
        if self.frame_counter % self.cooldown_frames != 0:
            return None
        if hand_type not in ["left", "right"]:
            raise ValueError(
                "Invalid hand_type. It should be either 'left' or 'right'."
            )
        thresh = (lst.landmark[0].y * 100 - lst.landmark[9].y * 100) / 2
        finger_pairs = [(5, 8), (9, 12), (13, 16), (17, 20)]
        raised_fingers = [
            int(
                (lst.landmark[finger_tip].y * 100 - lst.landmark[knuckle].y * 100)
                > thresh
            )
            for finger_tip, knuckle in finger_pairs
        ]
        thumb_condition = (
            (lst.landmark[4].x * 100 - lst.landmark[5].x * 100) > 6
            if hand_type == "left"
            else (lst.landmark[5].x * 100 - lst.landmark[4].x * 100) > 6
        )
        raised_fingers.insert(0, int(thumb_condition))

        return raised_fingers[::-1] if hand_type == "left" else raised_fingers

    def detect_downwards_fingers(self, lst, hand_type):
        # this is not working as intended can someone fix
        if self.frame_counter % self.cooldown_frames != 0:
            return None
        if hand_type not in ["left", "right"]:
            raise ValueError(
                "Invalid hand_type. It should be either 'left' or 'right'."
            )
        thresh = (lst.landmark[0].y * 100 - lst.landmark[9].y * 100) / 2 + 5  # added a small constant to the threshold -> didn't do jackshit copilot
        finger_pairs = [(5, 8), (9, 12), (13, 16), (17, 20)]
        downwards_fingers = [
            int(
                (lst.landmark[finger_tip].y * 100 - lst.landmark[knuckle].y * 100)
                < thresh
            )
            for finger_tip, knuckle in finger_pairs
        ]

        print(downwards_fingers[::-1] if hand_type == "left" else downwards_fingers[1:])
        return downwards_fingers[::-1] if hand_type == "left" else downwards_fingers[1:]

    def find_position(self, frame):
        if self.frame_counter % self.smooth_cooldown_frames != 0:
            return None
        results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        landmarks = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmarks.append([id, cx, cy])
        return landmarks
