import math
import platform
import numpy as np
import pyautogui


class MouseControl:
    def __init__(self, hand_tracker):
        self.mouse = None
        self.hand_tracker = hand_tracker
        self.os = platform.system()
        self.screen_width, self.screen_height = pyautogui.size()
        self.w_cam, self.h_cam = 640, 480
        self.frame_r = 100
        self.p_loc_x, self.p_loc_y = 0, 0
        self.c_loc_x, self.c_loc_y = 0, 0

        if self.os == "Windows":
            import mouse

            self.mouse = mouse

        elif self.os == "Darwin":
            import macmouse

            self.mouse = macmouse

    def control_mouse(self, raised_fingers, frame):
        landmarks = self.hand_tracker.find_position(frame, True)
        if landmarks is not None and len(landmarks) != 0:
            if raised_fingers == [0, 1, 1, 0, 0]:
                if landmarks is not None and len(landmarks) != 0:
                    x1, y1 = landmarks[8][1:]
                    x2, y2 = landmarks[12][1:]
                    dx, dy = (x1 + x2) // 2, (y1 + y2) // 2
                    x3 = np.interp(
                        dx,
                        (self.frame_r, self.w_cam - self.frame_r),
                        (0, self.screen_width),
                    )
                    y3 = np.interp(
                        dy,
                        (self.frame_r, self.h_cam - self.frame_r),
                        (0, self.screen_height),
                    )
                    self.c_loc_x = self.p_loc_x + (x3 - self.p_loc_x) / 5
                    self.c_loc_y = self.p_loc_y + (y3 - self.p_loc_y) / 5
                    self.mouse.move(x3, y3)
                    self.p_loc_x, self.p_loc_y = self.c_loc_x, self.c_loc_y

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
