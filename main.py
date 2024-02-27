import cv2
import modules.tracker as tr
from modules.media_control import MediaControl
from modules.app_control import AppControl


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

hand_tracker = tr.HandTracker()

prev_gesture = None
current_gesture = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
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

            if handedness.lower() == "right" and current_gesture == "thumb":
                volume_control = MediaControl(hand_tracker)
                frame = volume_control.control_volume(frame)

            if handedness.lower() == "right" and current_gesture == "index":
                app_control = AppControl(hand_tracker)
                app_control.window_nav(raised_fingers)

    hand_tracker.frame_counter += 1

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
