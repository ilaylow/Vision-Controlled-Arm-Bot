from os import stat
import numpy as np
import cv2

# Define ROI Regions
roi_lower_X = 15
roi_upper_X = 300

roi_lower_Y = 90
roi_upper_Y = 380

# Load external background subtractor
bg_subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

BLUR_RADIUS = 21
erode_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

class BackGroundSubtract:
    def __init__(self):
        return

    @staticmethod
    def read_initial_background(cap, use_roi = True):
        # Capture 10 frames and discard 9, we do this to allow adjustment of camera's autoexposure
        for i in range(10):
            success, frame = cap.read()
        if not success:
            exit(1)
        
        gray_og = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        """ print(gray_og)
        gray_og = (np.true_divide(gray_og, 0.7)).astype(np.uint8)
        print(gray_og) """
        gray_back = cv2.GaussianBlur(gray_og, (BLUR_RADIUS, BLUR_RADIUS), 0)

        if use_roi:
            return gray_back[roi_lower_Y: roi_upper_Y, roi_lower_X: roi_upper_X] 
        
        return gray_back

    @staticmethod
    def perform_background_subtraction(roi, background, use_external=True):

        if use_external:
            image_mask = bg_subtractor.apply(roi)

            # Threshold the difference
            ret, thresh = cv2.threshold(image_mask, 100, 255, cv2.THRESH_BINARY)
            
            # Perform Image Smoothing
            cv2.erode(thresh, erode_kernel, thresh, iterations = 2)
            cv2.dilate(thresh, dilate_kernel, thresh, iterations = 2)

            return image_mask, thresh

        else:

            # Get the absolute difference between the frame and the background
            print(roi.shape, background.shape)
            diff = cv2.absdiff(roi, background)

            # Threshold the difference
            ret, thresh = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)
            
            # Perform Image Smoothing
            cv2.erode(thresh, erode_kernel, thresh, iterations = 2)
            cv2.dilate(thresh, dilate_kernel, thresh, iterations = 4)

            return diff, thresh
