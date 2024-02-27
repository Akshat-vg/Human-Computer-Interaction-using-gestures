import pyautogui


class AppControl:
    def __init__(self, hand_tracker):
        self.hand_tracker = hand_tracker

    def window_nav(self, raised_fingers):
        if raised_fingers is not None:
            print(raised_fingers)
            if raised_fingers == [0, 0, 0, 0, 1]:
                pyautogui.hotkey("command", "tab")
            elif raised_fingers == [1, 0, 0, 0, 0]:
                pyautogui.hotkey("command", "shift", "tab")
            elif raised_fingers == [1, 1, 1, 1, 1]:
                pyautogui.hotkey("command", "m")
            elif raised_fingers == [0, 0, 0, 1, 1]:
                pyautogui.hotkey("command", "w")

    # time.sleep(0.5) -> this is slowing the the program a lot. Found alternative, there's no reason for this comment to exist so, can someone please make a commit "fix: fixed comment" for just this one line and nothing else, thanks much appreciated
