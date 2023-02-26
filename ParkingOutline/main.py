import argparse
import yaml
import cv2 as open_cv
import numpy as np
import logging
from drawing_utils import draw_contours
from colors import COLOR_RED, COLOR_WHITE, COLOR_BLUE


# from motion_detector import MotionDetector

from colors import *
import logging


def main():
    logging.basicConfig(level=logging.INFO)

    args = parse_args()

    
    data_file = args.data_file
   

    

    with open(data_file, "r") as data:
        points = yaml.safe_load(data)
        detector = MotionDetector(points)
        detector.detect_motion()

class MotionDetector:
    def __init__(self,  coordinates):
     
        self.coordinates_data = coordinates
     
        self.contours = []
        self.bounds = []
        self.mask = []

    def detect_motion(self):
        
        capture = open_cv.VideoCapture(0)
    
        coordinates_data = self.coordinates_data


        for p in coordinates_data:
            coordinates = self._coordinates(p)
            

            rect = open_cv.boundingRect(coordinates)
           

  

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


            for index, p in enumerate(coordinates_data):
                coordinates = self._coordinates(p)

                # color = COLOR_GREEN if statuses[index] else COLOR_BLUE
                draw_contours(new_frame, coordinates, str(p["id"] + 1), COLOR_WHITE, COLOR_RED)

            open_cv.imshow("video", new_frame)
            k = open_cv.waitKey(1)
            if k == ord("q"):
                break
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


if __name__ == '__main__':
    main()
