import numpy as np
import cv2 as cv
import argparse
from algo import MeanShift
import time

parser = argparse.ArgumentParser(description='This sample demonstrates the meanshift algorithm.')
parser.add_argument('image', type=str, help='folder of image')
parser.add_argument('m_h', type=int, help='min H', nargs='?', default=0)
parser.add_argument('m_s', type=int, help='min S', nargs='?', default=30)
parser.add_argument('m_v', type=int, help='min V', nargs='?', default=30)
parser.add_argument('M_h', type=int, help='max H', nargs='?', default=180)
parser.add_argument('M_s', type=int, help='max S', nargs='?', default=205)
parser.add_argument('M_v', type=int, help='max V', nargs='?', default=205)

args = parser.parse_args()

cap = cv.VideoCapture(args.image+"/img/%04d.jpg")

file1 = open(args.image + '/groundtruth_rect.txt', 'r')
Lines = file1.readlines()

count = 0
print("Line{}: {}".format(count, Lines[count].strip()))

# take first frame of the video
ret, frame = cap.read()

# setup initial location of window
x, y, w, h = 300, 200, 100, 50  # simply hardcoded the values
track_window = (x, y, w, h)

# set up the ROI for tracking
roi = frame[y:y + h, x:x + w]
hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
mask = cv.inRange(hsv_roi, np.array((int(args.m_h), int(args.m_s),int(args.m_v))), np.array((int(args.M_h), int(args.M_s),int(args.M_v))))
roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
roi_hist = cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)

track_window = None

while (1):

    ret, frame = cap.read()
    if ret == True:
        time.sleep(0.2)
        # Draw it on image
        if track_window is None:
            x, y, w, h = 0, 0, 0, 0
        else:
            x, y, w, h = [int(v) for v in track_window]

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        cv.imshow("Frame2", dst)
        ### Plotting true border
        count +=1
        try:
            tb = [int(i) for i in Lines[count].split(',')]
        except:
            tb = [int(i) for i in Lines[count].split()]
        frame = cv.rectangle(frame, (tb[0], tb[1]), (tb[0] + tb[2], tb[1] + tb[3]), [0,0, 255], 2)
        ###

        key = cv.waitKey(1) & 0xFF
        # if the 's' key is selected, we are going to "select" a bounding
        # box to track
        if key == ord("s"):
            # select the bounding box of the object we want to track (make
            # sure you press ENTER or SPACE after selecting the ROI)
            track_window = cv.selectROI("Frame", frame, fromCenter=False,
                                  showCrosshair=True)
            # set up the ROI for tracking
            x, y, w, h = [int(v) for v in track_window]
            roi = frame[x:x + w, y:y + h]
            hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
            mask = cv.inRange(hsv_roi, np.array((int(args.m_h), int(args.m_s),int(args.m_v))), np.array((int(args.M_h), int(args.M_s),int(args.M_v))))
            roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
            roi_hist = cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)
        if key == 27:
            break

        if track_window is not None:
            # # Usage of self implemented MeanShift
            track_window = MeanShift(dst, track_window).get_trace_window()
            # # Usage of build in function
            # _ , track_window = cv.meanShift(dst, track_window, term_crit)
            frame = cv.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
        # show the output frame
        cv.imshow("Frame", frame)

    else:
        break
