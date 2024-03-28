import platform
import pyautogui


class BrowserControl:
    def __init__(self, hand_tracker):
        self.hand_tracker = hand_tracker

    def tab_nav(self, raised_fingers):
        if raised_fingers is not None and raised_fingers != [0, 0, 0, 0, 0]:
            print(raised_fingers)
            if raised_fingers == [1, 0, 0, 0, 0]:
                # switch tab backward, gesture: thumb
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "shift", "[")
                elif platform.system() == "Windows":
                    pyautogui.hotkey("ctrl", "shift", "tab")
            elif raised_fingers == [0, 0, 0, 0, 1]:
                # switch tab forward, gesture: little
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "shift", "]")
                elif platform.system() == "Windows":
                    pyautogui.hotkey("ctrl", "tab")
            elif raised_fingers == [1, 1, 1, 1, 1]:
                # close tab, gesture: all
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "w")
                elif platform.system() == "Windows":
                    pyautogui.hotkey("ctrl", "w")
            elif raised_fingers == [0, 0, 0, 1, 1]:
                # new tab, gesture: ring and little
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "t")
                elif platform.system() == "Windows":
                    pyautogui.hotkey("ctrl", "t")
            elif raised_fingers == [0, 1, 0, 0, 1]:
                # reopen closed tab, gesture: index and little
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "shift", "t")
                elif platform.system() == "Windows":
                    pyautogui.hotkey("ctrl", "shift", "t")
            elif raised_fingers == [0, 1, 1, 1, 1]:
                # new window, gesture: index, middle, ring and little
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "n")
                elif platform.system() == "Windows":
                    pyautogui.hotkey("ctrl", "n")
