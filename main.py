# import cv2
# import numpy as np
#
# hsvVals = {'hmin': 44, 'smin': 91, 'vmin': 11, 'hmax': 68, 'smax': 255, 'vmax': 255}
# lower_green = np.array([hsvVals['hmin'], hsvVals['smin'], hsvVals['vmin']])
# upper_green = np.array([hsvVals['hmax'], hsvVals['smax'], hsvVals['vmax']])
#
# cap = cv2.VideoCapture("q2.webm")
#
# def detect_dartboard(frame):
#     """Detects the dartboard and returns its center and radius."""
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     gray = cv2.medianBlur(gray, 5)
#
#     circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=200,
#                                param1=100, param2=30, minRadius=100, maxRadius=300)
#
#     if circles is not None:
#         circles = np.uint16(np.around(circles))
#         for circle in circles[0, :]:
#             center_x, center_y, radius = circle
#             # Draw the detected circle
#             cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)  # Dartboard circle in green
#             cv2.circle(frame, (center_x, center_y), 2, (255, 20, 147), 3)  # Center point in pink
#             return (center_x, center_y), radius
#
#     return None, None
#
# def get_score(hit_x, hit_y, board_center, board_radius):
#     """Calculate the score based on hit location."""
#     if board_center is None:
#         return None
#
#     distance_from_center = np.sqrt((hit_x - board_center[0]) ** 2 + (hit_y - board_center[1]) ** 2)
#
#     print(f"Distance from center: {distance_from_center}, Board radius: {board_radius}")
#
#     if distance_from_center > board_radius:
#         return None
#
#     if distance_from_center < board_radius * 0.1:
#         return 100
#     elif distance_from_center < board_radius * 0.5:
#         return 80
#     elif distance_from_center < board_radius * 0.75:
#         return 60
#     elif distance_from_center < board_radius * 1:
#         return 5
#     else:
#         return 0
#
# consecutive_frames = 0
# hit_threshold = 1
# hit_detected = False
# confirmed_hits = []
# total_score = 0  # Initialize total score
#
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
#
#     board_center, board_radius = detect_dartboard(frame)
#     if board_center is None:
#         print("Dartboard not detected")
#         cv2.imshow('Dartboard Scoring', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#         continue
#
#     hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     mask = cv2.inRange(hsv_frame, lower_green, upper_green)
#
#     kernel = np.ones((5, 5), np.uint8)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
#
#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#     green_pixel_count = 0
#     for contour in contours:
#         if cv2.contourArea(contour) > 500:  # Minimum area to consider as a hit
#             green_pixel_count += cv2.contourArea(contour)
#             (x, y, w, h) = cv2.boundingRect(contour)
#             center_x, center_y = x + w // 2, y + h // 2
#             confirmed_hits.append((center_x, center_y))  # Store the hit position
#
#     if green_pixel_count > 1000:
#         consecutive_frames += 1
#     else:
#         consecutive_frames = 0
#
#     if consecutive_frames >= hit_threshold and not hit_detected:
#         hit_detected = True
#         print("Green ball detected for enough consecutive frames! Hit confirmed.")
#
#         # Process scoring for confirmed hits
#         for hit_x, hit_y in confirmed_hits:
#             score = get_score(hit_x, hit_y, board_center, board_radius)
#
#             if score is not None:
#                 print("score",score)
#                 total_score += score
#                 print("total_score", total_score)
#                 cv2.circle(frame, (hit_x, hit_y), 5, (0, 255, 255), -1)  # Hit in yellow
#                 cv2.putText(frame, f'Score: {score}', (hit_x + 10, hit_y - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
#                 print(f"Hit at ({hit_x}, {hit_y}) - Score: {score}")
#             else:
#                 print(f"Hit at ({hit_x}, {hit_y}) is outside the board.")
#
#         confirmed_hits.clear()
#
#     elif consecutive_frames < hit_threshold:
#         hit_detected = False
#         print("No green ball detected or not enough consecutive frames for confirmation.")
#
#     # Display total score on the frame
#     cv2.putText(frame, f'Total Score: {total_score}', (10, 30),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#
#     # Display the original frame
#     cv2.imshow('Dartboard Scoring', frame)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()
import cv2
import numpy as np
from turtle import Turtle, Screen
import random

# HSV values for detecting the green object (adjust as needed)
hsvVals = {'hmin': 44, 'smin': 91, 'vmin': 11, 'hmax': 68, 'smax': 255, 'vmax': 255}
lower_green = np.array([hsvVals['hmin'], hsvVals['smin'], hsvVals['vmin']])
upper_green = np.array([hsvVals['hmax'], hsvVals['smax'], hsvVals['vmax']])

# OpenCV Video Capture
cap = cv2.VideoCapture("q2.webm")

# Turtle Setup
screen = Screen()
screen.setup(width=600, height=600)
screen.title("Dartboard Visualization")

myPen = Turtle()
myPen.speed(0)
myPen.hideturtle()

def drawLayer(radius, color1, color2):
    """Draw alternating color layers for the dartboard."""
    angle = 18
    initialAngle = angle
    myPen.penup()
    myPen.setheading(180)
    myPen.goto(0, radius)
    myPen.circle(radius, angle // 2)
    myPen.pendown()
    i = 0
    while i <= 20:
        myPen.begin_fill()
        myPen.circle(radius, angle)
        myPen.left(90)
        myPen.forward(radius)
        myPen.left(180 - initialAngle)
        myPen.forward(radius)
        myPen.left(90)
        myPen.speed(0)
        angle = initialAngle * 2
        i += 1
        if i % 2 == 0:
            myPen.fillcolor(color1)
        else:
            myPen.fillcolor(color2)
        myPen.end_fill()

def drawTarget():
    """Draw the entire dartboard target with colored layers."""
    drawLayer(144, "#FF0000", "#099909")
    drawLayer(134, "#111111", "#FFFFAA")
    drawLayer(84, "#FF0000", "#099909")
    drawLayer(74, "#111111", "#FFFFAA")
    # Outer Bull
    myPen.fillcolor("#099909")
    myPen.penup()
    myPen.setheading(180)
    myPen.goto(0, 20)
    myPen.begin_fill()
    myPen.pendown()
    myPen.circle(20)
    myPen.end_fill()
    # Bull's Eye
    myPen.fillcolor("#FF0000")
    myPen.penup()
    myPen.setheading(180)
    myPen.goto(0, 10)
    myPen.begin_fill()
    myPen.pendown()
    myPen.circle(10)
    myPen.end_fill()

def drawCross(color, size, x, y):
    """Draw a cross on the dartboard at hit locations."""
    myPen.pensize(3)
    myPen.color(color)
    myPen.penup()
    myPen.goto(x - size, y - size)
    myPen.pendown()
    myPen.goto(x + size, y + size)
    myPen.penup()
    myPen.goto(x - size, y + size)
    myPen.pendown()
    myPen.goto(x + size, y - size)

def detect_dartboard(frame):
    """Detect the dartboard in the frame and return its center and radius."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(
        gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=200,
        param1=100, param2=30, minRadius=100, maxRadius=300
    )
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            center_x, center_y, radius = circle
            cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)
            cv2.circle(frame, (center_x, center_y), 2, (255, 20, 147), 3)
            return (center_x, center_y), radius
    return None, None

drawTarget()  # Draw dartboard once at the start

while True:
    ret, frame = cap.read()
    if not ret:
        break

    board_center, board_radius = detect_dartboard(frame)
    if board_center is None:
        cv2.imshow('Dartboard Scoring', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, lower_green, upper_green)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 500:
            (x, y, w, h) = cv2.boundingRect(contour)
            center_x, center_y = x + w // 2, y + h // 2
            # Draw cross at detected hit location on turtle dartboard
            turtle_x = (center_x - board_center[0]) * 0.5
            turtle_y = (center_y - board_center[1]) * -0.5
            drawCross("blue", 10, turtle_x, turtle_y)
            cv2.circle(frame, (center_x, center_y), 5, (0, 255, 255), -1)  # Hit in yellow
            cv2.putText(frame, f'Hit Detected', (center_x + 10, center_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow("Dartboard Scoring", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
screen.mainloop()
