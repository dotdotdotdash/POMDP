#!/usr/bin/env python

import rospy
import numpy as np
import pandas as pd
import sklearn as learn
import matplotlib as plt
from kinect_op_bridge.msg import Dataset
import sys
import gc

collect_data = []
count = 0

def get_data(data):
    global collect_data,count
    filename = './src/kinect_op_bridge/src/data_collection.txt'
    batch_size = 15
    difference = data.data
    left = data.data_left
    right = data.data_right

    dataset = {'diff' : difference,'left' : left,'right' : right}
    collect_data.append(dataset)
    if count % batch_size == 0:
        df = pd.DataFrame(data = collect_data, columns = ['diff','left','right'])
        df.to_csv(filename,index=False,header=False)
        print('Data written to {}'.format(filename))
    count += 1
#    print('Difference: {} | Left: {} | Right: {}'.format(difference,left,right))

if __name__=="__main__":
    rospy.init_node('training',anonymous=True)
    rospy.Subscriber("dataset", Dataset, get_data)
    rospy.spin()
