import unittest
from unittest.mock import patch
import os
import sys

import pyautogui

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "script"))
)

from modules.app_control import AppControl


class TestAppControl(unittest.TestCase):
    def setUp(self):
        self.app_control = AppControl(hand_tracker=None)

        # Mock the platform.system() function
        self.platform_patch = patch("platform.system", return_value="Darwin")
        self.mock_platform = self.platform_patch.start()

    def tearDown(self):
        self.platform_patch.stop()

    def test_window_nav_switch_window_forward_mac(self):
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.app_control.window_nav([0, 0, 0, 0, 1])
            mock_hotkey.assert_called_with("command", "tab")
            print(
                f"test_window_nav_switch_window_forward_mac: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_window_nav_switch_window_forward_windows(self):
        self.mock_platform.return_value = "Windows"
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.app_control.window_nav([0, 0, 0, 0, 1])
            mock_hotkey.assert_called_with("alt", "tab")
            print(
                f"test_window_nav_switch_window_forward_windows: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_window_nav_switch_window_backward_mac(self):
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.app_control.window_nav([1, 0, 0, 0, 0])
            mock_hotkey.assert_called_with("command", "shift", "tab")
            print(
                f"test_window_nav_switch_window_backward_mac: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_window_nav_switch_window_backward_windows(self):
        self.mock_platform.return_value = "Windows"
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.app_control.window_nav([1, 0, 0, 0, 0])
            mock_hotkey.assert_called_with("alt", "shift", "tab")
            print(
                f"test_window_nav_switch_window_backward_windows: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_window_nav_minimize_window_mac(self):
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.app_control.window_nav([1, 1, 1, 1, 1])
            mock_hotkey.assert_called_with("command", "m")
            print(
                f"test_window_nav_minimize_window_mac: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_window_nav_minimize_window_windows(self):
        self.mock_platform.return_value = "Windows"
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.app_control.window_nav([1, 1, 1, 1, 1])
            mock_hotkey.assert_called_with("win", "m")
            print(
                f"test_window_nav_minimize_window_windows: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_window_nav_close_window_mac(self):
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.app_control.window_nav([0, 0, 0, 1, 1])
            mock_hotkey.assert_called_with("command", "w")
            print(
                f"test_window_nav_close_window_mac: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_window_nav_close_window_windows(self):
        self.mock_platform.return_value = "Windows"
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.app_control.window_nav([0, 0, 0, 1, 1])
            mock_hotkey.assert_called_with("alt", "fn", "f4")
            print(
                f"test_window_nav_close_window_windows: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_window_nav_switch_window_same_app_forward_mac(self):
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.app_control.window_nav([0, 1, 0, 0, 1])
            mock_hotkey.assert_called_with("command", "`")
            print(
                f"test_window_nav_switch_window_same_app_forward_mac: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_window_nav_switch_window_same_app_forward_windows(self):
        self.mock_platform.return_value = "Windows"
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.app_control.window_nav([0, 1, 0, 0, 1])
            mock_hotkey.assert_called_with("alt", "esc")
            print(
                f"test_window_nav_switch_window_same_app_forward_windows: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_window_nav_close_app_window_mac(self):
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.app_control.window_nav([0, 1, 1, 1, 1])
            mock_hotkey.assert_called_with("command", "w")
            print(
                f"test_window_nav_close_app_window_mac: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_window_nav_close_app_window_windows(self):
        self.mock_platform.return_value = "Windows"
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.app_control.window_nav([0, 1, 1, 1, 1])
            mock_hotkey.assert_called_with("ctrl", "w")
            print(
                f"test_window_nav_close_app_window_windows: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )


if __name__ == "__main__":
    unittest.main()
