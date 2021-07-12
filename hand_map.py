# Addition of this code is the property of Chuen Ley low
# The following code attempts to perform a mapping of a humans hand to the Adeept Robotic Arm Kit

import cv2
import numpy as np
import random

from BackgroundSubtractor import BackGroundSubtract
from BackgroundSubtractor import BLUR_RADIUS, roi_lower_X, roi_lower_Y, roi_upper_X, roi_upper_Y

font = cv2.FONT_HERSHEY_SIMPLEX

cap = cv2.VideoCapture(0)

def main():

    while True:
        _, frame =  cap.read()

        

        cv2.imshow("Original Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    main()