
import cv2
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
import time
# (1) Capture camera
cap = cv2.VideoCapture(0)
cap.set(3, 1080)  # The width of the display box 1080
cap.set(4, 720)  # Display the height of the box 720

pTime = 0  # Set the start time for the first frame to start processing

# Hand testing method with a confidence level of 0.8. only one hand is detected
detector = HandDetector(detectionCon=0.8, maxHands=1)

# (2) Processing each image frame
while True:

    # Receive images
    success, img = cap.read()

    # Flip the image to ensure that the camera screen and human movement are mirror images
    img = cv2.flip(img, flipCode=1)  # 0 vertical flip, 1 horizontal flip

    # (3) Detect hand keypoints and return the coordinates of all keypoints and the image after drawing
    hands, img = detector.findHands(img, flipType=False)

    #detector.fingersUp Detects the status of each finger and returns it as an array
    if hands:
        # Hand 1
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)
        print(fingers1)

    # View FPS
    cTime = time.time()  # Time to finish processing an image frame
    fps = 1 / (cTime - pTime)
    pTime = cTime  # Reset start time

    # Display fps information on the video.
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # Display image, window name and image data
    cv2.imshow('image', img)
    if cv2.waitKey(20) & 0xFF == 27:  # Each frame lingers for 20 milliseconds and then disappears, press ESC to exit
        break

# Release video resources
cap.release()
cv2.destroyAllWindows()

#Testing git