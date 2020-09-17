#Source Reference https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/
#Import packages
import numpy as np
import cv2
import argparse

#Lower and upper bound values for colours 
boundaries = {
				'red': ([162, 99, 72], [183, 187, 203]),
				'black': ([0, 0, 0], [121, 52, 50]),
				'white':([0, 0, 178], [13, 25, 253]),
				'blue':([83,43,127], [126,94,255]),
				'silver':([119,0,114], [255,21,255])
				}
				
#Method to detect colour of the car classifier
def colordetection(image):
	#hsv color code format			
	hsv_range = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
	max= 0	
	for key, value in boundaries.items():
		lower = np.array(value[0], dtype = "uint8")
		upper = np.array(value[1], dtype = "uint8")
		masked_values = cv2.inRange(hsv_range, lower, upper)
		pixels = np.sum(masked_values)
		if (max < pixels):
			max = pixels
			detected_colour = key
	return detected_colour