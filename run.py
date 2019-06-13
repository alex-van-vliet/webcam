#!python
import roslib
import numpy as np
import cv2
import time
import os
import argparse
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def ms_time():
    return int(round(time.time() * 1000))

parser = argparse.ArgumentParser(description='Take images from webcam.')
parser.add_argument('--width', action='store', default=640, type=int)
parser.add_argument('--height', action='store', default=480, type=int)
parser.add_argument('--color', action='store_true', default=False)
parser.add_argument('--directory', action='store', default='images')
parser.add_argument('--frequency', action='store', default=0, type=float, help="0 to take images as fast as possible")
parser.add_argument('--topic', action='store', default=None)
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
gray = not args.color
print("Grayscale:", gray)
directory = os.path.abspath(args.directory) + "-" + str(ms_time())
print("Directory:", directory)
os.makedirs(directory)#, exist_ok=True) Considering py2 because some dependencies don't work on py3
frequency = args.frequency
print("Frequency:", frequency)
if frequency < 0:
    print("Invalid frequency")
    exit(1)
if frequency:
    delay = 1000 / frequency
topic = args.topic
print("Topic:", topic)

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

if topic:
    bridge = CvBridge()
    publisher = rospy.Publisher(topic, Image, queue_size=10)

rospy.init_node('webcam', anonymous=True)

i = 0
while True:
    # Capture frame-by-frame
    if frequency:
        start_time = time.time() * 1000
        expected_next = start_time + delay
    name = str(i) + "-" + str(ms_time()) + ".png"
    ret, frame = cap.read()
    # Our operations on the frame come here
    if gray:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the resulting frame
        if topic:
            publisher.publish(bridge.cv2_to_imgmsg(frame, "8UC1"))
    cv2.imwrite(os.path.join(directory, name), frame)
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if frequency:
        real_delay = expected_next - time.time() * 1000
        if real_delay < 0:
            print('Lagging')
        else:
            time.sleep(real_delay / 1000)
    i += 1   

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
