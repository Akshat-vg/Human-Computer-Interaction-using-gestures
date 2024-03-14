import unittest
from unittest.mock import patch
import os
import sys

import pyautogui

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from modules.browser_control import BrowserControl


class TestBrowserControl(unittest.TestCase):
    def setUp(self):
        self.browser_control = BrowserControl(hand_tracker=None)

        # Mock the platform.system() function
        self.platform_patch = patch("platform.system", return_value="Darwin")
        self.mock_platform = self.platform_patch.start()

    def tearDown(self):
        self.platform_patch.stop()

    def test_tab_nav_switch_tab_backward_mac(self):
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.browser_control.tab_nav([1, 0, 0, 0, 0])
            mock_hotkey.assert_called_with("command", "shift", "[")
            print(
                f"test_tab_nav_switch_tab_backward_mac: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_tab_nav_switch_tab_backward_windows(self):
        self.mock_platform.return_value = "Windows"
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.browser_control.tab_nav([1, 0, 0, 0, 0])
            mock_hotkey.assert_called_with("ctrl", "shift", "tab")
            print(
                f"test_tab_nav_switch_tab_backward_windows: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_tab_nav_switch_tab_forward_mac(self):
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.browser_control.tab_nav([0, 0, 0, 0, 1])
            mock_hotkey.assert_called_with("command", "shift", "]")
            print(
                f"test_tab_nav_switch_tab_forward_mac: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_tab_nav_switch_tab_forward_windows(self):
        self.mock_platform.return_value = "Windows"
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.browser_control.tab_nav([0, 0, 0, 0, 1])
            mock_hotkey.assert_called_with("ctrl", "tab")
            print(
                f"test_tab_nav_switch_tab_forward_windows: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_tab_nav_close_tab_mac(self):
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.browser_control.tab_nav([1, 1, 1, 1, 1])
            mock_hotkey.assert_called_with("command", "w")
            print(
                f"test_tab_nav_close_tab_mac: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_tab_nav_close_tab_windows(self):
        self.mock_platform.return_value = "Windows"
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.browser_control.tab_nav([1, 1, 1, 1, 1])
            mock_hotkey.assert_called_with("ctrl", "w")
            print(
                f"test_tab_nav_close_tab_windows: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_tab_nav_new_tab_mac(self):
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.browser_control.tab_nav([0, 0, 0, 1, 1])
            mock_hotkey.assert_called_with("command", "t")
            print(
                f"test_tab_nav_new_tab_mac: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_tab_nav_new_tab_windows(self):
        self.mock_platform.return_value = "Windows"
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.browser_control.tab_nav([0, 0, 0, 1, 1])
            mock_hotkey.assert_called_with("ctrl", "t")
            print(
                f"test_tab_nav_new_tab_windows: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_tab_nav_reopen_closed_tab_mac(self):
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.browser_control.tab_nav([0, 1, 0, 0, 1])
            mock_hotkey.assert_called_with("command", "shift", "t")
            print(
                f"test_tab_nav_reopen_closed_tab_mac: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_tab_nav_reopen_closed_tab_windows(self):
        self.mock_platform.return_value = "Windows"
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.browser_control.tab_nav([0, 1, 0, 0, 1])
            mock_hotkey.assert_called_with("ctrl", "shift", "t")
            print(
                f"test_tab_nav_reopen_closed_tab_windows: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_tab_nav_new_window_mac(self):
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.browser_control.tab_nav([0, 1, 1, 1, 1])
            mock_hotkey.assert_called_with("command", "n")
            print(
                f"test_tab_nav_new_window_mac: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )

    def test_tab_nav_new_window_windows(self):
        self.mock_platform.return_value = "Windows"
        with patch.object(pyautogui, "hotkey") as mock_hotkey:
            self.browser_control.tab_nav([0, 1, 1, 1, 1])
            mock_hotkey.assert_called_with("ctrl", "n")
            print(
                f"test_tab_nav_new_window_windows: {'PASSED' if mock_hotkey.called else 'FAILED'}"
            )


if __name__ == "__main__":
    unittest.main()
