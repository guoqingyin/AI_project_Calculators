
import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import os
import sys
import getopt
import pandas as pd


def main(num=1):

    # Get the value input to choose the number
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:", ["num="])
    except getopt.GetoptError:
        print('Please input python dataset_genration.py -n <num>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-n', '--num'):
            num = arg

    # (1) Capture camera
    cap = cv2.VideoCapture(0)
    cap.set(3, 1080)  # The width of the display box 1080
    cap.set(4, 720)  # The height of the display box 720

    sTime = time.time()  # Set the start time for the first frame to start processing
    pTime = sTime  # Set the first previous time as the start time

    # Hand testing method with a confidence level of 0.8. only one hand is detected
    detector = HandDetector(detectionCon=0.8, maxHands=2)

    # Create empty lists to save datas

    # Lists for left hands
    list_lmList_l = []
    list_bbox_l = []
    list_centerPoint_l = []
    cnt_l = 0

    # Lists for right hands
    list_lmList_r = []
    list_bbox_r = []
    list_centerPoint_r = []
    cnt_r = 0

    # (2) Processing each image frame
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

        if cTime - sTime > 5:
            if cnt_l < 500 or cnt_r < 500:
                cv2.putText(img, f'collecting {num}', (500, 50),
                            cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

                # Save list of 21 landmark points
                for hand in hands:
                    if hand["type"] == "Left" and cnt_l < 500:
                        list_lmList_l.append(hand["lmList"])
                        list_bbox_l.append(hand["bbox"])
                        list_centerPoint_l.append(hand["center"])
                        cnt_l += 1

                    if hand["type"] == "Right" and cnt_r < 500:
                        list_lmList_r.append(hand["lmList"])
                        list_bbox_r.append(hand["bbox"])
                        list_centerPoint_r.append(hand["center"])
                        cnt_r += 1

            # save datas to csv files
            if cnt_l == 500 and cnt_r == 500:
                cv2.putText(img, 'finished collecting', (300, 50),
                            cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                data_l = {"lmList": list_lmList_l,
                          "bbox": list_bbox_l,
                          "center": list_centerPoint_l}
                data_r = {"lmList": list_lmList_r,
                          "bbox": list_bbox_r,
                          "center": list_centerPoint_r}
                df_dataleft = pd.DataFrame(data_l)
                df_dataright = pd.DataFrame(data_r)

                path = os.getcwd()
                parent = os.path.dirname(path)
                df_dataleft.to_csv(f'{parent}/Data/left_{num}.csv')
                df_dataright.to_csv(f'{parent}/Data/right_{num}.csv')

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
