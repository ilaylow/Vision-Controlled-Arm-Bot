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
THUMB_TOP = 4
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
            thumb_coords = results.multi_hand_landmarks[0].landmark[THUMB_TOP]

            # Apply an odd scaling factor
            wrist_coords.z *= -151761.5608
            
            # Wrist z-coordinate is a bit strange being a factor of 151761.5608 smaller
            #print(wrist_coords.z, index_coords.z, middle_coords.z, ring_coords.z)

            # Draw a circle on the four landmarks above and the color will indicate the depth (distance from camera)

            scaled_wrist_x = round(wrist_coords.x * frame.shape[1])
            scaled_wrist_y = round(wrist_coords.y * frame.shape[0])
            scaled_wrist_z = round(wrist_coords.z * frame.shape[1])

            scaled_index_x = round(index_coords.x * frame.shape[1])
            scaled_index_y = round(index_coords.y * frame.shape[0])
            scaled_index_z = round(index_coords.z * frame.shape[1])

            scaled_middle_x = round(middle_coords.x * frame.shape[1])
            scaled_middle_y = round(middle_coords.y * frame.shape[0])
            scaled_middle_z = round(middle_coords.z * frame.shape[1])

            scaled_ring_x = round(ring_coords.x * frame.shape[1])
            scaled_ring_y = round(ring_coords.y * frame.shape[0])
            scaled_ring_z = round(ring_coords.z * frame.shape[1])

            scaled_thumb_x = round(thumb_coords.x * frame.shape[1])
            scaled_thumb_y = round(thumb_coords.y * frame.shape[0])
            scaled_thumb_z = round(thumb_coords.z * frame.shape[1])

            # Visualises depth (3rd dimension)
            wrist_z_ratio = wrist_coords.z / -0.2
            wrist_z_comp = 1 - wrist_z_ratio 
            cv2.circle(frame, (scaled_wrist_x, scaled_wrist_y), 4, (255, round(wrist_z_ratio * 255), round(wrist_z_comp * 255)), 5)

            index_z_ratio = index_coords.z / -0.2
            index_z_comp = 1 - index_z_ratio
            cv2.circle(frame, (scaled_index_x, scaled_index_y), 4, (255, round(index_z_ratio * 255), round(index_z_comp * 255)), 5)

            middle_z_ratio = middle_coords.z / -0.2
            middle_z_comp = 1 - middle_z_ratio
            cv2.circle(frame, (scaled_middle_x, scaled_middle_y), 4, (255, round(middle_z_ratio * 255), round(middle_z_comp * 255)), 5)

            ring_z_ratio = ring_coords.z / -0.2
            ring_z_comp = 1 - ring_z_ratio
            cv2.circle(frame, (scaled_ring_x, scaled_ring_y), 4, (255, round(ring_z_ratio * 255), round(ring_z_comp * 255)), 5)

            thumb_z_ratio = thumb_coords.z / -0.2
            thumb_z_comp = 1 - thumb_z_ratio
            cv2.circle(frame, (scaled_thumb_x, scaled_thumb_y), 4, (255, round(thumb_z_ratio * 255), round(thumb_z_comp * 255)), 5)

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

            new_angle = round(new_angle, 2)
            cv2.putText(frame, f"2D Angle: {new_angle} degrees", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)


            # 3D MAPPING STARTS HERE
            # Calculate the angle using 3d trigonometry to rotate the 3rd motor with direction of hand towards camera being invariant
             
            right_angle_point_3d = (scaled_index_x, scaled_wrist_y, scaled_index_z)

            # Calculate the distance between right angle point and wrist
            wrist_to_3d_point = math.dist(right_angle_point_3d, (scaled_wrist_x, scaled_wrist_y, scaled_wrist_z))

            # Distance between right angle point and index
            index_to_3d_point = math.dist(right_angle_point_3d, (scaled_index_x, scaled_index_y, scaled_index_z))

            hyp_3d = math.sqrt(wrist_to_3d_point**2 + index_to_3d_point**2)
            #print(right_angle_point_3d, index_coords.z)

            # Now get the angle between
            angle_3d = (math.asin(index_to_3d_point/hyp_3d) * 180) / math.pi
            #print(angle_3d)
            if (scaled_index_y > scaled_wrist_y):
                new_angle_3d = 90 + angle_3d
            else:
                new_angle_3d = 90 - angle_3d

            pix_send3(None, round(new_angle_3d))
            pix_send4(None, 90)

            # Implement In grabbing

            # Use the idea of obtaining the average coordinate of the 3 fingers (index, middle and ring) and then use the average
            # to calculate the distance between the thumb
            # Translate this distance into angle of the grabbing motor

            # First obtain the average of the three fingers
            average_x_fingers = (scaled_index_x + scaled_middle_x + scaled_ring_x) / 3
            average_y_fingers = (scaled_index_y + scaled_middle_y + scaled_ring_y) / 3
            average_z_fingers = (scaled_index_z + scaled_middle_z + scaled_ring_z) / 3

            dist_finger_thumb = math.dist((scaled_thumb_x, scaled_thumb_y, scaled_thumb_z), (average_x_fingers, average_y_fingers, average_z_fingers))
            print(dist_finger_thumb)

            # Now we map this distance to the angle of rotation of the hand (motor 5) 
            # Establish maximums and minimums for distances

            dist_normalized_value = abs(dist_finger_thumb - 18) / (130 - 18)
            
            dist_normalized_value = min(1, dist_normalized_value) # Establishes that the normalized value cannot exceed beyond range
            dist_normalized_value = max(0, dist_normalized_value) # As maximum and minimum and arbitarily chosen from observation

            angle_scaled_value = 130 - ((dist_normalized_value * 70) + 30)
            #pix_send5(None, round(angle_scaled_value))
            

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