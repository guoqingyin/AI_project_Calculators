import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import numpy as np
import torch
import os
from poland import InversPolishCalculator

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
        output = str(num)
        cv2.putText(img, f'number: {output}', (200, 600),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    elif handType == "Right":
        num = torch.argmax(model[1](ts_lmList)).item()
        output = operator[num]
        cv2.putText(img, f'operator: {output}', (800, 600),
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

    # we define "del" "AC" '=' as long operator
    # means they have to wait double time than the others
    operator = {0: '=', 1: '+', 2: '-', 3: '*', 4: '/',
                5: '(', 6: ')', 7: '.', 8: 'DEL', 9: 'AC'}

    # Load number identification model
    net_left = torch.load('net_left.pkl', map_location='cpu')
    net_right = torch.load('net_right.pkl', map_location='cpu')
    model = [net_left, net_right]


    output_per_frame=[]
    Screen_Display=[]
    stack_operater=[]

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
        cv2.putText(img, str(int(fps)), (1000, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        if hands:
            # Hand 1
            hand1 = hands[0]
            output1 = handOutput(hand1, model, operator, img)
            print(output1)
            output_per_frame.append(output1)
            if len(hands) == 2:
                # Hand 2
                hand2 = hands[1]
                output2 = handOutput(hand2, model, operator, img)
                output_per_frame.append(output2)

        #put every output into output_per_frame and we judge the last 10 output
        #if they are the same means we want do a operation(input the number or operator)
        if len(output_per_frame)>10:
            check=set(output_per_frame[-9:])
            if len(check)==1:
                output_per_frame.clear()
                temp=check.pop()
                #long operator
                if temp in ["AC","DEL","="]:
                    stack_operater.append(temp)
                    if len(stack_operater)==1:
                        continue
                    else:
                        if stack_operater[-1]==stack_operater[-2]:
                            operator_final=stack_operater[-2]
                            stack_operater.clear()
                            if operator_final=="AC":
                                Screen_Display.clear()
                            elif operator_final=="DEL":
                                Screen_Display.pop(-1)
                            else:# =
                                if len(Screen_Display)>=2:
                                    expression="".join(Screen_Display)
                                    Calculator = InversPolishCalculator()
                                    Screen_Display.clear()
                                    Screen_Display.append(Calculator.deal(expression))
                #short operator
                else:
                    Screen_Display.append(temp)

        #print(output_per_frame)
        # Display image, window name and image data
        #cv2.putText(img, 'AI Calculator', (500, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.putText(img, "".join(Screen_Display), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.imshow('image', img)
        # Each frame lingers for 20 milliseconds and then disappears, press ESC to exit
        if cv2.waitKey(10) & 0xFF == 27:
            break

    # Release video resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
