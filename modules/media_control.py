import numpy as np
import math


class MediaControl:
    def __init__(self, hand_tracker):
        self.hand_tracker = hand_tracker

    def control_volume(self, frame):
        landmarks = self.hand_tracker.find_position(frame)
        if landmarks is not None and len(landmarks) != 0:
            x1, y1 = landmarks[4][1], landmarks[4][2]
            x2, y2 = landmarks[8][1], landmarks[8][2]
            length = math.hypot(x2 - x1, y2 - y1)

            volume = np.interp(length, [50, 300], [0, 100])
            print(int(volume))
        return frame
