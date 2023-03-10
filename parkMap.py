import argparse
import yaml
import cv2 as open_cv
import numpy as np
import logging
from drawing_utils import draw_contours
# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
# Importing Libraries
import serial
import time
arduino = serial.Serial(port='', baudrate=115200, timeout=.1)
#pursuit = False
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)

def getGridCoordinate(mappy, location):
    current_x = location[0]
    current_y = location[1]
    for i in range(0, len(mappy)):
        for j in range(0, len(mappy[0])):
            if(current_x <= mappy[i][j][0] and current_y <= mappy[i][j][1]):
                if mappy[i][j][2] == 1:
                    return i, j, 1
                else:
                    return i,j,0
    return 0, 0, 1


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower =(95, 50, 50)  #(162, 99, 49) 
greenUpper = (110, 255, 255) #(162, 99, 98) 
pts = deque(maxlen=args["buffer"])

def main():
    pursuit = False
    logging.basicConfig(level=logging.INFO)

    args = parse_args()
    
    data_file = args.data_file

    with open(data_file, "r") as data:
        points = yaml.safe_load(data)
        detector = LotBorders(points)
        detector.lotOutline()

class LotBorders:
    def __init__(self,  coordinates):
     
        self.coordinates_data = coordinates
     
        self.contours = []
        self.bounds = []
        self.mask = []

    def lotOutline(self):
        mappy = [[(180, 126, 1), (455, 126, 0), (620, 126, 1), (915, 126, 0), (1076, 126, 1)],
            [(180, 253, 1), (455, 253, 0), (620, 253, 1), (915, 253, 0), (1076, 253, 1)],
            [(180, 379, 1), (455, 379, 0), (620, 379, 1), (915, 379, 0), (1076, 379, 1)],
            [(180, 505, 1), (455, 505, 0), (620, 505, 1), (915, 505, 0), (1076, 505, 1)],
            [(180, 690, 1), (455, 690, 0), (620, 690, 0), (915, 690, 0), (1076, 690, 0)],
            [(180, 840, 1), (455, 840, 1), (620, 840, 1), (915, 840, 1), (1076, 840, 1)]]

        occupancy = {
            '1': [(0, 0), 0],
            '2': [(1, 0), 0],
            '3': [(2, 0), 0],
            '4': [(3, 0), 0],
            '5': [(0, 2), 0],
            '6': [(1,2), 0],
            '7': [(2,2), 0],
            '8': [(3,2), 0],
            '9': [(0,4), 0],
            '10':[(1,4), 0],
            '11':[(2,4), 0],
            '12':[(3,4), 0]
        }

        priority = ['1', '5', '9', '2', '6', '10', '3', '7', '11', '4', '8', '12']
        priority_tracker = 0
        stop = False
        pursuit = False
        capture = open_cv.VideoCapture(0)
    
        coordinates_data = self.coordinates_data


        for p in coordinates_data:
            coordinates = self._coordinates(p)
           
        vs = capture
        # allow the camera or video file to warm up
        time.sleep(2.0)
        frame_counter = 0
        while capture.isOpened():
            result, frame = capture.read()

            frame = frame[0:840, 844:1920]
            if frame is None:
                break

            if not result:
                raise CaptureReadError("Error reading video capture on frame %s" % str(frame))

            new_frame = frame.copy()
            logging.debug("new_frame: %s", new_frame)

            position_in_seconds = capture.get(open_cv.CAP_PROP_POS_MSEC) / 1000.0


            for _, p in enumerate(coordinates_data):
                coordinates = self._coordinates(p)

                # color = COLOR_GREEN if statuses[index] else COLOR_BLUE
                draw_contours(new_frame, coordinates, str(p["id"] + 1), (0,0,0), (0,0,0))

            
             # grab the current frame
            frame = new_frame
            # handle the frame from VideoCapture or VideoStream
            frame = frame[1] if args.get("video", False) else frame
            # if we are viewing a video and we did not grab a frame,
            # then we have reached the end of the video
            if frame is None:
                break
            # resize the frame, blur it, and convert it to the HSV
            # color space
            #frame = imutils.resize(frame, width=600)
            blurred = open_cv.GaussianBlur(frame, (11, 11), 0)
            hsv = open_cv.cvtColor(blurred, open_cv.COLOR_BGR2HSV)
            # construct a mask for the color "green", then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
            mask = open_cv.inRange(hsv, greenLower, greenUpper)
            mask = open_cv.erode(mask, None, iterations=2)
            mask = open_cv.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = open_cv.findContours(mask.copy(), open_cv.RETR_EXTERNAL,
                open_cv.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            center = None
            # only proceed if at least one contour was found
            if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                
                c = max(cnts, key=open_cv.contourArea)
                ((x, y), radius) = open_cv.minEnclosingCircle(c)
                M = open_cv.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                # Use this center as the center of the detected object (color-wise)
                #print(center)
                
                # only proceed if the radius meets a minimum size
                if radius > 10:
                    frame_counter += 1
                    if(frame_counter > 30 and pursuit == False and stop == False):
                        #write_read(priority[priority_tracker])
                        print('Starting')
                        pursuit = True
                        target = occupancy[priority[priority_tracker]][0]
                        print(target)
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    #open_cv.circle(frame, (int(x), int(y)), int(radius),S
                    #	(0, 255, 255), 2)
                    grid_y, grid_x, isLot = getGridCoordinate(mappy, center)
                    #print('Grid X: ', grid_x, ' Grid Y: ', grid_y, ' Is a lot: ', isLot)
                    
                    if(pursuit and (center[0] <= mappy[target[1]][target[0]][0]) and (center[1] <= mappy[target[1]][target[0]][1])):
                        print('Arrival')
                        write_read('-1')
                        occupancy[priority[priority_tracker]][1] = 1
                        pursuit = False
                        stop = True
                        frame_counter = 0
                        priority_tracker += 1
                    open_cv.circle(frame, center, 10, (0, 0, 255), -1)
            # update the points queue
            pts.appendleft(center)
            
            open_cv.imshow("video", frame)
            k = open_cv.waitKey(1)
            if k == ord("q"):
                break


        # if we are not using a video file, stop the camera video stream
        if not args.get("video", False):
            vs.stop()
        # otherwise, release the camera
        else:
            vs.release()
        # close all windows

        capture.release()
        open_cv.destroyAllWindows()

    def __apply(self, grayed, index, p):
        coordinates = self._coordinates(p)
        logging.debug("points: %s", coordinates)

    @staticmethod
    def _coordinates(p):
        return np.array(p["coordinates"])

 

class CaptureReadError(Exception):
    pass


def parse_args():
    parser = argparse.ArgumentParser(description='Generates Coordinates File')

    parser.add_argument("--data",
                        dest="data_file",
                        required=False,
                        default="data/coordinates_1.yml",
                        help="Data file to be used with OpenCV")

    return parser.parse_args()

if __name__ == "__main__":
    main()