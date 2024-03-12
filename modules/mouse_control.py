import math
import platform
import numpy as np
import modules.hand_tracking_module as htm
import autopy
import cv2


class MouseControl:
    def __init__(self, hand_tracker, frame):
        self.mouse = None
        self.click_mouse = None
        self.hand_tracker = hand_tracker
        self.frame = frame
        self.os = platform.system()
        self.screen_width, self.screen_height = autopy.screen.size()
        self.w_cam, self.h_cam = 640, 480
        self.frame_r = 100
        self.p_loc_x, self.p_loc_y = 0, 0
        self.c_loc_x, self.c_loc_y = 0, 0
        self.detector = htm.hand_detector(max_hands=1)

        if self.os == "Windows":
            import mouse

            self.click_mouse = autopy.mouse
            self.mouse = mouse

        elif self.os == "Darwin":
            import macmouse

            self.click_mouse = macmouse
            self.mouse = macmouse

    def control_mouse(self, raised_fingers, frame):
        try:
            # landmarks = self.hand_tracker.find_position(frame)
            frame = self.detector.find_hands(frame)
            landmarks, _ = self.detector.find_position(frame)
            if landmarks is not None and len(landmarks) != 0:
                # print(f"landmarks: {landmarks}")
                cv2.rectangle(
                    frame,
                    (self.frame_r, self.frame_r),
                    (self.w_cam - self.frame_r, self.h_cam - self.frame_r),
                    (255, 0, 255),
                    2,
                )
                if raised_fingers == [0, 1, 1, 0, 0]:
                    if landmarks is not None and len(landmarks) != 0:
                        x1, y1 = landmarks[8][1:]
                        print(f"X1: {x1} and Y1: {y1}")
                        x3 = np.interp(
                            x1,
                            (self.frame_r, self.w_cam - self.frame_r),
                            (0, self.screen_width),
                        )
                        y3 = np.interp(
                            y1,
                            (self.frame_r, self.h_cam - self.frame_r),
                            (0, self.screen_height),
                        )
                        self.c_loc_x = self.p_loc_x + (x3 - self.p_loc_x) / 5
                        self.c_loc_y = self.p_loc_y + (y3 - self.p_loc_y) / 5
                        autopy.mouse.move(
                            self.screen_width - self.c_loc_x, self.c_loc_y
                        )
                        self.p_loc_x, self.p_loc_y = self.c_loc_x, self.c_loc_y
                        cv2.circle(
                            frame,
                            (self.w_cam // 2, self.h_cam // 2),
                            15,
                            (255, 0, 255),
                            cv2.FILLED,
                        )
                        if x1 == self.w_cam / 2 and y1 == self.h_cam / 2:
                            print("You are at the centre of the screen")
                            print(f"X: {x1} and Y: {y1}")
                            exit()

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

        except Exception as e:
            print(f"Error in control_mouse: {e}")
