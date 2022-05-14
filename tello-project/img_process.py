import cv2 as cv
import numpy as np


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


def door1(image):
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
            cv.circle(frame, (center_arcuo[i][0],center_arcuo[i][1]), 8, (0, 0, 255), 3, 8, 0)
        cv.circle(frame, (center_x,center_y), 8, (0, 0, 255), 3, 8, 0)
        cv.circle(frame, (frame_x,frame_y), 10, (255, 255, 0), 3, 8, 0)
        cv.line(frame, (frame_x,frame_y), (center_x,center_y), (0, 255, 0), 2, 4)
        corner_ids = get_ids_flag(ids)
        x,y,w,h = get_rectangle_points(center_arcuo)

        if corner_ids == 10:
            flag=1
            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        return frame, center_x,center_y,flag,w,h    
    else:
        flag = -1
        
        return frame, None,None,flag,None,None
            

def door2(image):
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

def door3(img):
    flag=0
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask_green = cv.inRange(hsv, (35,43,35),(90,255,255))

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