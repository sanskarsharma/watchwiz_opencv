import cv2

# start capturing video from primary camera(0)
video = cv2.VideoCapture(0)     # arg can be 0, 1 2 depending on which camera of device to be used

# counter variable 
total_frames_captured = 0 

while True:

    total_frames_captured += 1

    # read() returns status alongwith frame read from video
    checksuccess, frame = video.read()

    print("Success in reading : " + str(checksuccess))
    print(frame)

    # converting frame to grayscale
    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # showing frame in a window
    cv2.imshow("capturing video ...", grayframe)

    # to find which key was pressed
    keypress = cv2.waitKey(1)   # waiting for 1 millisecond before moving ahead 
                                # this runs in while loop and generates frames continuously which we see as video in our window

    if keypress==ord('q'):
        break


video.release()
cv2.destroyAllWindows

print("total_frames_captured = "+ str(total_frames_captured))