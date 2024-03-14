import cv2
import mediapipe as mp
import time
import math


class hand_detector:
    def __init__(
        self,
        mode=False,
        max_hands=2,
        detection_con=0.5,
        model_complexity=1,
        track_con=0.5,
    ):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.model_complex = model_complexity
        self.track_con = track_con
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            self.mode,
            self.max_hands,
            self.model_complex,
            self.detection_con,
            self.track_con,
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]
        self.results = []

    def find_hands(self, img, draw=False):
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_RGB)
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        img, hand_lms, self.mp_hands.HAND_CONNECTIONS
                    )
        return img

    def find_position(self, img, hand_no=0, draw=False):
        x_list = []
        y_list = []
        b_box = []
        self.lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                x_list.append(cx)
                y_list.append(cy)
                self.lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            x_min, x_max = min(x_list), max(x_list)
            y_min, y_max = min(y_list), max(y_list)
            b_box = x_min, y_min, x_max, y_max
            if draw:
                cv2.rectangle(
                    img,
                    (x_min - 20, y_min - 20),
                    (x_max + 20, y_max + 20),
                    (0, 255, 0),
                    2,
                )
        return self.lm_list, b_box

    def fingers_up(self):
        fingers = []
        if self.lm_list[self.tip_ids[0]][1] > self.lm_list[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1, 5):
            if (
                self.lm_list[self.tip_ids[id]][2]
                < self.lm_list[self.tip_ids[id] - 2][2]
            ):
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def find_distance(self, p1, p2, img, draw=True, r=10, t=2):
        # p1=4, p2=8
        x1, y1 = self.lm_list[p1][1], self.lm_list[p1][2]
        x2, y2 = self.lm_list[p2][1], self.lm_list[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]


def main():
    p_time = 0
    c_time = 0
    cap = cv2.VideoCapture(0)
    detector = hand_detector()
    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        lm_list, b_box = detector.find_position(img)
        # if len(lm_list) != 0:
        #     print(lm_list[4])
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time
        cv2.putText(
            img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3
        )
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


if __name__ == "__main__":
    main()
