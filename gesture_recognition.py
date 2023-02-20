import cv2
import numpy as np
import argparse

bg = None

def run_avg(image, aWeight):
    global bg
    if bg is None:
        bg = image.copy().astype("float")
        return

    cv2.accumulateWeighted(image, bg, aWeight)


def segment(image, threshold=25):
    global bg

    diff = cv2.absdiff(bg.astype("uint8"), image)

    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]
    cnts, hiearchy = cv2.findContours(thresholded.copy(), 
                                        cv2.RETR_EXTERNAL, 
                                        cv2.CHAIN_APPROX_SIMPLE)

    if len(cnts) == 0:
        return
    else:
        segmented = max(cnts, key=cv2.contourArea)
        return (thresholded, segmented)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--thresh', type=int,
                        help='Use if you want do display thresholded image',
                        choices=range(0,2))
    return parser.parse_args() 

if __name__ == "__main__":

    args = parse_args()

    aWeight = 0.5

    # capturing webcam footage 
    camera = cv2.VideoCapture(0)

    # init frame count 
    num_frames = 0

    # init region of intrest ROI
    top, right, bottom, left = 100, 350, 325, 590

    while(True):
        # get the current frame
        (grabbed, frame) = camera.read()

        # flipping the image
        frame = cv2.flip(frame, 1)
        clone = frame.copy()

        # get the ROI
        roi = frame[top:bottom, right:left]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)


        if num_frames < 30:
            run_avg(gray, aWeight)
        else:
            # get segmented hand
            hand = segment(gray)

            if hand is not None:

                (thresholded, segmented) = hand

                hull = cv2.convexHull(segmented, returnPoints=False)
                hull2 = cv2.convexHull(segmented)
                hull[::-1].sort(axis=0)
                defects = cv2.convexityDefects(segmented, hull)
                cv2.drawContours(clone, [segmented + (right, top)], 
                                -1, (255, 0,0))
                tresh_deg = 80.0
                num_fingers = 1
                area = 0.0
                if defects is not None:
                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        start = tuple(segmented[s][0]+(right, top))
                        end = tuple(segmented[e][0]+(right, top))
                        far = tuple(segmented[f][0]+(right, top))

                        if (np.arctan2(np.linalg.norm(
                                        np.cross(np.subtract(start,far),
                                        np.subtract(end,far))),
                                       np.dot(
                                        np.subtract(start,far), 
                                        np.subtract(end,far))) < tresh_deg/180.0*np.pi):
                            num_fingers += 1
                            cv2.circle(clone, far, 5, [0, 0, 255], -1)
                        else:
                            cv2.circle(clone, far, 5, [0, 255, 0], -1)
                        cv2.line(clone, start, end, [0, 255, 0], 2)

                    areahull = cv2.contourArea(hull2)
                    areacont = cv2.contourArea(segmented)
                    arearatio = ((areahull-areacont)/areacont)*100
                    if(arearatio<15.0):
                        cv2.putText(clone, "0", (0, 100), cv2.FONT_ITALIC, 
                                    1, (255, 255, 255), 2, cv2.LINE_4)
                    else:
                        cv2.putText(clone,str(num_fingers),(0,100),cv2.FONT_ITALIC,
                                    1,(255,255,255),2,cv2.LINE_4)

                if args.thresh == 1:
                    window_name = "Thesholded"
                    cv2.namedWindow(window_name) 
                    cv2.moveWindow(window_name, 100,500)
                    cv2.imshow(window_name, thresholded)

        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)

        num_frames += 1
        cv2.imshow("Video Feed", clone)

        # monitor user's input
        keypress = cv2.waitKey(1) & 0xFF

        # pressing 'q' will stop the program
        if keypress == ord("q"):
            break
        # pressing 'r' will update background
        elif keypress ==ord("r"):
            bg = None
            num_frames = 0

    # stop camera recording
    camera.release()
    cv2.destroyAllWindows()
