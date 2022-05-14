# Introduction
This is the common project of the course "Robotics and Autonomous Systems(2022)" in University of Turku. The main task of this project is to make the tello pass 3 diffirent gates automatically. The principle is shown below.
<img src="img/System.jpeg" width=2500>
## Gate 1
Gate 1 include 4 arcuo codes, we need to decect all the arcuo codes and calculate the position of the center of 4 arcuo codes. By some calculation, we can gat the center point of the Gate 1, and then compare it with the center point of the image frame of the drone. Arccoding to the diffirence of two center points, planning the path and motion and controling the drone automatically.

