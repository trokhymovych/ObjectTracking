import numpy as np
import cv2 as cv
import argparse
from algo import MeanShift
import time

# parse parameters:
parser = argparse.ArgumentParser(description='This sample demonstrates the meanshift algorithm.')
parser.add_argument('image', type=str, help='folder of image')
parser.add_argument('m_h', type=int, help='min H', nargs='?', default=0)
parser.add_argument('m_s', type=int, help='min S', nargs='?', default=30)
parser.add_argument('m_v', type=int, help='min V', nargs='?', default=30)
parser.add_argument('M_h', type=int, help='max H', nargs='?', default=180)
parser.add_argument('M_s', type=int, help='max S', nargs='?', default=205)
parser.add_argument('M_v', type=int, help='max V', nargs='?', default=205)
args = parser.parse_args()


def get_frame(line):
    try:
        tb = [int(i) for i in line.split(',')]
    except:
        tb = [int(i) for i in line.split()]
    return tb


# Reading the data
cap = cv.VideoCapture(args.image + "/img/%04d.jpg")
file1 = open(args.image + '/groundtruth_rect.txt', 'r')
Lines = file1.readlines()
count = 0

# setting initial tracking window
x, y, w, h = get_frame(Lines[count])
track_window = (x, y, w, h)

# take first frame of the video
ret, frame = cap.read()

# set up the ROI for tracking
roi_rgb = frame[y:y + h, x:x + w]
hsv_roi = cv.cvtColor(roi_rgb, cv.COLOR_BGR2HSV)
mask = cv.inRange(hsv_roi, np.array((int(args.m_h), int(args.m_s), int(args.m_v))),
                  np.array((int(args.M_h), int(args.M_s), int(args.M_v))))
roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
roi_hist = cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)

while (1):

    ret, frame = cap.read()
    if ret == True:
        time.sleep(0.2)

        # Plotting predicted border
        x, y, w, h = [int(v) for v in track_window]

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        cv.imshow("Frame2", dst)

        ### Plotting true border
        count += 1
        tb = get_frame(Lines[count])
        frame = cv.rectangle(frame, (tb[0], tb[1]), (tb[0] + tb[2], tb[1] + tb[3]), [0, 0, 255], 2)
        ###

        key = cv.waitKey(1) & 0xFF
        # Reinitialize tracking if needed
        if key == ord("s"):
            # select the bounding box of the object we want to track (make
            # sure you press ENTER or SPACE after selecting the ROI)
            track_window = cv.selectROI("Frame", frame, fromCenter=False,
                                        showCrosshair=True)
            # set up the ROI for tracking
            x, y, w, h = [int(v) for v in track_window]
            roi = frame[y:y + h, x:x + w]
            hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
            mask = cv.inRange(hsv_roi, np.array((int(args.m_h), int(args.m_s), int(args.m_v))),
                              np.array((int(args.M_h), int(args.M_s), int(args.M_v))))
            roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
            roi_hist = cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)
        if key == 27:
            break

        if track_window is not None:
            track_window = MeanShift(dst, track_window).get_trace_window()
            frame = cv.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
        cv.imshow("Frame", frame)

    else:
        break

