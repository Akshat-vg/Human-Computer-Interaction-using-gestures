import json
import subprocess


class UserDefControls:
    def __init__(self, hand_tracker):
        self.hand_tracker = hand_tracker
        with open("./user_data.json", "r") as file:
            self.app_data = json.load(file)

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

        self.gesture_map = {
            "index": [0, 1, 0, 0, 0],
            "index and middle": [0, 1, 1, 0, 0],
            "index, middle and ring": [0, 1, 1, 1, 0],
            "index, middle, ring and little": [0, 1, 1, 1, 1],
            "thumb": [1, 0, 0, 0, 0],
        }

    def user_controls(self, raised_fingers):
        for gesture, shellName in self.app_data["userDefinedControls"].items():
            if self.gesture_map[gesture] == raised_fingers:
                for app in self.data:
                    if app["displayName"] == shellName:
                        subprocess.run(app["shellName"], shell=True)
                        break
