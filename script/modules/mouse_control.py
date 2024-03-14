import math
import platform
import pyautogui
import numpy as np


class MouseControl:
    def __init__(self, hand_tracker, frame):
        self.prev_x = 0
        self.prev_y = 0
        self.mouse = None
        self.hand_tracker = hand_tracker
        self.frame = frame
        self.os = platform.system()
        self.screen_width, self.screen_height = pyautogui.size()
        self.frame_width, self.frame_height = self.frame.shape[1], self.frame.shape[0]

        if self.os == "Windows":
            import mouse

            self.mouse = mouse

        elif self.os == "Darwin":
            import macmouse

            self.mouse = macmouse

    def control_mouse(self, raised_fingers, frame):
        landmarks = self.hand_tracker.find_position(frame)
        if raised_fingers == [0, 1, 1, 0, 0]:
            # DOESN'T WORk <- can't even type captial 'k'
            if landmarks is not None and len(landmarks) != 0:
                x1, y1 = landmarks[8][1], landmarks[8][2]
                x3 = np.interp(x1, (0, self.frame_width), (0, self.screen_width))
                y3 = np.interp(y1, (0, self.frame_height), (0, self.screen_height))

                c_loc_x = self.prev_x + (x3 - self.prev_x) / 5
                c_loc_y = self.prev_y + (y3 - self.prev_y) / 5
                self.mouse.move(self.screen_width - c_loc_x, c_loc_y)
                self.prev_x, self.prev_y = c_loc_x, c_loc_y

        # everything except thumb
        elif raised_fingers == [0, 1, 1, 1, 1]:
            # scroll up
            self.mouse.wheel(-3)

        # all fingers
        elif raised_fingers == [1, 1, 1, 1, 1]:
            # scroll down
            self.mouse.wheel(3)

        if (
            landmarks is not None
            and len(landmarks) != 0
            and (
                raised_fingers != [0, 1, 1, 0, 0]
                or raised_fingers != [0, 1, 1, 1, 1]
                or raised_fingers != [1, 1, 1, 1, 1]
            )
        ):
            # left click
            x1, y1 = landmarks[4][1], landmarks[4][2]
            x2, y2 = landmarks[8][1], landmarks[8][2]
            length = math.hypot(x2 - x1, y2 - y1)
            if length < 27:
                self.mouse.click("left")

            # right click
            x2, y2 = landmarks[12][1], landmarks[12][2]
            length = math.hypot(x2 - x1, y2 - y1)
            if length < 27:
                self.mouse.click("right")
