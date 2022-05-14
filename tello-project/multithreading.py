import time
import cv2 as cv
from threading import Thread
from djitellopy import Tello
from img_process import gate3, gate2, gate1

tello = Tello()
tello.connect()



keepRecording = True
keepMoveing = True
tello.streamon()
frame_read = tello.get_frame_read()
cv.waitKey(0)



order_list=[2,1,3]


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



player = Thread(target=videoplayer)
player.start()



tello.takeoff()
tello.move_up(90)
tello.move_forward(30)
time.sleep(3)
print('start')
cc_x1=1
cc_y1=1
cc_x2=1
cc_y2=1
cc_x3=1
cc_y3=1
flagg1=0
flagg2=0
flagg3=0
while True:
    print(order_list[0])
    if order_list[0]==1:
        # ----------------------- gate 1 ----------------------- #
        img1 = frame_read.frame
        img1,cc_xx1,cc_yy1, flag1, weight1,height1 = gate1(img1)
        if flag1 ==1:
            cc_x1=cc_xx1
            cc_y1=cc_yy1
        print('flag1=',flag1)

        if flag1==1:
            flagg1=1

            if int(cc_y1) in range(0, 180):
                
                tello.move_up(20)
                print('up1')

            elif int(cc_y1) > 260:            

                tello.move_down(20)
                print('down1')

            else:
                print(0)   

            if int(cc_x1) in range(340,420):
                if height1>250:
                    tello.move_down(20)
                    tello.move_forward(280)
                    order_list.pop(0)
                    tello.move_up(40)
                else:
                    tello.move_forward(20)
                    
                print('move1')

            elif int(cc_x1) in range(0, 340):
                
                tello.move_left(20)
                print('left1')

            elif int(cc_x1) > 420:    

                tello.move_right(20)
                print('right1')

            else:
                print(0)
        if flagg1 != 1:
            tello.rotate_clockwise(7)

        # ----------------------- EOF: gate 1 ----------------------- #

    if order_list[0]==2:
        # ----------------------- gate 2 ----------------------- #
        img2 = frame_read.frame
        img2,cc_xx2,cc_yy2, flag2,weight2, height2 = gate2(img2)
        if flag2 ==1:
            cc_x2=cc_xx2
            cc_y2=cc_yy2
        print('flag2=',flag2)

        if flag2==1:
            flagg2=1

            if int(cc_y2) in range(0, 220):
                
                tello.move_up(20)
                print('up2')

            elif int(cc_y2) > 280:            

                tello.move_down(20)
                print('down2')

            else:
                print(0)   


            if int(cc_x2) in range(410,460):
                if height2>400:
                    tello.move_down(20)
                    tello.move_forward(230)
                    order_list.pop(0)
                    tello.move_up(40)
                else:
                    tello.move_forward(20)
                print('move2')

            elif int(cc_x2) in range(0, 410):
                
                tello.move_left(20)
                print('left2')

            elif int(cc_x2) > 460:    

                tello.move_right(20)
                print('right2')

            else:
                print(0)

        if flagg2 != 1:
            tello.rotate_counter_clockwise(7)
        # ----------------------- EOF: gate 2 ----------------------- #
    if order_list[0]==3:
        # ----------------------- gate 3 ----------------------- #

        img3 = frame_read.frame
        img3,cc_xx3,cc_yy3, flag3,weight3, height3 = gate3(img3)
        if flag3 ==1:
            cc_x3=cc_xx3
            cc_y3=cc_yy3
        print('flag3=',flag3)

        if flag3==1:
            flagg3=1

            if int(cc_y3) in range(0, 200):
                
                tello.move_up(20)
                print('up3')

            elif int(cc_y3) > 270:            

                tello.move_down(20)
                print('down3')

            else:
                print(0)   


            if int(cc_x3) in range(410,460):
                if height3>270:
                    tello.move_down(20)
                    tello.move_forward(210)
                    break
                else:
                    tello.move_forward(20)
                print('move3')

            elif int(cc_x3) in range(0, 410):
                
                tello.move_left(20)
                print('left3')

            elif int(cc_x3) > 460:    

                tello.move_right(20)
                print('right3')

            else:
                print(0)
        if flagg3 != 1:
            tello.rotate_counter_clockwise(7)
        # ----------------------- EOF: gate 3 ----------------------- #
tello.land()


keepRecording = False
keepMoveing = False
player.join()
