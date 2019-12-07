# Software Carpentry Final Project
# Lincoln Kartchner
# averager.py
'''
This script imports all the necessary modules in order to
find an 'average' face from all faces in the images in a
specified folder.

Sources:
    1. http://dlib.net/face_landmark_detection.py.html
    2. https://github.com/spmallick/learnopencv/tree/master/FaceAverage
    3. stack exchange
'''
import cv2
import numpy as np
from process_images import face_check, process_images
from landmark_map import find_landmarks
from scale import scale_images, scale_landmarks
from transform import calculateDelaunayTriangles, warpTriangle, image_transform


def main(image_path):
    """ Main runs the program to average the
    faces in a given file path, displaying
    the 'average' face at the end.

    **Parameters**

    image_path: str
        A string indicating the filepath containing
        the images to be 'averaged'

    **Returns**

    None
    """
    print('Opening {} and checking for faces...'.format(image_path))
    print('Processing images...')
    face_check(image_path)
    images = process_images(image_path)
    print('Finding facial landmarks...')
    allandmarks = find_landmarks(image_path)
    print('Scaling images to common space...')
    scaled_images = scale_images(images, allandmarks)
    pointsAvg, pointsNorm = scale_landmarks(images, allandmarks)
    print('Triangulating points...')
    dt = calculateDelaunayTriangles(np.array(pointsAvg))
    print('Averaging faces...')
    output = image_transform(scaled_images, pointsNorm, pointsAvg, dt)
    print('Success!')
    cv2.imshow('image', output)
    cv2.waitKey(0)

if __name__ == '__main__':
    image_path = input("Please enter the name of a folder containing images: ")
    main(image_path)
