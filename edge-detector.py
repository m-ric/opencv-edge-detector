#!/usr/bin/python

import cv2
import cv2.cv as cv
import thread
import numpy as np
import time
# from matplotlib import pyplot as plt

def get_properties(cap):
    width = cap.get(cv.CV_CAP_PROP_FRAME_WIDTH) # 3
    height = cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT) # 4
    #fps = cap.get(cv.CV_CAP_PROP_FPS) # 5
    #rgb = cap.get(cv.CV_CAP_PROP_CONVERT_RGB) # 16
    print "properties:", width, "x", height#, "at", fps, "fps"

def trackbar_cb(arg):
    # global edges
    # cv2.imshow("Edge", edges)
    pass

def detect_edges(rval):
    ''' detect image edges using Canny algo, wait for keyboard event '''
    global frame

    # create trackbar for edge window
    cv2.createTrackbar('canny1', 'Edge', 0, 1000, trackbar_cb)
    cv2.createTrackbar('canny2', 'Edge', 0, 1000, trackbar_cb)

    while rval:
        c1 = cv2.getTrackbarPos('canny1', 'Edge')
        c2 = cv2.getTrackbarPos('canny2', 'Edge')

        # Canny requires the image to be in grayscale format (CV_8U)
        grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(grayframe, c1, c2)
        cv2.imshow("Edge", edges)
        time.sleep(0.025)

def cam_preview(rval):
    ''' preview webcam content, wait for keyboard event '''

    global frame, leave

    toggle = True

    while rval:
        cv2.imshow("Webcam", frame)
        time.sleep(0.025)
        # wait 25ms for a keystroke
        key = cv2.waitKey(25)
        if (key & 255) == 27: # exit on ESC, masking necessary on 64-bit machines
            leave = True
            break
        elif chr(key & 255) == 's': # ord('s') = key
            toggle = not toggle
        elif chr(key & 255) == 'f':
            thread.start_new_thread(detect_face, (rval,))

        if toggle:
            rval, frame = capture.read()

        # print "cam_preview"

def detect_face(rval):
    ''' detect face on image capture by camera '''

    global frame

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(grayframe, scaleFactor=1.1,
                                          minNeighbors=4, minSize=(50,50),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
    cv2.imshow('Face-eyes', grayframe)
    print "len(faces):", len(faces)

    for (x,y,w,h) in faces:
        print "face detected!"
        cv2.rectangle(grayframe,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.imshow('Face-eyes', grayframe)
        roi_gray = grayframe[y:y+h, x:x+w]
        roi_color = grayframe[y:y+h, x:x+w]
        eyes = eye_cascade,detectMultiScale(roi_gray)
        print "eye detection done"
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)

# k = 1048678
# print chr(k & 255)
# print chr(-1048577 & 255)

# create new windows
cv2.namedWindow("Webcam")
cv2.namedWindow("Edge")
cv2.namedWindow("Face-eyes")

# create global edge image
# edges = None
leave = False

# capture video and check it is ok, else quit
capture = cv2.VideoCapture(0)
if capture.isOpened():
    rval, frame = capture.read()
    get_properties(capture)
else:
    rval = False
    # capture.open()

# separate cam preview and edges in different threads
try:
    thread.start_new_thread(cam_preview, (rval,))
    thread.start_new_thread(detect_edges, (rval,))
except Exception as errtxt:
    print "error: unable to start thread,", errtxt

# main thread just loops
while not leave:
    pass

capture.release()
cv2.destroyWindow("Webcam")
cv2.destroyWindow("Edge")

