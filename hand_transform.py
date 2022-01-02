"""
This script utilises Google's Mediapipe Models to perform Real-Time Pose Detection.
Purely Experimental. 
"""
import Adeept
import cv2
import mediapipe 
import numpy as np
import math
from transcribe import pix_send1, pix_send2, pix_send3, pix_send4, pix_send5
import traceback

WRIST = 0
INDEX_TOP = 8
MIDDLE_TOP = 12
RING_TOP = 16

mp_drawing = mediapipe.solutions.drawing_utils
mp_drawing_styles = mediapipe.solutions.drawing_styles
mp_hands = mediapipe.solutions.hands

cap = cv2.VideoCapture(0)

def serial_connect():    #Call this function to connect with the server
    global ADDR,tcpClicSock,BUFSIZ,ip_stu,ipaddr,ser
    com="COM3"    #Get the IP address from Entry
    Adeept.com_init(com,115200,1)
    Adeept.wiat_connect()
    Adeept.three_function("'servo_attach'",0,9)
    Adeept.three_function("'servo_attach'",1,6)
    Adeept.three_function("'servo_attach'",2,5)
    Adeept.three_function("'servo_attach'",3,3)
    Adeept.three_function("'servo_attach'",4,11)
    print(com+':Success')

def main():

    hands = mp_hands.Hands(max_num_hands=1,
    min_detection_confidence=0.5, min_tracking_confidence = 0.5) 

    serial_connect()
    pix_send1(None, 90)
    pix_send2(None, 90)
    pix_send3(None, 90)
    pix_send4(None, 90)
    pix_send5(None, 65)

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
            #print(wrist_coords.z, index_coords.z, middle_coords.z, ring_coords.z)

            # Draw a circle on the four landmarks above and the color will indicate the depth (distance from camera)

            scaled_wrist_x = round(wrist_coords.x * frame.shape[1])
            scaled_wrist_y = round(wrist_coords.y * frame.shape[0])

            scaled_index_x = round(index_coords.x * frame.shape[1])
            scaled_index_y = round(index_coords.y * frame.shape[0])

            scaled_middle_x = round(middle_coords.x * frame.shape[1])
            scaled_middle_y = round(middle_coords.y * frame.shape[0])

            scaled_ring_x = round(ring_coords.x * frame.shape[1])
            scaled_ring_y = round(ring_coords.y * frame.shape[0])

            wrist_z_ratio = wrist_coords.z / -0.2
            wrist_z_comp = 1 - wrist_z_ratio 
            cv2.circle(frame, (scaled_wrist_x, scaled_wrist_y), 4, (255, round(wrist_z_ratio * 255), round(wrist_z_comp * 255)), 5)

            index_z_ratio = index_coords.z / -0.2
            index_z_comp = 1 - index_z_ratio
            cv2.circle(frame, (scaled_index_x, scaled_index_y), 4, (255, round(index_z_ratio * 255), round(index_z_comp * 255)), 5)

            # Let's draw a circle on the y coordinate of the wrist and x coordinate of index finger

            right_angle_point = (scaled_index_x, scaled_wrist_y)
            cv2.circle(frame, right_angle_point, 4, (0, 255, 0), 5)

            # Draw a line between circle to wrist and circle to index
            cv2.line(frame, right_angle_point, (scaled_index_x, scaled_index_y), (0, 0, 255), 2)
            cv2.line(frame, right_angle_point, (scaled_wrist_x, scaled_wrist_y), (0, 0, 255), 2)

            # Draw a line from wrist to index
            cv2.line(frame, (scaled_wrist_x, scaled_wrist_y), (scaled_index_x, scaled_index_y), (0, 0, 255), 2)

            # Use sin to calculate the angle between the wrist and the index
            # angle = arcsin(opp / hyp)
            opp = abs(round(scaled_wrist_y - scaled_index_y))
            hyp = abs(round(math.sqrt(opp**2 + round((scaled_wrist_x - scaled_index_x) ** 2))))

            angle = (math.asin(opp/hyp) * 180) / math.pi
            angle = round(angle, 2)

            if (scaled_index_y > scaled_wrist_y):
                new_angle = 90 + angle
            else:
                new_angle = 90 - angle
            
            pix_send3(None, round(new_angle))

            cv2.putText(frame, f"{angle} degrees", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

        except:
            traceback.print_exc()

        cv2.imshow("Frame", frame)
        cv2.imshow("Hand Movement", hand_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()

cap.release()
cv2.destroyAllWindows()