import subprocess

import pyautogui


class UserDefControls:
    def __init__(self, hand_tracker):
        self.hand_tracker = hand_tracker
        self.data = [
            {
                "displayName": "Explorer",
                "shellName": ["explorer.exe", "microsoft.windows.camera:"],
            },
            {"displayName": "Calculator", "shellName": ["calc.exe"]},
            {"displayName": "Notepad", "shellName": ["notepad.exe"]},
            {"displayName": "Settings", "shellName": ["explorer.exe", "ms-settings:"]},
            {
                "displayName": "Photos",
                "shellName": ["explorer.exe", "microsoft.windows.photos:"],
            },
        ]


def user_controls(self, raised_fingers):
    if raised_fingers is not None and raised_fingers != [0, 0, 0, 0, 0]:
        # gesture 1: index
        if raised_fingers == [0, 1, 0, 0, 0]:
            subprocess.run(self.data[0]["shellName"], shell=True)
        # gesture 2: index and middle
        elif raised_fingers == [0, 1, 1, 0, 0]:
            subprocess.run(self.data[1]["shellName"], shell=True)
        # gesture 3: index, middle and ring
        elif raised_fingers == [0, 1, 1, 1, 0]:
            subprocess.run(self.data[2]["shellName"], shell=True)
        # gesture 4: index, middle, ring and little
        elif raised_fingers == [0, 1, 1, 1, 1]:
            subprocess.run(self.data[3]["shellName"], shell=True)
        # gesture 5: thumb
        elif raised_fingers == [1, 0, 0, 0, 0]:
            subprocess.run(self.data[4]["shellName"], shell=True)
