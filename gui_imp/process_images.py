'''
'''
import os
import glob
import cv2
import numpy as np
import dlib


def process_images(imagesfp):
    '''
    '''
    images = []
    for file in glob.glob(os.path.join(imagesfp, "*")):
        image = cv2.imread(file)
        image = np.float32(image)/255.0
        images.append(image)
    return images


def face_check(imagesfp):
    '''
    '''
    detector = dlib.get_frontal_face_detector()
    detections = []
    for file in glob.glob(os.path.join(imagesfp, "*")):
        image = dlib.load_rgb_image(file)
        faces = detector(image, 1)
        detections.append(len(faces))
    return detections

if __name__ == '__main__':
    pass
