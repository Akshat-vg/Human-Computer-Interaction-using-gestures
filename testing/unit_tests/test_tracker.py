import unittest
from unittest.mock import patch
import os
import sys
import cv2
import mediapipe as mp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from modules.tracker import HandTracker


class TestHandTracker(unittest.TestCase):
    def setUp(self):
        self.hand_tracker = HandTracker()

    def test_detect_raised_fingers_left_hand(self):
        lst = mp.solutions.hands.Hands().process(cv2.imread("left_hand.jpg"))
        raised_fingers = self.hand_tracker.detect_raised_fingers(lst, "left")
        self.assertEqual(raised_fingers, [1, 1, 1, 1, 1])

    def test_detect_raised_fingers_right_hand(self):
        lst = mp.solutions.hands.Hands().process(cv2.imread("right_hand.jpg"))
        raised_fingers = self.hand_tracker.detect_raised_fingers(lst, "right")
        self.assertEqual(raised_fingers, [1, 1, 1, 1, 1])

    def test_find_position(self):
        frame = cv2.imread("frame.jpg")
        landmarks = self.hand_tracker.find_position(frame)
        self.assertIsNotNone(landmarks)
        self.assertIsInstance(landmarks, list)
        self.assertGreater(len(landmarks), 0)


if __name__ == "__main__":
    unittest.main()
