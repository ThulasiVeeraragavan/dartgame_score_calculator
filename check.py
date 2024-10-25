import cv2
import numpy as np

# Define the HSV color range based on your values
hsvVals = {'hmin': 44, 'smin': 91, 'vmin': 11, 'hmax': 68, 'smax': 255, 'vmax': 255}
lower_green = np.array([hsvVals['hmin'], hsvVals['smin'], hsvVals['vmin']])
upper_green = np.array([hsvVals['hmax'], hsvVals['smax'], hsvVals['vmax']])

# Initialize variables
consecutive_frames = 0
hit_threshold = 10
hit_detected = False

# Open video capture
cap = cv2.VideoCapture("q2.webm")  # Replace with your video file path

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the specified green color
    mask = cv2.inRange(hsv_frame, lower_green, upper_green)

    # Clean up the mask using morphological operations
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize green pixel count
    green_pixel_count = 0
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Minimum area to consider as a hit
            green_pixel_count += cv2.contourArea(contour)

    # Display the mask for debugging (optional)
    cv2.imshow('Mask', mask)

    # Check if a green object is detected
    if green_pixel_count > 1000:  # Adjust this threshold based on your needs
        consecutive_frames += 1
    else:
        consecutive_frames = 0

    # If the object is detected for enough frames
    if consecutive_frames >= hit_threshold and not hit_detected:
        hit_detected = True
        print("Green ball detected for enough consecutive frames! Hit confirmed.")
        # Here you can add your hit logic (e.g., scoring, drawing, etc.)
    elif consecutive_frames < hit_threshold:
        hit_detected = False
        print("No green ball detected or not enough consecutive frames for confirmation.")

    # Display the original frame for debugging (optional)
    cv2.imshow('Original Frame', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
