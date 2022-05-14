# Introduction
This is the common project of the course "Robotics and Autonomous Systems(2022)" in University of Turku. The main task of this project is to make the tello pass 3 diffirent gates automatically. The principle is shown below.
<img src="img/System.jpeg" width=2500>
## Gate 1
Gate 1 includes 4 arcuo codes, we need to decect all the arcuo codes and calculate the position of the center of 4 arcuo codes. By some calculation, we can gat the center point of the Gate 1, and then compare it with the center point of the image frame of the drone. According to the diffirence of two center points, planning the path and motion and controling the drone automatically.
## Gate 2
Gate 2 is a full green rectangle, we first extract the green components of the image frame, and then use edge detection to get the max green rectangle. Similarly, calculate 2 center points and do path and motion planing.
## Gate 3
Gate 3 includes 4 green corners, similar with Gate 2, we extract the green components and detect 4 largest rectangle edges.
# Results
| Gate1                                                         | Gate2                                                                                           | Gate3                                                                                       |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| <img src="img/gate1.gif" width=400>| <img src="img/gate2.gif" width=400> | <img src="img/gate3.gif" width=400>|

| Go through 3 gates in a row                                                        | 
| ------------------------------------------------------------------------------------ |
| <img src="img/pass 3 gates.gif" width=2000>|

# How to use
## Before using
change the order_list, if you want to go though gate2:
```
order_list=[2]
```
if you want go though Gate 2, Gate 1 and Gate 3 in order:
```
order_list=[2,1,3]
```

## Run the main code
```
python3 multithreading.py
```
## Live drone footage in another thread
```
def videoplayer():
    
    while keepRecording:
        
        image1 = frame_read.frame
        if order_list[0]==1:
            image1, cc_x,cc_y, flag, weight,height = gate1(image1)
        elif order_list[0]==2:
            image1, cc_x,cc_y, flag, weight,height = gate2(image1)
        elif order_list[0]==3:
            image1, cc_x,cc_y, flag, weight,height = gate3(image1)

        key = cv.waitKey(1) & 0xff
        if key == 27: # ESC
            break
        cv.imshow("drone", image1)
```


### Detection algorithm of Gate1
```
from img_process import gate1
```
```
def get_corner_center(corners):
    center = []
    for i in range(len(corners)):
        x = int(np.sum(corners[i][0].T[0])/4.0)
        y = int(np.sum(corners[i][0].T[1])/4.0)
        center.append([x,y])
    return center

def get_center(center):
    x = int(np.sum(np.array(center).T[0])/len(center))
    y = int(np.sum(np.array(center).T[1])/len(center))
    
    return x,y
    
def get_ids_flag(ids):
    corner_ids = []
    for i in range(len(ids)):
        id = ids[i][0]
        corner_ids.append(id)
    return np.sum(np.array(corner_ids))
    
    
def get_rectangle_points(arr):
    sum_arr = []
    for i in range(len(arr)):
        sum = arr[i][0]+arr[i][1]
        sum_arr.append(sum)
    index_min = sum_arr.index(min(sum_arr))
    x = arr[index_min][0]
    y = arr[index_min][1]
    w = max(np.array(arr).T[0]) - min(np.array(arr).T[0])
    h = max(np.array(arr).T[1]) - min(np.array(arr).T[1])
    return x,y,w,h


def gate1(image):
    flag=-1
    frame = image
    frame=cv.resize(frame,None,fx=0.9,fy=0.9,interpolation=cv.INTER_CUBIC)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_250)
    parameters =  cv.aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = cv.aruco.detectMarkers(gray,aruco_dict,parameters=parameters)
    cv.aruco.drawDetectedMarkers(frame, corners,ids)


    if ids is not None:
        cv.aruco.drawDetectedMarkers(frame, corners, ids)
        center_arcuo = get_corner_center(corners)
        center_x,center_y = get_center(center_arcuo)
        frame_x = int(frame.shape[1]/2)
        frame_y = int(frame.shape[0]/2)
        for i in range(len(center_arcuo)):
            cv.circle(frame, (center_arcuo[i][0],center_arcuo[i][1]), 80, (0, 0, 255), 30, 8, 0)
        cv.circle(frame, (center_x,center_y), 8, (0, 0, 255), 10, 8, 0)
        cv.circle(frame, (frame_x,frame_y), 8, (255, 255, 0), 10, 8, 0)
        cv.line(frame, (frame_x,frame_y), (center_x,center_y), (0, 255, 0), 2, 4)
        corner_ids = get_ids_flag(ids)
        x,y,w,h = get_rectangle_points(center_arcuo)

        if corner_ids == 10:
            flag=1
            # cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        return frame, center_x,center_y,flag,w,h    
    else:
        flag = -1
        
        return frame, None,None,flag,None,None
```
### Detection algorithm of Gate2
```
from img_process import gate2
```
```
def gate2(image):
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask_green = cv.inRange(hsv, (35,43,35),(90,255,255))
    masks = [mask_green]
    flag = 0
    for mask in masks:
        contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) <= 1:
            flag = -1
            return image, None, None, flag, None, None 
        else:
            index = 1
            max = 0
            for c in range(len(contours)):
                area = cv.contourArea(contours[c])
                if area > max:
                    max = area
                    index = c
            if index >= 0:
                rect = cv.minAreaRect(contours[index])
                width=rect[1][0]
                height=rect[1][1]
                mianji = width*height
                if mianji > 50000:
                    flag = 1
                    box = np.int0(cv.boxPoints(rect))
                    cv.drawContours(image,[box],0,(0,0,255),10)
                    cv.circle(image,(np.int32(rect[0][0]),np.int32(rect[0][1])),2,(0,255,0),2,8,0)
                else:
                    flag = 0
            cv.putText(image,'center',(np.int32(rect[0][0]),np.int32(rect[0][1])),cv.FONT_HERSHEY_SIMPLEX,1.00,(0,0,255),2)
        return image,np.int32(rect[0][0]),np.int32(rect[0][1]),flag, width, height
```
### Detection algorithm of Gate3
```
from img_process import gate3
```

```
def gate3(img):
    flag=0
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask_green = cv.inRange(hsv, (30,43,35),(90,255,255))

    contours, hierarchy = cv.findContours(mask_green, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours_index_list=[1,1,1,1]
    area_list=[1,1,1,1]
    if len(contours) <= 1:
        flag = -1
        return img, None, None, flag, None, None 
    else:
        for c in range(len(contours)):
            area = cv.contourArea(contours[c])
            if area > min(area_list):
                contours_index_list[area_list.index(min(area_list))]=c
                area_list[area_list.index(min(area_list))]=area
        area_list_new=[]
        contours_index_list_new=[]
        for i in range(len(area_list)):
            if area_list[i]<max(area_list)*0.3:
                pass
                
            else:
                area_list_new.append(area_list[i])
                contours_index_list_new.append(contours_index_list[i])
        x_list=[]
        y_list=[]
        xplusy_list=[]
        for index in contours_index_list_new:
            rect = cv.minAreaRect(contours[index])
            box = np.int0(cv.boxPoints(rect))
            x_list.append(np.int32(rect[0][0]))
            y_list.append(np.int32(rect[0][1]))
            xplusy_list.append(np.int32(rect[0][0])+np.int32(rect[0][1]))
            cv.drawContours(img,[box],0,(0,255,0),3)

        center_x = int(x_list[xplusy_list.index(max(xplusy_list))]/2+x_list[xplusy_list.index(min(xplusy_list))]/2)
        center_y = int(y_list[xplusy_list.index(max(xplusy_list))]/2+y_list[xplusy_list.index(min(xplusy_list))]/2)
        height = y_list[xplusy_list.index(max(xplusy_list))]-y_list[xplusy_list.index(min(xplusy_list))]

        if max(area_list_new)>20000 and len(area_list_new)==4:
            flag=1
            cv.rectangle(img, (x_list[xplusy_list.index(min(xplusy_list))],y_list[xplusy_list.index(min(xplusy_list))]),
                        (x_list[xplusy_list.index(max(xplusy_list))],y_list[xplusy_list.index(max(xplusy_list))]), (0,0,255), 10)
            cv.circle(img,(center_x,center_y),2,(0,255,0),2,8,0)
            cv.putText(img,'center',(center_x,center_y),cv.FONT_HERSHEY_SIMPLEX,1.00,(0,0,255),2)
        return img, center_x, center_y, flag, None, height
```
