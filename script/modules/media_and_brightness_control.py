import numpy as np
import math
import pyautogui
import platform


class MediaControl:
    def __init__(self, hand_tracker):
        self.hand_tracker = hand_tracker

    def control_volume(self, frame):
        landmarks = self.hand_tracker.find_position(frame)
        if landmarks is not None and len(landmarks) != 0:
            x1, y1 = landmarks[4][1], landmarks[4][2]
            x2, y2 = landmarks[8][1], landmarks[8][2]

            mkx, mky = landmarks[9][1], landmarks[9][2]
            wx, wy = landmarks[0][1], landmarks[0][2]

            tipLength = (x2 - x1) ** 2 + (y2 - y1) ** 2
            palmLength = (wx - mkx) ** 2 + (wy - mky) ** 2
            ratio = tipLength / palmLength

            if platform.system() == "Windows":
                volume = np.interp(ratio, [0.15, 1.0], [-65.25, 0.0])

                """
                The volume level is a float value between -65.25 and 0.0.
                                
                """
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(
                    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
                )
                device_volume = interface.QueryInterface(IAudioEndpointVolume)
                # print(volume, device_volume.GetMasterVolumeLevel())
                device_volume.SetMasterVolumeLevel(volume, None)

            elif platform.system() == "Darwin":
                import subprocess

                volume = np.interp(ratio, [0.15, 1.5], [0, 100])
                print(f"volume: {volume}")
                subprocess.run(
                    ["osascript", "-e", f"set volume output volume {volume}"]
                )

            else:
                # could have done it for linux, but don't have a linux machine to test
                raise NotImplementedError("This OS is not supported")

    def control_media(self, raised_fingers):
        # not working on darwin
        if raised_fingers is not None and raised_fingers != [0, 0, 0, 0, 0]:
            print(raised_fingers)
            if platform.system() == "Windows":
                # prev track, gesture: thumb
                if raised_fingers == [1, 0, 0, 0, 0]:
                    pyautogui.press("prevtrack")
                # next track, gesture: little
                elif raised_fingers == [0, 0, 0, 0, 1]:
                    pyautogui.press("nexttrack")
                # play/pause, gesture: all
                elif raised_fingers == [1, 1, 1, 1, 1]:
                    pyautogui.press("playpause")
                # volume mute, gesture: index, middle and ring
                elif raised_fingers == [0, 1, 1, 1, 0]:
                    pyautogui.press("volumemute")

            elif platform.system() == "Darwin":
                # could do it if found the key code for media keys
                pass

            else:
                # could have done it for linux, but don't have a linux machine to test
                raise NotImplementedError("This OS is not supported")

    def control_brightness(self, frame):
        landmarks = self.hand_tracker.find_position(frame)
        if landmarks is not None and len(landmarks) != 0:
            x1, y1 = landmarks[4][1], landmarks[4][2]
            x2, y2 = landmarks[8][1], landmarks[8][2]

            mkx, mky = landmarks[9][1], landmarks[9][2]
            wx, wy = landmarks[0][1], landmarks[0][2]

            tipLength = (x2 - x1) ** 2 + (y2 - y1) ** 2
            palmLength = (wx - mkx) ** 2 + (wy - mky) ** 2

            ratio = tipLength / palmLength

            if platform.system() == "Windows":
                import screen_brightness_control as sbc

                brightness = int(np.interp(ratio, [0.15, 1.5], [0, 100]))
                sbc.set_brightness(brightness)

            elif platform.system() == "Darwin":
                # this only works on apple silicon if you have the brightness cli tool, which should be built from source
                # link to repo: https://github.com/nriley/brightness
                import subprocess

                brightness = np.interp(ratio, [0.15, 1.5], [0, 1])
                print(f"brightness: {brightness}")
                subprocess.run(["brightness", str(brightness)])

            else:
                # could have done it for linux, but don't have a linux machine to test
                raise NotImplementedError("This OS is not supported")
