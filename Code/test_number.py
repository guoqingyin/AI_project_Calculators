import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import numpy as np
import torch
import os


def normilization(lmList, bbox, center):
    np_lmList = np.array(lmList).astype(np.float32)
    np_lmList[:, 0] = (np_lmList[:, 0] - center[0]) / bbox[2]
    np_lmList[:, 1] = (np_lmList[:, 1] - center[1]) / bbox[3]
    np_lmList = np_lmList.transpose().reshape(1, 3, 21)
    ts_lmList = torch.tensor(np_lmList, dtype=torch.float32)
    return ts_lmList


def handOutput(hand, model, operator, img):
    lmList = hand["lmList"]  # List of 21 Landmark points
    bbox = hand["bbox"]  # Bounding box info x,y,w,h
    centerPoint = hand['center']  # center of the hand cx,cy
    handType = hand["type"]  # Handtype Left or Right
    ts_lmList = normilization(lmList, bbox, centerPoint)
    if handType == "Left":
        num = torch.argmax(model[0](ts_lmList)).item()
        output = num
        cv2.putText(img, f'number: {output}', (300, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    elif handType == "Right":
        num = torch.argmax(model[1](ts_lmList)).item()
        output = operator[num]
        cv2.putText(img, f'operator: {output}', (700, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    return output


def main():
    # set path to be the folder of data to get the model data
    cur_path = os.getcwd()
    parent = os.path.dirname(cur_path)
    path = parent + '/Data'
    os.chdir(path)

    # (1) Capture camera
    cap = cv2.VideoCapture(0)
    cap.set(3, 1920)  # The width of the display box 1920
    cap.set(4, 720)  # The height of the display box 720

    sTime = time.time()  # Set the start time for the first frame to start processing
    pTime = sTime  # Set the first previous time as the start time

    # Hand testing method with a confidence level of 0.8. only one hand is detected
    detector = HandDetector(detectionCon=0.8, maxHands=2)

    operator = {0: '=', 1: '+', 2: '-', 3: '*', 4: '/',
                5: '(', 6: ')', 7: '.', 8: 'del', 9: 'AC'}

    # Load number identification model
    net_left = torch.load('net_left.pkl', map_location='cpu')
    net_right = torch.load('net_right.pkl', map_location='cpu')
    model = [net_left, net_right]

    while True:

        # Receive images
        success, img = cap.read()

        # Flip the image to ensure that the camera screen and human movement are mirror images
        img = cv2.flip(img, flipCode=1)  # 0 vertical flip, 1 horizontal flip

        # (3) Detect hand keypoints and return the coordinates of all keypoints and the image after drawing
        hands, img = detector.findHands(img, flipType=False)

        # View FPS
        cTime = time.time()  # Time to finish processing an image frame
        fps = 1 / (cTime - pTime)
        pTime = cTime  # Reset start time

        # Display fps information on the video.
        cv2.putText(img, str(int(fps)), (70, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        if hands:
            # Hand 1
            hand1 = hands[0]
            output1 = handOutput(hand1, model, operator, img)

            if len(hands) == 2:
                # Hand 2
                hand2 = hands[1]
                output2 = handOutput(hand2, model, operator, img)

        # Display image, window name and image data
        cv2.imshow('image', img)
        # Each frame lingers for 20 milliseconds and then disappears, press ESC to exit
        if cv2.waitKey(20) & 0xFF == 27:
            break

    # Release video resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
