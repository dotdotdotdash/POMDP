# POMDP
Intelligent Attention Management using Integrated Planning and Perception

An individual research project dealing with suggesting optimal policy for multitasking users. The systems consists of two parts; a perception algorithm and a decision system. This repository basically deals with the perception algorithm and doesn't have the POMDP solver. 

The perception algorithm fundamentally works on top of the data fetched from the camera and preprocessing it with the Dlib library. Then the essential features from the face is extracted. 

<img src="https://github.com/dotdotdotdash/POMDP/blob/master/perception_approach.jpg"></img>

The datapoints extracted through perception is fed to the POMDP engine as an observation. Then an optimal policy is suggested to the user.

<img src="https://github.com/dotdotdotdash/POMDP/blob/master/POMDP%20engine.JPG"></img>

# How to use the package ?
Step - 1: Clone the package.
Step - 2: Change the location of the shape_predictor_68_face_landmarks.dat file in image_bridge_opencv.py.
Step - 3: Run the python script. You should be getting the estimated pose of the user.
