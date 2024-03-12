import math
import platform
import numpy as np
import autopy
import cv2


class MouseControl:
    def __init__(self, hand_tracker, frame):
        self.prev_x = 0
        self.prev_y = 0
        self.mouse = None
        self.scroll_mouse = None
        self.hand_tracker = hand_tracker
        self.frame = frame
        self.os = platform.system()
        self.screen_width, self.screen_height = autopy.screen.size()
        self.frame_width, self.frame_height = self.frame.shape[1], self.frame.shape[0]

        if self.os == "Windows":
            import mouse

            self.mouse = autopy.mouse
            self.scroll_mouse = mouse

        elif self.os == "Darwin":
            import macmouse

            self.mouse = macmouse

    def control_mouse(self, raised_fingers, frame):
        landmarks = self.hand_tracker.find_position(frame)
        if landmarks is not None and len(landmarks) != 0:
            w_cam, h_cam, frame_r = 640, 480, 100
            cv2.rectangle(
                frame,
                (frame_r, frame_r),
                (w_cam - frame_r, h_cam - frame_r),
                (255, 0, 255),
                2,
            )
            if raised_fingers == [0, 1, 1, 0, 0]:
                # DOESN'T WORk <- can't even type captial 'k'
                if landmarks is not None and len(landmarks) != 0:
                    x1, y1 = landmarks[8][1], landmarks[8][2]
                    x3 = np.interp(
                        x1, (frame_r, w_cam - frame_r), (0, self.screen_width)
                    )
                    y3 = np.interp(
                        y1, (frame_r, h_cam - frame_r), (0, self.screen_height)
                    )

                    c_loc_x = self.prev_x + (x3 - self.prev_x) / 5
                    c_loc_y = self.prev_y + (y3 - self.prev_y) / 5
                    self.mouse.move(self.screen_width - c_loc_x, c_loc_y)
                    self.prev_x, self.prev_y = c_loc_x, c_loc_y

            # everything except thumb
            elif raised_fingers == [0, 1, 1, 1, 1]:
                # scroll up
                self.scroll_mouse.wheel(-3)

            # all fingers
            elif raised_fingers == [1, 1, 1, 1, 1]:
                # scroll down
                self.scroll_mouse.wheel(3)

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
