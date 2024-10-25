import cv2
import cvzone
import numpy as np
from cvzone.ColorModule import ColorFinder
import pickle

# Initialize video capture and parameters
cap = cv2.VideoCapture("video_sample.mp4")
frameCounter = 0
cornerPoints = [[234, 56], [1326, 47], [219, 800], [1317, 853]]
colorFinder = ColorFinder(False)  # Disable automatic trackbars in ColorFinder
countHit = 0
imgListBallsDetected = []
hitDrawBallInfoList = []
totalScore = 0

# Define initial HSV values as placeholders
hsvVals = {'hmin': 0, 'smin': 0, 'vmin': 0, 'hmax': 179, 'smax': 255, 'vmax': 255}

# Create trackbars for adjusting HSV values
cv2.namedWindow("HSV Trackbars")
cv2.createTrackbar("Hmin", "HSV Trackbars", hsvVals['hmin'], 179, lambda x: None)
cv2.createTrackbar("Smin", "HSV Trackbars", hsvVals['smin'], 255, lambda x: None)
cv2.createTrackbar("Vmin", "HSV Trackbars", hsvVals['vmin'], 255, lambda x: None)
cv2.createTrackbar("Hmax", "HSV Trackbars", hsvVals['hmax'], 179, lambda x: None)
cv2.createTrackbar("Smax", "HSV Trackbars", hsvVals['smax'], 255, lambda x: None)
cv2.createTrackbar("Vmax", "HSV Trackbars", hsvVals['vmax'], 255, lambda x: None)


def getBoard(img):
    width, height = int(400 * 1.5), int(380 * 1.5)
    pts1 = np.float32(cornerPoints)
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (width, height))
    for x in range(4):
        cv2.circle(img, (cornerPoints[x][0], cornerPoints[x][1]), 15, (0, 255, 0), cv2.FILLED)
    return imgOutput


def detectColorDarts(img):
    imgBlur = cv2.GaussianBlur(img, (7, 7), 2)
    # Get updated HSV values from trackbars
    hsvVals['hmin'] = cv2.getTrackbarPos("Hmin", "HSV Trackbars")
    hsvVals['smin'] = cv2.getTrackbarPos("Smin", "HSV Trackbars")
    hsvVals['vmin'] = cv2.getTrackbarPos("Vmin", "HSV Trackbars")
    hsvVals['hmax'] = cv2.getTrackbarPos("Hmax", "HSV Trackbars")
    hsvVals['smax'] = cv2.getTrackbarPos("Smax", "HSV Trackbars")
    hsvVals['vmax'] = cv2.getTrackbarPos("Vmax", "HSV Trackbars")

    # Use colorFinder to get mask based on hsvVals
    imgColor, mask = colorFinder.update(imgBlur, hsvVals)
    kernel = np.ones((7, 7), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.medianBlur(mask, 9)
    mask = cv2.dilate(mask, kernel, iterations=4)
    kernel = np.ones((9, 9), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return imgColor, mask


while True:
    frameCounter += 1
    if frameCounter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        frameCounter = 0
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    imgBoard = getBoard(img)
    imgColorOnly, mask = detectColorDarts(imgBoard)  # Get color-only result and mask

    # Display results
    cv2.imshow("Detected Color Only", imgColorOnly)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
