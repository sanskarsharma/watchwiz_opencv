import cv2
import time
from datetime import datetime as dt

video = cv2.VideoCapture(1)         # 1 for using secondary camera not webcam
reference_frame = None

time_marker_prev = 0

timelist =[]
timeline = []

while True:
    
    checkstatus , frame = video.read()

    gray_frame = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur( gray_frame, (21,21), 0 )

    if reference_frame is None :
        reference_frame = gray_frame
        print("initial reference frame set, press 'p' to reset referenec frame")
        cv2.imwrite("referenceframe.jpg", reference_frame)
        continue

    delta_frame = cv2.absdiff(reference_frame, gray_frame)
    thresh_frame = cv2.threshold( delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations =2)
    
    (_,cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    time_marker = 0

    for contour in cnts:
        if cv2.contourArea(contour) < 1000 :
            continue
        else:
            time_marker = 1
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)

    if time_marker==1 and time_marker_prev==0 :
        print("Entry")
        timelist.append(dt.now())
    elif time_marker==0 and time_marker_prev==1 :
        print("exit") 
        timelist.append(dt.now())
    time_marker_prev = time_marker

    cv2.imshow("Gray frame Output", gray_frame)
    cv2.imshow("Delta frame Output", delta_frame)
    cv2.imshow("THRESH frame Output", thresh_frame)
    cv2.imshow("FINAL frame Output", frame)

    keypressed = cv2.waitKey(1)
    
    if keypressed == ord('p'):
        reference_frame = gray_frame
        cv2.imwrite("referenceframe.jpg", reference_frame)
        print("referenece frame reset to new , motion time recording started")
    if keypressed==ord('q') or keypressed==ord('p') :
        if time_marker==1 :
            timelist.append(dt.now())
        timeline.append(timelist)
        timelist = []
        time_marker = 0
        time_marker_prev = 0
    if keypressed == ord('q'):
        timeline.append([dt.now()])
        break

video.release()
cv2.destroyAllWindows
print(timeline)