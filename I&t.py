import numpy as np
import cv2
frame_count=0
# Open the Video
video = cv2. VideoCapture('FULL11.mp4')

# read the fiurst frame  of the video as the initial background image
ret, Prev_frame= video.read()



while(video.isOpened()):

    frame_count+=1

    ##capture frame by frame
    ret, Current_frame= video.read()

    # Find the absolute difference between the pixels of the prev_frame and current_frame
    #absdiff() will extract just the pixels of the objects that are moving between the two frames
    frame_diff= cv2.absdiff(Current_frame, Prev_frame)
    motion=0

    # applying Gray scale by converting the images from color to grayscale,
    #This will reduce noise
    gray= cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)

    #image smoothing also called blurring is applied using gauisian Blur
    # convert the gray to Gausioan blur to detect motion

    blur= cv2.GaussianBlur(gray, (5,5), 0)
    thresh= cv2.threshold(blur, 20,255, cv2.THRESH_BINARY)[1]

    # fill the gaps by dialiting the image
    #Dilation is applied to binary images.
    dilate = cv2.dilate(thresh,None, iterations=4 )

    # Finding contour of moving object
    #Contours can be explained simply as a curve joining all the continuous points (along the boundary),
    #having same color or intensity.
    # For better accuracy, use binary images. So before finding contours, we apply threshold aletrnatives
    (contours, _)= cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    # loop over the contours
    for cnt in contours:
        (x,y,w,h) = cv2.boundingRect(cnt)
        if cv2.contourArea(cnt)>700 and (x <= 840) and (y >= 150 and y <=350):

                cv2.rectangle(Prev_frame, (x, y), (x + w, y + h), (255, 255, 0), 3)
                motion+=1
                cv2.putText(Prev_frame, f'person {motion} area {cv2.contourArea(cnt)}', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)


    cv2.line(Prev_frame, (0, 150),(840,150),(0, 0,255), 4)
    cv2.line(Prev_frame, (0, 350),(840,350),(0, 0, 255),4)
    cv2.imshow("feed", Prev_frame)
    cv2.imwrite("frame%d.jpg" % frame_count , Prev_frame)


    Prev_frame=Current_frame

    if ret == False:
        break
    if cv2.waitKey(1) == ord('q'):
        break

video.release()
cv2.destroyAllWindows()