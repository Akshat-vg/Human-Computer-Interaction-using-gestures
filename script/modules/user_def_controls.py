import json
import subprocess


class UserDefControls:
    def __init__(self, hand_tracker):
        self.hand_tracker = hand_tracker

        with open("./script/modules/user_defined_data.json", "r") as file:
            self.app_data = json.load(file)

        self.gesture_map = {
            "[0, 1, 0, 0, 0]": "index",
            "[0, 1, 1, 0, 0]": "index and middle",
            "[0, 1, 1, 1, 0]": "index, middle and ring",
            "[0, 1, 1, 1, 1]": "index, middle, ring and little",
            "[1, 0, 0, 0, 0]": "thumb",
        }

    def user_controls(self, raised_fingers):
        if raised_fingers is not None and raised_fingers != [0, 0, 0, 0, 0]:
            if raised_fingers == [0, 1, 0, 0, 0]:
                subprocess.run(
                    self.app_data["userDefinedControls"][
                        self.gesture_map[str(raised_fingers)]
                    ],
                    shell=True,
                )

            elif raised_fingers == [0, 1, 1, 0, 0]:
                subprocess.run(
                    self.app_data["userDefinedControls"][
                        self.gesture_map[str(raised_fingers)]
                    ],
                    shell=True,
                )

            elif raised_fingers == [0, 1, 1, 1, 0]:
                subprocess.run(
                    self.app_data["userDefinedControls"][
                        self.gesture_map[str(raised_fingers)]
                    ],
                    shell=True,
                )

            elif raised_fingers == [0, 1, 1, 1, 1]:
                subprocess.run(
                    self.app_data["userDefinedControls"][
                        self.gesture_map[str(raised_fingers)]
                    ],
                    shell=True,
                )

            elif raised_fingers == [1, 0, 0, 0, 0]:
                subprocess.run(
                    self.app_data["userDefinedControls"][
                        self.gesture_map[str(raised_fingers)]
                    ],
                    shell=True,
                )
