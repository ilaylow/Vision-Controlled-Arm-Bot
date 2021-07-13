# Addition of this code is the property of Chuen Ley low
# The following code attempts to perform a mapping of a humans hand to the Adeept Robotic Arm Kit

import cv2
import numpy as np
import random

from BackgroundSubtractor import BackGroundSubtract
from BackgroundSubtractor import BLUR_RADIUS, roi_lower_X, roi_lower_Y, roi_upper_X, roi_upper_Y

font = cv2.FONT_HERSHEY_SIMPLEX

cap = cv2.VideoCapture(0)

gray_background = BackGroundSubtract.read_initial_background(cap, use_roi=False)

def main():

    while True:
        _, frame =  cap.read()

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff, img_thresh = BackGroundSubtract.perform_background_subtraction(gray_frame, gray_background, use_external=False)
        
        contours, _ = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) != 0:
        
            max_contour = max(contours, key = cv2.contourArea)   
            hulls = [cv2.convexHull(contour) for contour in contours]
            max_hull = max(hulls, key = cv2.contourArea)

            cv2.drawContours(frame, max_contour, -1, (0, 255, 0))
            cv2.drawContours(frame, [max_hull], -1, (255, 0, 0))
        
        # Show the different video streams
        cv2.imshow("Img Thresh", img_thresh)
        cv2.imshow("Original Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if cv2.waitKey(1) & 0xFF == ord('t'):
            background = BackGroundSubtract.read_initial_background(cap, use_roi=False)


if __name__ == "__main__":
    main()