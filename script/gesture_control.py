import cv2
from script.modules.tracker import HandTracker
from script.modules.media_and_brightness_control import MediaControl
from script.modules.app_control import AppControl
from script.modules.browser_control import BrowserControl
from script.modules.user_def_controls import UserDefControls
from script.modules.mouse_control import MouseControl


class GestureControl:
    def __init__(self, runFlag=True):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        self.hand_tracker = HandTracker()
        self.prev_gesture = None
        self.current_gesture = None
        self.mouse_control_active = False
        self.runFlag = runFlag

    def detect_gesture(self, raised_fingers):
        gestures = {
            (0, 0, 0, 0, 1): "thumb",
            (1, 0, 0, 0, 0): "little",
            (0, 0, 0, 1, 1): "thumb and index",
            (0, 0, 1, 1, 1): "thumb, index and middle",
            (0, 1, 1, 1, 1): "thumb, index, middle and ring",
            (0, 0, 0, 1, 0): "index",
            (0, 0, 1, 1, 0): "index and middle",
            (0, 1, 1, 1, 0): "index, middle and ring",
            (1, 1, 1, 1, 0): "index, middle, ring and little",
            (1, 1, 1, 1, 1): "all",
        }
        return gestures.get(tuple(raised_fingers))

    def run(self):
        while True:
            success, frame = self.cap.read()
            if not success or not self.runFlag:
                exit(0)
            frame = cv2.flip(frame, 1)
            results = self.hand_tracker.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    handedness = results.multi_handedness[0].classification[0].label
                    raised_fingers = self.hand_tracker.detect_raised_fingers(
                        hand_landmarks, handedness.lower(), self.mouse_control_active
                    )
                    if handedness.lower() == "left":
                        if raised_fingers is not None:
                            self.current_gesture = self.detect_gesture(raised_fingers)
                            if self.current_gesture and self.current_gesture != self.prev_gesture:
                                print(self.current_gesture)
                                self.prev_gesture = self.current_gesture

                    # volume control, gesture left: thumb
                    if handedness.lower() == "right" and self.current_gesture == "thumb":
                        volume_control = MediaControl(self.hand_tracker)
                        volume_control.control_volume(frame)

                    # brightness control, gesture left: thumb and index
                    if handedness.lower() == "right" and self.current_gesture == "thumb and index":
                        brightness_control = MediaControl(self.hand_tracker)
                        brightness_control.control_brightness(frame)

                    # media control, gesture left: thumb, index and middle
                    if (handedness.lower() == "right" and self.current_gesture == "thumb, index and middle"):
                        media_control = MediaControl(self.hand_tracker)
                        media_control.control_media(raised_fingers)

                    # app control, gesture left: index
                    if handedness.lower() == "right" and self.current_gesture == "index":
                        app_control = AppControl(self.hand_tracker)
                        app_control.window_nav(raised_fingers)

                    # browser control, gesture left: index and middle
                    if handedness.lower() == "right" and self.current_gesture == "index and middle":
                        browser_control = BrowserControl(self.hand_tracker)
                        browser_control.tab_nav(raised_fingers)

                    # mouse control, gesture left: index, middle and ring
                    if (handedness.lower() == "right" and self.current_gesture == "index, middle and ring"):
                        self.mouse_control_active = True
                        mouse_control = MouseControl(self.hand_tracker)
                        mouse_control.control_mouse(raised_fingers, frame)

                    else:
                        self.mouse_control_active = False

                    # user defined controls, gesture left: all
                    if handedness.lower() == "right" and self.current_gesture == "all":
                        user_def_controls = UserDefControls(self.hand_tracker)
                        user_def_controls.user_controls(raised_fingers)

            if not self.mouse_control_active:
                self.hand_tracker.frame_counter += 1

            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()