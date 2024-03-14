import cv2
from modules.tracker import HandTracker
from modules.media_and_brightness_control import MediaControl
from modules.app_control import AppControl
from modules.browser_control import BrowserControl
from modules.user_def_controls import UserDefControls
from modules.mouse_control import MouseControl


def detect_gesture(raised_fingers):
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


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

hand_tracker = HandTracker()

prev_gesture = None
current_gesture = None

while True:
    success, frame = cap.read()
    if not success:
        break
    frame = cv2.flip(frame, 1)
    results = hand_tracker.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            handedness = results.multi_handedness[0].classification[0].label

            raised_fingers = hand_tracker.detect_raised_fingers(
                hand_landmarks, handedness.lower()
            )

            if handedness.lower() == "left":
                if raised_fingers is not None:
                    current_gesture = detect_gesture(raised_fingers)
                    if current_gesture and current_gesture != prev_gesture:
                        print(current_gesture)
                        prev_gesture = current_gesture

            # volume control, gesture left: thumb
            if handedness.lower() == "right" and current_gesture == "thumb":
                volume_control = MediaControl(hand_tracker)
                volume_control.control_volume(frame)

            # brightness control, gesture left: thumb and index
            if handedness.lower() == "right" and current_gesture == "thumb and index":
                brightness_control = MediaControl(hand_tracker)
                brightness_control.control_brightness(frame)

            # media control, gesture left: thumb, index and middle
            if (
                handedness.lower() == "right"
                and current_gesture == "thumb, index and middle"
            ):
                media_control = MediaControl(hand_tracker)
                media_control.control_media(raised_fingers)

            # app control, gesture left: index
            if handedness.lower() == "right" and current_gesture == "index":
                app_control = AppControl(hand_tracker)
                app_control.window_nav(raised_fingers)

            # browser control, gesture left: index and middle
            if handedness.lower() == "right" and current_gesture == "index and middle":
                browser_control = BrowserControl(hand_tracker)
                browser_control.tab_nav(raised_fingers)

            # mouse control, gesture left: index, middle and ring
            if (
                handedness.lower() == "right"
                and current_gesture == "index, middle and ring"
            ):
                mouse_control = MouseControl(hand_tracker, frame)
                mouse_control.control_mouse(raised_fingers, frame)

            # user defined controls, gesture left: all
            if handedness.lower() == "right" and current_gesture == "all":
                user_def_controls = UserDefControls(hand_tracker)
                user_def_controls.volume_control(raised_fingers)

    hand_tracker.frame_counter += 1

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
