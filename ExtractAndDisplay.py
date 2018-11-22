#!/usr/bin/env python3
#! /usr/bin/pip
import cv2
import os
import threading
import base64
import queue

frame1 = []
frame2 = []
lock1 = threading.Lock()
semaphore1 = threading.Semaphore(10)
semaphore2 = threading.Semaphore(10)
lock2 = threading.Lock()
semaphore3 = threading.Semaphore(10)
semaphore4 = threading.Semaphore(10)

class extractFrames(threading.Thread):
    def __init__(self):
        super(extractFrames, self).__init__()
    def run(self): #Beginning of thread to extract all frames.
        clip = 'clip.mp4'
        vidcap = cv2.VideoCapture(clip)
        success, image = vidcap.read()
        count = 0
        print("Reading frame {} {} ".format(count, success))
        count+=1
        while success: #Obtaining or reading frames one by one, until there are no more threads.
            semaphore1.acquire()
            lock1.acquire()
            frame1.append(image)
            success,image = vidcap.read()
            print('Reading frame {} {}'.format(count, success))
            count += 1
            lock1.release()
            semaphore1.release()
        for x in range(10):
            semaphore1.release()
        print("Frame extraction complete")

#Frames are converted and sent to its queue.
class convertFrames(threading.Thread):
    def __init__(self):
        super(convertFrames, self).__init__()

    def run(self): #Beginning of thread to convert frames in greyscale.
        count2 = 0
        while True: 
            semaphore2.acquire()
            semaphore3.acquire()
            lock1.acquire()
            lock2.acquire()
            if(frame1):
                freeFrame = frame1.pop()
            else:
                break
            grayFrame = cv2.cvtColor(freeFrame, cv2.COLOR_BGR2GRAY) #Frame converts to greyscale
            frame2.append(grayFrame)
            print("Converting frame {}".format(count2))
            count2 += 1
            lock2.release()
            lock1.release()
            semaphore4.release()
            semaphore1.release()
        lock2.release()
        lock1.release()
        semaphore1.release()
        for x in range(10):
            semaphore4.release()
        
class displayFrames(threading.Thread):
    def __init__(self):
        super(displayFrames, self).__init__()
    def run(self): #Beginning of thread for displaying frames
        while True:
            semaphore4.acquire()
            lock2.acquire()
            if(frame2):
                freeFrame2 = frame2.pop()
                cv2.imshow("Video", freeFrame2)
                if cv2.waitKey(24) and 0xFF == ord("q"):
                    break
            else:
                break
            lock2.release()
            semaphore3.release()

for x in range(10):
    semaphore2.acquire()
    semaphore4.acquire()

#Setting threads to be able to run them easily.
dis = displayFrames()
con = convertFrames()
ext = extractFrames()

#Starting all threads
ext.start()
con.start()
dis.start()