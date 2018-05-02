#!/usr/bin/env python

import cv2
import numpy as np
import dlib
import time

detector = dlib.get_frontal_face_detector()

# Change this accordingly to the location where you have the file.
predictor = dlib.shape_predictor("C:/Users/venka/Documents/GitHub/POMDP/kinect_op_bridge/src/shape_predictor_68_face_landmarks.dat")

cap = cv2.VideoCapture(0)

def main_loop():
    _,image = cap.read()
    image = cv2.resize(image,(300,200))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    clahe_image = clahe.apply(gray)

    detections = detector(clahe_image, 1)

    for k,d in enumerate(detections):
        shape = predictor(clahe_image, d)

        left,right = calculate_mean_distance(shape)
        difference = left - right
	
        if difference >= -8:
            side = 1
            print("User is focused")
        else:
            side = 0
            print("User is distracted")

    cv2.imshow('test_window',image)
    cv2.waitKey(1)

def calculate_mean_distance(shape):
    left_side = []
    right_side = []

    distance = 0
    sum_left = 0
    sum_right = 0
    num_points = 19
    center = shape.part(30)
    
    for i in range(0,48):
        if i >= 0 and i<=7:
            left_side.append(shape.part(i))
        elif i >=9 and i <= 16:
            right_side.append(shape.part(i))
        elif i >= 17 and i <= 21:
            left_side.append(shape.part(i))
        elif i >=22 and i<= 26:
            right_side.append(shape.part(i))
        elif i >=36 and i<=41:
            left_side.append(shape.part(i))
        elif i >=42 and i<=47:
            right_side.append(shape.part(i))

    for data_point in left_side:
        distance = np.sqrt((center.x-data_point.x)**2+(center.y-data_point.y)**2)
        sum_left = sum_left + distance

    for data_point in right_side:
        distance = np.sqrt((center.x-data_point.x)**2+(center.y-data_point.y)**2)
        sum_right = sum_right + distance

    avg_left = sum_left/num_points
    avg_right = sum_right/num_points
    return avg_left,avg_right

if __name__ == '__main__':
	while True:
		main_loop()








