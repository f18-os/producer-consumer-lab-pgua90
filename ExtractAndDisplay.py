#!/usr/bin/env python3
#! /usr/bin/pip
import os
import threading
import cv2
import base64
import queue

frame_1 = []
frame_2 = []
semaphore_1 = threading.Semaphore(10)
semaphore_2 = threading.Semaphore(10)
semaphore_3 = threading.Semaphore(10)
semaphore_4 = threading.Semaphore(10)
lock_1 = threading.Lock()
lock_2 = threading.Lock()

class extractFrames(threading.Thread):
    def __init__(self):
        super(extractFrames, self).__init__()

    def extracting(self):
        filename = 'clip.mp4'
        vidcap = cv2.VideoCapture(fileName)    
        success = vidcap.read()
        image = vidcap.read()
        count = 0
        print("Reading frame {} {} ".format(count, success))
        count+=1
        while success:
            semaphore_1.acquire()
            lock_1.acquire()
            frame_1.append(image)
            success,image = vidcap.read()
            print('Reading frame {} {}'.format(count, success))
            count += 1
            lock_1.release()
            semaphore_1.release()
        for x in range(10):
            semaphore_1.release()
        print("Frame extraction complete")

class convertFrames(threading.Thread):
    def __init__(self):
        super(convertFrames, self).__init__()
    def converting(self):
        count2 = 0
        while True:
            semaphore_2.acquire()
            semaphore_3.acquire()
            lock_1.acquire()
            lock_2.acquire()
            if(frame_1):
                freeFrame = frame_1.pop()
            else:
                break
            grayFrame = cv2.cvtColor(freeFrame, cv2.COLOR_BGR2GRAY)
            frame_2.append(grayFrame)
            print("Converting frame {}".format(count))
            count2 += 1
            lock_2.release()
            lock_1.release()
            semaphore_4.release()
            semaphore_1.release()
        lock_2.release()
        lock_1.release()
        semaphore_1.release()
        for x in range(10):
            semaphore_4.release()
        
class displayFrames(threading.Thread):
    def __init__(self):
        super(displayFrames, self).__init__()
    def displaying(self):
        while True:
            semaphore_4.acquire()
            lock_2.acquire()
            if(frame_2):
                freeFrame2 = frame_2.pop()
                cv2.imshow("Video",freeFrame2)
                if cv2.waitKey(24) and 0xFF == ord("q"):
                    break
            else:
                print("Finished displaying all frames")
                break
            lock_2.release()
            semaphore_4.release()

for x in range(10):
    semaphore_2.acquire()
    semaphore_4.acquire()

toDisplay = displayFrames()
toConvert = convertFrames()
toExtract = extractFrames()

toDisplay.start()
toConvert.start()
toExtract.start()