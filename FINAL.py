import cv2
import numpy as np

# Initialize the laptop camera
cap = cv2.VideoCapture(0)  # 0 is typically the default camera for most laptops

# Check if the camera is opened
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Manually define the frame size (x, y, width, height)
frame_x, frame_y, frame_width, frame_height = 50, 50, 200, 280  # Adjust these values to define the frame

while True:
    # Read frame from the laptop camera
    ret, frame = cap.read()

    # Check if the frame was read correctly
    if not ret:
        print("Error: Failed to capture image from the camera.")
        break

    # Convert the image to grayscale and apply edge detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Assume the largest contour corresponds to the picture/object
        largest_contour = max(contours, key=cv2.contourArea)

        # Get the bounding box of the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Check if the object crosses the border of the frame
        if (x < frame_x or x + w > frame_x + frame_width or  # Object is outside the left or right boundary
            y < frame_y or y + h > frame_y + frame_height):  # Object is outside the top or bottom boundary
            error_detected = True
            print("Error: Object has crossed the border of the frame!")
            cv2.putText(frame, "ERROR: Misalignment Detected", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            error_detected = False
            print("No misalignment detected.")

        # Draw the frame rectangle for visual reference
        cv2.rectangle(frame, (frame_x, frame_y), (frame_x + frame_width, frame_y + frame_height), (0, 255, 0), 2)

    else:
        print("No object detected in the frame.")

    # Display the live feed with bounding boxes and error message
    cv2.imshow("Live Feed - Detecting Misalignment", frame)

    # Break the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
