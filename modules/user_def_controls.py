import pyautogui

class UserDefControls:
    def __init__(self, hand_tracker):
        self.hand_tracker = hand_tracker

    def volume_control(self, raised_fingers):
        if raised_fingers is not None and raised_fingers != [0, 0, 0, 0, 0]:
            # gesture 1: index
            if raised_fingers == [0, 1, 0, 0, 0]:
                pass
            # gesture 2: index and middle
            elif raised_fingers == [0, 1, 1, 0, 0]:
                pass
            # gesture 3: index, middle and ring
            elif raised_fingers == [0, 1, 1, 1, 0]:
                pass
            # gesture 4: index, middle, ring and little
            elif raised_fingers == [0, 1, 1, 1, 1]:
                pass
            # gesture 5: thumb
            elif raised_fingers == [1, 0, 0, 0, 0]:
                pass