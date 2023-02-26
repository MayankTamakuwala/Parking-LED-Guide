import cv2
import csv
import collections
import numpy as np
from tracker import EuclideanDistTracker

# Setup tracking 
tracker = EuclideanDistTracker()
confThreshold = 0.1
nmsThreshold = 0.2

# Middle cross line position
middle_line_position = 225
up_line_position = middle_line_position - 15
down_line_position = middle_line_position + 15

# COCO Names
classesFile = 'coco.names'
classNames = open(classesFile).read().strip().split('\n')
#print(classNames)
print('Number of classes: ', len(classNames))

# Load Yolo Detection Model
modelConfiguration = 'yolov3.cfg'
modelWeights = 'yolov3.weights'
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Set bounding box colors
np.random.seed(42)
colors = np.random.randint(0, 255, size=(len(classNames), 3), dtype='uint8')

# Initialize video capture

# Define real time detection
def realTime():
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        #img = process_image(img)
        img = cv2.resize(img,(0,0),None,0.5,0.5)
        ih, iw, channels = img.shape
        # Draw crossing lines
        cv2.line(img, (0, middle_line_position), (iw, middle_line_position), (255,0,255),1)
        cv2.line(img, (0, up_line_position), (iw, up_line_position), (0,0,255), 1)
        cv2.line(img, (0, down_line_position), (iw, down_line_position), (0,0,255), 1)
        # Show frames
        cv2.imshow('output', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def process_image(img):
    # Resize
    image =cv2.resize(img, (416, 416), interpolation=cv2.INTER_CUBIC)
    image = np.array(image, dtype='float')
    image /= 255.
    image = np.expand_dims(image, axis=0)
    return image


    
        
if __name__ == '__main__':
    print('Main Start')
    realTime()