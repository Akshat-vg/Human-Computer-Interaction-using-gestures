from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from modules.tracker import HandTracker
import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
device_volume = interface.QueryInterface(IAudioEndpointVolume)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

hand_tracker = HandTracker()

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while True:
        success, image = cap.read()
        if not success:
            break
        image = cv2.flip(image, 1)
        results = hand_tracker.hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                handedness = results.multi_handedness[0].classification[0].label
                if(handedness.lower() == "right"):
                    # printing the distance between the thumb and the index finger

                    # thumb tip
                    x1, y1 = hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y

                    # index finger tip
                    x2, y2 = hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y

                    # middle knuckle
                    mkx, mky = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y

                    # wrist
                    wx, wy = hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y

                    tipLength = ((x2 - x1)**2 + (y2 - y1)**2)
                    palmLength = ((wx - mkx)**2 + (wy - mky)**2)
                    print("tip : " , tipLength, "\t palm : ", palmLength, "\t ratio : ", tipLength/palmLength)

                    # ratio >= 0.5 means the volume is full == 0.0
                    # ratio <= 0.2 means the volume is mute == -65.25

                    ratio = tipLength/palmLength
                    if ratio >= 1.7:
                        device_volume.SetMasterVolumeLevel(0.0, None)
                    elif ratio <= 0.15:
                        device_volume.SetMasterVolumeLevel(-65.25, None)
                    else:
                        volume = (ratio - 0.15) * (0.0 - (-65.25)) / (1.7 - 0.15) + (-65.25)
                        device_volume.SetMasterVolumeLevel(volume, None)
                    # volume = np.interp(ratio, [0.15, 1.7], [-65.25, 0.0])
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 'q':
            break   

cap.release()
            

