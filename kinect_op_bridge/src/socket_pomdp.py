#!/usr/bin/env python

import rospy
import numpy as np
import socket
import random
from kinect_op_bridge.msg import Dataset
import sys
import time

count = 0
priority = 'low'

s = socket.socket()
host = "10.211.22.244"
port = 9077
s.bind((host,port))

def get_data(data):
    global count,priority
    pose = data.side
    if pose == 1:
        focus = 'pos'
    else:
        focus = 'neg'
#    priority_interval = 20

#    if count == priority_interval:
#        priority_list = ['high','medium']
#        priority = random.choice(priority_list)
#        count = 0

    message = focus+','+priority
    s.listen(5)

    if True:
        c, addr = s.accept()
        c.send(message)
        time.sleep(1)
    else:
        c.close()

    print("focus is",focus,"Priority is",priority)
    count += 1

if __name__=="__main__":
    rospy.init_node('socket',anonymous=True)
    rospy.Subscriber("dataset", Dataset, get_data)
    rospy.spin()
