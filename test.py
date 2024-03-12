import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

prev_gesture = None
current_gesture = None

while True:
    try:
        success, frame = cap.read()
        if not success:
            break

        # Draw the rectangle on the frame
        w_cam, h_cam, frame_r = 640, 480, 100
        cv2.rectangle(
            frame,
            (frame_r, frame_r),
            (w_cam - frame_r, h_cam - frame_r),
            (255, 0, 255),
            2,
        )

        # Display the frame
        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    except Exception as e:
        print("error is: ", e.message)

cap.release()
cv2.destroyAllWindows()
