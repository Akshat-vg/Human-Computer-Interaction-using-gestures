import platform
import pyautogui


class AppControl:
    def __init__(self, hand_tracker):
        self.hand_tracker = hand_tracker

    def window_nav(self, raised_fingers):
        if raised_fingers is not None and raised_fingers != [0, 0, 0, 0, 0]:
            print(raised_fingers)
            if raised_fingers == [0, 0, 0, 0, 1]:
                # switch window forward, gesture: little
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "tab")
                elif platform.system() == "Windows":
                    pyautogui.hotkey("alt", "tab")
            elif raised_fingers == [1, 0, 0, 0, 0]:
                # switch window backward, gesture: thumb
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "shift", "tab")
                elif platform.system() == "Windows":
                    pyautogui.hotkey("alt", "shift", "tab")
            elif raised_fingers == [1, 1, 1, 1, 1]:
                # minimize window, gesture: all
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "m")
                elif platform.system() == "Windows":
                    pyautogui.hotkey("win", "m")
            elif raised_fingers == [0, 0, 0, 1, 1]:
                # close window, gesture: ring and little
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "w")
                elif platform.system() == "Windows":
                    pyautogui.hotkey("alt", "f4")
            elif raised_fingers == [0, 1, 0, 0, 1]:
                # switch window(same application different windows) forward, gesture: index and little
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "`")
                elif platform.system() == "Windows":
                    pyautogui.hotkey("alt", "esc")
            elif raised_fingers == [0, 1, 1, 1, 1]:
                # close a window of the application, gesture: index, middle, ring and little
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "w")
                elif platform.system() == "Windows":
                    pyautogui.hotkey("ctrl", "w")
