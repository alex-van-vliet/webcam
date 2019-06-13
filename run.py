import numpy as np
import cv2
import time
import os
import argparse

def ms_time():
    return int(round(time.time() * 1000))

parser = argparse.ArgumentParser(description='Take images from webcam.')
parser.add_argument('--width', action='store', default=640, type=int)
parser.add_argument('--height', action='store', default=480, type=int)
parser.add_argument('--grayscale', action='store_true', default=False)
parser.add_argument('--directory', action='store', default='images')
args = parser.parse_args()
width = args.width
print("Width:", width)
if width <= 0:
    print("Invalid width")
    exit(1)
height = args.height
print("Height:", height)
if height <= 0:
    print("Invalid height")
    exit(1)
gray = args.grayscale
print("Grayscale:", gray)
directory = os.path.abspath(args.directory) + "-" + str(ms_time())
print("Directory:", directory)
os.makedirs(directory, exist_ok=True)

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

i = 0
while True:
    # Capture frame-by-frame
    name = str(i) + "-" + str(ms_time()) + ".png"
    ret, frame = cap.read()
    # Our operations on the frame come here
    if gray:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv2.imwrite(os.path.join(directory, name), frame)
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    i += 1   

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
