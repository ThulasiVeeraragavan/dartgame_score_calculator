# import cv2
# import numpy as np
# import tkinter as tk
# from tkinter import messagebox

# # Default scoring values based on game type
# scoring_values = {
#     'Normal': [100, 80, 60, 5],  # Scores for bullseye, bull, triple, and outer ring
#     '301': [100, 80, 60, 5],
#     '501': [101, 81, 61, 5],
# }

# # Initialize selected game type and total score
# selected_game_type = 'Normal'
# total_score = 0  

# # HSV values for green detection (adjust if needed)
# hsvVals = {'hmin': 44, 'smin': 91, 'vmin': 11, 'hmax': 68, 'smax': 255, 'vmax': 255}
# lower_green = np.array([hsvVals['hmin'], hsvVals['smin'], hsvVals['vmin']])
# upper_green = np.array([hsvVals['hmax'], hsvVals['smax'], hsvVals['vmax']])

# # Initialize video capture
# cap = cv2.VideoCapture("q2.webm")  # Change to your video file path or use camera input

# def detect_dartboard(frame):
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     gray = cv2.medianBlur(gray, 5)

#     circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=200,
#                                param1=100, param2=30, minRadius=100, maxRadius=300)

#     if circles is not None:
#         circles = np.uint16(np.around(circles))
#         for circle in circles[0, :]:
#             center_x, center_y, radius = circle
#             cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)  # Draw the outer circle
#             cv2.circle(frame, (center_x, center_y), 2, (255, 20, 147), 3)  # Draw the center point
#             scoring_radii = [radius * 0.1, radius * 0.5, radius * 0.75, radius * 1]
#             scoring_colors = [(0, 0, 255), (0, 255, 255), (255, 255, 0), (255, 255, 255)]  # Colors for scoring rings
#             scoring_labels = scoring_values[selected_game_type]

#             # Draw scoring regions
#             for r, color, score in zip(scoring_radii, scoring_colors, scoring_labels):
#                 cv2.circle(frame, (center_x, center_y), int(r), color, 2)
#                 cv2.putText(frame, str(score), (center_x + 10, center_y - int(r)),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1) 

#             radius_end_x = int(center_x + radius * np.cos(0))
#             radius_end_y = int(center_y + radius * np.sin(0)) 
#             cv2.line(frame, (center_x, center_y), (radius_end_x, radius_end_y), (0, 255, 0), 2)  # Draw the radius line
            
#             return (center_x, center_y), radius

#     return None, None

# def get_score(hit_x, hit_y, board_center, board_radius):
#     if board_center is None:
#         return None

#     distance_from_center = np.sqrt((hit_x - board_center[0]) ** 2 + (hit_y - board_center[1]) ** 2)

#     if distance_from_center > board_radius:
#         return None  # Outside the dartboard

#     if distance_from_center < board_radius * 0.1:
#         return scoring_values[selected_game_type][0]  # Bull's Eye
#     elif distance_from_center < board_radius * 0.5:
#         return scoring_values[selected_game_type][1]  # Bull
#     elif distance_from_center < board_radius * 0.75:
#         return scoring_values[selected_game_type][2]  # Triple
#     elif distance_from_center < board_radius * 1:
#         return scoring_values[selected_game_type][3]  # Outer ring
#     else:
#         return 0  # No score

# def select_game_type_and_scores():
#     global selected_game_type, total_score

#     selected_game_type = game_type_var.get()
#     custom_region_selected = custom_region_var.get()  # Check if custom region is selected

#     if custom_region_selected == 'yes':
#         try:
#             scoring_values[selected_game_type] = [
#                 int(score1_entry.get()) if score1_entry.get() else 100,
#                 int(score2_entry.get()) if score2_entry.get() else 80,
#                 int(score3_entry.get()) if score3_entry.get() else 60,
#                 int(score4_entry.get()) if score4_entry.get() else 5
#             ]
#         except ValueError:
#             messagebox.showerror("Invalid Input", "Please enter valid integer scores.")
#             return
#     else:  # If "no" is selected, use default values
#         scoring_values[selected_game_type] = [100, 80, 60, 5]

#     if selected_game_type == '301':
#         total_score = 301
#     elif selected_game_type == '501':
#         total_score = 501
#     else:
#         total_score = 0

#     messagebox.showinfo("Game Type Selected", f"You have selected {selected_game_type}.\n"
#                                                f"Scores: {scoring_values[selected_game_type]}\n"
#                                                f"Total Score: {total_score}")
#     root.quit()

# def toggle_score_entries(enable):
#     score1_entry.config(state='normal' if enable else 'disabled')
#     score2_entry.config(state='normal' if enable else 'disabled')
#     score3_entry.config(state='normal' if enable else 'disabled')
#     score4_entry.config(state='normal' if enable else 'disabled')

# # GUI for selecting game type and scores
# root = tk.Tk()
# root.title("Dart Game Selector")

# game_type_var = tk.StringVar(value='Normal')
# custom_region_var = tk.StringVar(value='no')  # New variable to track custom region selection

# tk.Label(root, text="Select Game Type:").pack(pady=10)

# tk.Radiobutton(root, text="Normal", variable=game_type_var, value='Normal').pack(anchor=tk.W)
# tk.Radiobutton(root, text="301", variable=game_type_var, value='301').pack(anchor=tk.W)
# tk.Radiobutton(root, text="501", variable=game_type_var, value='501').pack(anchor=tk.W)

# tk.Label(root, text="Do You Want to Set Score Region? :").pack(pady=10)
# tk.Radiobutton(root, text="Yes", variable=custom_region_var, value='yes', command=lambda: toggle_score_entries(True)).pack(anchor=tk.W)
# tk.Radiobutton(root, text="No", variable=custom_region_var, value='no', command=lambda: toggle_score_entries(False)).pack(anchor=tk.W)

# tk.Label(root, text="Enter Scores for Regions:").pack(pady=10)

# tk.Label(root, text="Bull's Eye Score:").pack()
# score1_entry = tk.Entry(root)
# score1_entry.pack()

# tk.Label(root, text="Bull Score:").pack()
# score2_entry = tk.Entry(root)
# score2_entry.pack()

# tk.Label(root, text="Outer Region Score:").pack()
# score3_entry = tk.Entry(root)
# score3_entry.pack()

# tk.Label(root, text="Last Region Score:").pack()
# score4_entry = tk.Entry(root)
# score4_entry.pack()

# tk.Button(root, text="Start Game", command=select_game_type_and_scores).pack(pady=20)

# root.mainloop()

# # Variables for hit detection
# consecutive_frames = 0
# hit_threshold = 1
# hit_detected = False
# confirmed_hits = []

# # Main loop for processing video frames
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     board_center, board_radius = detect_dartboard(frame)
#     if board_center is None:
#         print("Dartboard not detected")
#         cv2.imshow('Dartboard Scoring', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#         continue

#     hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     mask = cv2.inRange(hsv_frame, lower_green, upper_green)

#     kernel = np.ones((5, 5), np.uint8)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     green_pixel_count = 0
#     for contour in contours:
#         if cv2.contourArea(contour) > 500:  # Minimum area to consider as a hit
#             green_pixel_count += cv2.contourArea(contour)
#             (x, y, w, h) = cv2.boundingRect(contour)
#             center_x, center_y = x + w // 2, y + h // 2
#             confirmed_hits.append((center_x, center_y)) 

#     if green_pixel_count > 1000:
#         consecutive_frames += 1
#     else:
#         consecutive_frames = 0

#     if consecutive_frames >= hit_threshold and not hit_detected:
#         hit_detected = True
#         print("Green ball detected for enough consecutive frames! Hit confirmed.")

#         for hit_x, hit_y in confirmed_hits:
#             score = get_score(hit_x, hit_y, board_center, board_radius)

#             if score is not None:
#                 print("score", score)
#                 if selected_game_type != 'Normal':
#                     total_score -= score
#                 else:
#                     total_score += score  
#                 if total_score < 0: 
#                     total_score = 0
#                 print("total_score", total_score)
#                 cv2.circle(frame, (hit_x, hit_y), 5, (0, 255, 255), -1)
#                 cv2.putText(frame, f'Score: {score}', (hit_x + 10, hit_y - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
#                 print(f"Hit at ({hit_x}, {hit_y}) - Score: {score}")
#             else:
#                 print(f"Hit at ({hit_x}, {hit_y}) is outside the board.")

#         confirmed_hits.clear()

#     elif consecutive_frames < hit_threshold:
#         hit_detected = False
#         print("No green ball detected or not enough consecutive frames for confirmation.")

#     cv2.putText(frame, f'Total Score: {total_score}', (150, 150),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (135, 5, 5), 2)

#     cv2.imshow('Dartboard Scoring', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Default scoring values based on game type
scoring_values = {
    'Normal': [100, 80, 60, 5],  # Scores for bullseye, bull, triple, and outer ring
    '301': [100, 80, 60, 5],
    '501': [101, 81, 61, 5],
}

# Initialize selected game type and total score
selected_game_type = 'Normal'
total_score = 0  

# HSV values for green detection (adjust if needed)
hsvVals = {'hmin': 44, 'smin': 91, 'vmin': 11, 'hmax': 68, 'smax': 255, 'vmax': 255}
lower_green = np.array([hsvVals['hmin'], hsvVals['smin'], hsvVals['vmin']])
upper_green = np.array([hsvVals['hmax'], hsvVals['smax'], hsvVals['vmax']])

# Initialize video capture
cap = cv2.VideoCapture("q2.webm")  # Change to your video file path or use camera input

def detect_dartboard(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=200,
                               param1=100, param2=30, minRadius=100, maxRadius=300)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            center_x, center_y, radius = circle
            cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)  # Draw the outer circle
            cv2.circle(frame, (center_x, center_y), 2, (255, 20, 147), 3)  # Draw the center point

            scoring_radii = [radius * 0.1, radius * 0.5, radius * 0.75, radius * 1]
            scoring_colors = [(0, 0, 255), (0, 255, 255), (255, 255, 0), (255, 255, 255)]
            scoring_labels = scoring_values[selected_game_type]

            # Draw scoring regions
            for r, color, score in zip(scoring_radii, scoring_colors, scoring_labels):
                cv2.circle(frame, (center_x, center_y), int(r), color, 2)
                cv2.putText(frame, str(score), (center_x + 10, center_y - int(r)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

            # Draw lines every 18 degrees from the center
            for angle in range(0, 360, 18):
                angle_rad = np.radians(angle)
                end_x = int(center_x + radius * np.cos(angle_rad))
                end_y = int(center_y + radius * np.sin(angle_rad))
                cv2.line(frame, (center_x, center_y), (end_x, end_y), (0, 0, 0), 2)  # Line color and thickness

            return (center_x, center_y), radius

    return None, None


def get_score(hit_x, hit_y, board_center, board_radius):
    if board_center is None:
        return None

    distance_from_center = np.sqrt((hit_x - board_center[0]) ** 2 + (hit_y - board_center[1]) ** 2)

    if distance_from_center > board_radius:
        return None  # Outside the dartboard

    if distance_from_center < board_radius * 0.1:
        return scoring_values[selected_game_type][0]  # Bull's Eye
    elif distance_from_center < board_radius * 0.5:
        return scoring_values[selected_game_type][1]  # Bull
    elif distance_from_center < board_radius * 0.75:
        return scoring_values[selected_game_type][2]  # Triple
    elif distance_from_center < board_radius * 1:
        return scoring_values[selected_game_type][3]  # Outer ring
    else:
        return 0  # No score

def select_game_type_and_scores():
    global selected_game_type, total_score

    selected_game_type = game_type_var.get()
    custom_region_selected = custom_region_var.get()  # Check if custom region is selected

    if custom_region_selected == 'yes':
        try:
            scoring_values[selected_game_type] = [
                int(score1_entry.get()) if score1_entry.get() else 100,
                int(score2_entry.get()) if score2_entry.get() else 80,
                int(score3_entry.get()) if score3_entry.get() else 60,
                int(score4_entry.get()) if score4_entry.get() else 5
            ]
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integer scores.")
            return
    else:  # If "no" is selected, use default values
        scoring_values[selected_game_type] = [100, 80, 60, 5]

    if selected_game_type == '301':
        total_score = 301
    elif selected_game_type == '501':
        total_score = 501
    else:
        total_score = 0

    messagebox.showinfo("Game Type Selected", f"You have selected {selected_game_type}.\n"
                                               f"Scores: {scoring_values[selected_game_type]}\n"
                                               f"Total Score: {total_score}")
    root.quit()

def toggle_score_entries(enable):
    score1_entry.config(state='normal' if enable else 'disabled')
    score2_entry.config(state='normal' if enable else 'disabled')
    score3_entry.config(state='normal' if enable else 'disabled')
    score4_entry.config(state='normal' if enable else 'disabled')

# GUI for selecting game type and scores
root = tk.Tk()
root.title("Dart Game Selector")

game_type_var = tk.StringVar(value='Normal')
custom_region_var = tk.StringVar(value='no')  # New variable to track custom region selection

tk.Label(root, text="Select Game Type:").pack(pady=10)

tk.Radiobutton(root, text="Normal", variable=game_type_var, value='Normal').pack(anchor=tk.W)
tk.Radiobutton(root, text="301", variable=game_type_var, value='301').pack(anchor=tk.W)
tk.Radiobutton(root, text="501", variable=game_type_var, value='501').pack(anchor=tk.W)

tk.Label(root, text="Do You Want to Set Score Region? :").pack(pady=10)
tk.Radiobutton(root, text="Yes", variable=custom_region_var, value='yes', command=lambda: toggle_score_entries(True)).pack(anchor=tk.W)
tk.Radiobutton(root, text="No", variable=custom_region_var, value='no', command=lambda: toggle_score_entries(False)).pack(anchor=tk.W)

tk.Label(root, text="Enter Scores for Regions:").pack(pady=10)

tk.Label(root, text="Bull's Eye Score:").pack()
score1_entry = tk.Entry(root)
score1_entry.pack()

tk.Label(root, text="Bull Score:").pack()
score2_entry = tk.Entry(root)
score2_entry.pack()

tk.Label(root, text="Outer Region Score:").pack()
score3_entry = tk.Entry(root)
score3_entry.pack()

tk.Label(root, text="Last Region Score:").pack()
score4_entry = tk.Entry(root)
score4_entry.pack()

tk.Button(root, text="Start Game", command=select_game_type_and_scores).pack(pady=20)

root.mainloop()

# Variables for hit detection
consecutive_frames = 0
hit_threshold = 1
hit_detected = False
confirmed_hits = []

# Main loop for processing video frames
while True:
    ret, frame = cap.read()
    if not ret:
        break

    board_center, board_radius = detect_dartboard(frame)
    if board_center is None:
        print("Dartboard not detected")
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

    green_pixel_count = 0
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Minimum area to consider as a hit
            green_pixel_count += cv2.contourArea(contour)
            (x, y, w, h) = cv2.boundingRect(contour)
            center_x, center_y = x + w // 2, y + h // 2
            confirmed_hits.append((center_x, center_y)) 

    if green_pixel_count > 1000:
        consecutive_frames += 1
    else:
        consecutive_frames = 0

    if consecutive_frames >= hit_threshold and not hit_detected:
        hit_detected = True
        print("Green ball detected for enough consecutive frames! Hit confirmed.")

        for hit_x, hit_y in confirmed_hits:
            score = get_score(hit_x, hit_y, board_center, board_radius)

            if score is not None:
                print("score", score)
                if selected_game_type != 'Normal':
                    total_score -= score
                else:
                    total_score += score  
                if total_score < 0: 
                    total_score = 0
                print("total_score", total_score)
                cv2.circle(frame, (hit_x, hit_y), 5, (0, 255, 255), -1)
                cv2.putText(frame, f'Score: {score}', (hit_x + 10, hit_y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                print(f"Hit at ({hit_x}, {hit_y}) - Score: {score}")
            else:
                print(f"Hit at ({hit_x}, {hit_y}) is outside the board.")

        confirmed_hits.clear()

    elif consecutive_frames < hit_threshold:
        hit_detected = False
        print("No green ball detected or not enough consecutive frames for confirmation.")

    cv2.putText(frame, f'Total Score: {total_score}', (150, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (135, 5, 5), 2)

    cv2.imshow('Dartboard Scoring', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
