```
python3 multithreading.py     # The main code
```
# Introduction
This is the common project of the course "Robotics and Autonomous Systems(2022)" in University of Turku. The main task of this project is to make the tello pass 3 diffirent gates automatically. The principle is shown below.
<img src="img/System.jpeg" width=2500>
## Gate 1
Gate 1 includes 4 arcuo codes, we need to decect all the arcuo codes and calculate the position of the center of 4 arcuo codes. By some calculation, we can gat the center point of the Gate 1, and then compare it with the center point of the image frame of the drone. Arccoding to the diffirence of two center points, planning the path and motion and controling the drone automatically.
## Gate 2
Gate 2 is a full green rectangle, we first extract the green components of the image frame, and then use edge detection to get the max green rectangle. Similarly, calculate 2 center points and do path and motion planing.
## Gate 3
Gate 3 includes 4 green corners, similar with Gate 2, we extract the green components and detect 4 largest rectangle edges.
