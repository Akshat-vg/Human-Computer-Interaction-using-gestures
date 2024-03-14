import unittest
from unittest.mock import patch
import os
import sys

import pyautogui
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from modules.media_and_brightness_control import MediaControl


class TestMediaControl(unittest.TestCase):
    def setUp(self):
        self.hand_tracker = unittest.mock.Mock()
        self.hand_tracker.find_position = unittest.mock.Mock(return_value=...)
        self.media_control = MediaControl(hand_tracker=self.hand_tracker)
        # Mock the platform.system() function
        self.platform_patch = patch("platform.system", return_value="Darwin")
        self.mock_platform = self.platform_patch.start()

    def tearDown(self):
        self.platform_patch.stop()

    def test_control_volume_windows(self):
        self.mock_platform.return_value = "Windows"
        with patch.object(pyautogui, "press") as mock_press:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            self.media_control.control_volume(frame)
            mock_press.assert_called_with("volumemute")
            print(
                f"test_control_volume_windows: {'PASSED' if mock_press.called else 'FAILED'}"
            )

    def test_control_volume_darwin(self):
        self.mock_platform.return_value = "Darwin"
        with patch.object(pyautogui, "press") as mock_press:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            self.media_control.control_volume(frame)
            mock_press.assert_not_called()
            print(
                f"test_control_volume_darwin: {'PASSED' if not mock_press.called else 'FAILED'}"
            )

    def test_control_media_windows(self):
        self.mock_platform.return_value = "Windows"
        with patch.object(pyautogui, "press") as mock_press:
            self.media_control.control_media([1, 0, 0, 0, 0])
            mock_press.assert_called_with("prevtrack")
            print(
                f"test_control_media_windows: {'PASSED' if mock_press.called else 'FAILED'}"
            )

    def test_control_media_darwin(self):
        self.mock_platform.return_value = "Darwin"
        with patch.object(pyautogui, "press") as mock_press:
            self.media_control.control_media([1, 0, 0, 0, 0])
            mock_press.assert_not_called()
            print(
                f"test_control_media_darwin: {'PASSED' if not mock_press.called else 'FAILED'}"
            )

    def test_control_brightness_windows(self):
        self.mock_platform.return_value = "Windows"
        with patch(
            "modules.media_and_brightness_control.screen_brightness_control.set_brightness"
        ) as mock_set_brightness:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            self.media_control.control_brightness(frame)
            mock_set_brightness.assert_called()
            print(
                f"test_control_brightness_windows: {'PASSED' if mock_set_brightness.called else 'FAILED'}"
            )

    def test_control_brightness_darwin(self):
        self.mock_platform.return_value = "Darwin"
        with patch.object(os, "system") as mock_system:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            self.media_control.control_brightness(frame)
            mock_system.assert_called_with(["brightness", str(0)])
            print(
                f"test_control_brightness_darwin: {'PASSED' if mock_system.called else 'FAILED'}"
            )


if __name__ == "__main__":
    unittest.main()
