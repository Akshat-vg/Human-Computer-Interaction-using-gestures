import mediapipe as mp
import cv2
import numpy as np
import time

# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Initialize variables for flick detection
threshold_distance = 0.05  # Threshold distance for thumb-index finger proximity
threshold_flick_distance = 0.1  # Threshold distance for flick gesture
cooldown_time = 1.0  # Cooldown period in seconds
last_flick_time = 0

# Main loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)
    
    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        # Get landmarks of the detected hand
        landmarks = results.multi_hand_landmarks[0].landmark
        
        # Extract landmark coordinates for thumb and index finger
        thumb_coords = np.array([landmarks[4].x, landmarks[4].y, landmarks[4].z])  # Thumb tip landmark
        index_finger_coords = np.array([landmarks[8].x, landmarks[8].y, landmarks[8].z])  # Index finger tip landmark
        
        # Calculate distance between thumb and index finger landmarks
        thumb_index_distance = np.linalg.norm(thumb_coords - index_finger_coords)
        
        # Check if thumb and index finger are close together
        if thumb_index_distance < threshold_distance:
            # If cooldown period has elapsed
            if time.time() - last_flick_time > cooldown_time:
                # Calculate displacement between thumb and index finger landmarks
                displacement = thumb_coords - index_finger_coords
                
                # Normalize the displacement values
                normalized_displacement = displacement / np.linalg.norm(displacement)
                
                # Calculate Euclidean distance between normalized displacements
                flick_distance = np.linalg.norm(normalized_displacement)
                
                # If flick is detected
                if flick_distance > threshold_flick_distance:
                    # Perform scroll action here
                    print("Flick detected! Perform scroll action.")
                    
                    # Update last flick time
                    last_flick_time = time.time()
        
    # Display the frame
    cv2.imshow('Frame', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
