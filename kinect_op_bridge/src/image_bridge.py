#!/usr/bin/env python

import rospy
import cv2
from sensor_msgs.msg import Image
import numpy as np
import dlib
from kinect_op_bridge.msg import Dataset
from cv_bridge import CvBridge, CvBridgeError
import time

bridge = CvBridge()
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("/home/ubuntu/jetsonbot/src/kinect_op_bridge/src/shape_predictor_68_face_landmarks.dat")

def transfer_image(data):
    pub = rospy.Publisher('dataset', Dataset, queue_size = 10)
    dataset = Dataset()
    img_data = Image()
    image = bridge.imgmsg_to_cv2(data, "bgr8")
    image = cv2.resize(image,(300,200))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    clahe_image = clahe.apply(gray)

    detections = detector(clahe_image, 1)
    for k,d in enumerate(detections):
        shape = predictor(clahe_image, d)
        left,right = calculate_mean_distance(shape)
        difference = left - right
        dataset.data = difference
        if difference >= -8:
            side = 1
            rospy.loginfo("User is focused")
        else:
            side = 0
            rospy.loginfo("User is distracted")
        dataset.side = side

    cv2.imshow('test_window',image)
    pub.publish(dataset)
    time.sleep(1)
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

def get_image_from_kinect():
    rospy.init_node('image_subscriber', anonymous=True)
    rospy.Subscriber("/kinect2/hd/image_color", Image, transfer_image)
    rospy.spin()

if __name__ == '__main__':
    get_image_from_kinect()









