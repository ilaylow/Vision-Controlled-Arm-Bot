"""
This script utilises Google's Mediapipe Models to perform Real-Time Pose Detection.
Purely Experimental. 
"""

import cv2
import mediapipe 
import numpy as np

WRIST = 0
INDEX_TOP = 8
MIDDLE_TOP = 12
RING_TOP = 16

mp_drawing = mediapipe.solutions.drawing_utils
mp_drawing_styles = mediapipe.solutions.drawing_styles
mp_hands = mediapipe.solutions.hands

cap = cv2.VideoCapture(0)

def main():

    hands = mp_hands.Hands(max_num_hands=1,
    min_detection_confidence=0.5, min_tracking_confidence = 0.5) 

    while True:

        _, frame = cap.read()

        image_height, image_width, _ = frame.shape
        # Convert to RGB color space for model
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        hand_frame = np.zeros((image_height, image_width, 3))

        # We need to use a pivot point to determine the angle at which our arm is bent at
        try:

            mp_drawing.draw_landmarks(frame, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
            wrist_coords = results.multi_hand_landmarks[0].landmark[WRIST]
            index_coords = results.multi_hand_landmarks[0].landmark[INDEX_TOP]
            middle_coords = results.multi_hand_landmarks[0].landmark[MIDDLE_TOP]
            ring_coords = results.multi_hand_landmarks[0].landmark[RING_TOP]
            wrist_coords.z *= -151761.5608
            # Wrist z-coordinate is a bit strange being a factor of 151761.5608 smaller
            print(wrist_coords.z, index_coords.z, middle_coords.z, ring_coords.z)

            # Draw a circle on the four landmarks above and the color will indicate the depth (distance from camera)

            normalized_wrist_x = round(wrist_coords.x * frame.shape[1])
            normalized_wrist_y = round(wrist_coords.y * frame.shape[0])

            wrist_z_ratio = wrist_coords.z / -0.2
            wrist_z_ratio_comp = 1 - wrist_z_ratio 
            cv2.circle(frame, (normalized_wrist_x, normalized_wrist_y), 4, (round(wrist_z_ratio * 255), round(wrist_z_ratio_comp * 255), 255), 5)

        except:
            print("Error occured...")


        cv2.imshow("Frame", frame)
        cv2.imshow("Hand Movement", hand_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()

cap.release()
cv2.destroyAllWindows()