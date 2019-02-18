#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import sys
import os
import win32api
import win32con

try:
    cascPath = 'eye.xml'
    eyeCascade = cv2.CascadeClassifier(cascPath)
    casc2Path = 'face.xml'
    faceCascade = cv2.CascadeClassifier(casc2Path)
except Exception:
    print 'Missing Args! Run from CMD with the form eyereader.py eye.xml face.xml'
    sys.exit(0)
video_capture = cv2.VideoCapture(0)
video_capture.set(3, 320)
video_capture.set(4, 180)
offset = 0
ax = 0
ay = 0
cali = 0
while True:
    (ret, frame) = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eyeCascade.detectMultiScale(gray, scaleFactor=1.1,
            minNeighbors=5, minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1,
            minNeighbors=5, minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
    for (fax, fay, faw, fah) in faces:
        cv2.rectangle(frame, (fax + faw / 2, fay), (fax + faw / 2, fay
                      + fah), (0, 0xFF, 0), 2)
        cv2.rectangle(frame, (fax, fay - offset), (fax + faw, fay
                      - offset), (0, 0xFF, 0), 2)
        facecoord = fay
        if cali == 0:
            print 'Calibrated.'
            ax = fax + faw / 2
            ay = fay - offset
            cali += 1
        else:
            pass
    try:
        x1 = eyes[0][0] + eyes[0][2] / 2
        y1 = eyes[0][1] + eyes[0][3] / 2
        x2 = eyes[1][0] + eyes[1][2] / 2
        y2 = eyes[1][1] + eyes[1][3] / 2
        eyedist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        midx = (x1 + x2) / 2
        midy = (y1 + y2) / 2
        cv2.rectangle(frame, (midx - 1, midy - 1), (midx + 1, midy
                      + 1), (0, 0, 0xFF), 2)
        eyecoord = midy
        spx = 383 + 20 * (ax - midx)
        spy = -5 * (ay - midy)
        if (midx, midy) == (x1, y1) or (midx, midy) == (x2, y2):
            pass
        else:
            win32api.SetCursorPos((int(spx), int(spy)))
    except Exception:
        (x, y) = win32api.GetCursorPos()
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    cv2.imshow('Webcam View', frame)
    if offset == 0:
        try:
            offset = facecoord - eyecoord
        except Exception:
            pass
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break
video_capture.release()
cv2.destroyAllWindows()
