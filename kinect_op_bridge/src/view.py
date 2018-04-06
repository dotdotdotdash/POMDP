#!/usr/bin/env python

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import gc

def view_data():
    filename = '/home/ubuntu/jetsonbot/src/kinect_op_bridge/src/data_collection.txt'
    df = pd.read_csv(filename,header = None)
    left = df[1]
    right = df[2]
    difference = df[0]
    train_ratio = len(left)*0.8
    train_data = []
    for i in range(int(train_ratio)):
        datapoint = [left[i], right[i]]
        train_data.append(datapoint)

    random.shuffle(train_data)
    train_left,train_right = zip(*train_data)
    plt.suptitle('Training datapoints', fontsize=20)
    plt.xlabel('mean left distances')
    plt.ylabel('mean right distances')
    plt.scatter(train_left,train_right)
    plt.show()
    kmeans = KMeans(n_clusters=2, random_state=0).fit(train_data)

    test_data = []
    red = []
    green = []

    for i in range(int(train_ratio),len(left)):
        datapoint = [left[i], right[i]]
        test_data.append(datapoint)

    prediction = kmeans.predict(test_data)
    centers = kmeans.cluster_centers_
    plt.suptitle('Testing datapoints', fontsize=20)
    plt.xlabel('mean left distances')
    plt.ylabel('mean right distances')
    test_left,test_right = zip(*test_data)
    for i in range(len(test_data)):
        if prediction[i] == 1:
            red.append([test_left[i],test_right[i]])
        else:
            green.append([test_left[i],test_right[i]])

    red_left,red_right = zip(*red)
    plt.scatter(red_left,red_right,color = 'red')
    green_left,green_right = zip(*green)
    plt.scatter(green_left,green_right,color = 'green')

    plt.scatter(centers[0,0],centers[0,1],color='black')
    plt.scatter(centers[1,0],centers[1,1],color='black')
    plt.show()


    fig = plt.figure()
    ax = Axes3D(fig)


    if train_data:
        print("Data has been loaded successfully")

if __name__=="__main__":
    view_data()
