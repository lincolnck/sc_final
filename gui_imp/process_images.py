# Software Carpentry Final Project
# Lincoln Kartchner
# process_images.py
'''
This script takes care of reading in image files for the
averager.py program, and checking to make sure they
won't cause problems.
It contains two functions:
    process_images
    face_check

Sources:
    http://dlib.net/face_landmark_detection.py.html
    stack overflow
'''
import os
import glob
import cv2
import numpy as np
import dlib
import sys
from PIL import Image


def process_images(imagesfp):
    """process_images takes in the images from a
    specified filepath and converts them into one list
    of image information to make working with them easier.
    If no images are found inside the folder, it will
    exit the program. Likewise, if only one image is found
    in the folder after the image check, then it will
    exit the program as at least two are needed to
    find an average face.

    **Parameters**
    imagesfp: str
        The name of the folder containing the images
        to be averaged

    **Returns**
    images: list
        A list of lists of numpy arrays
        corresponding to prespecified images
    """
    images = []
    for file in glob.glob(os.path.join(imagesfp, "*")):
        image = cv2.imread(file)
        image = np.float32(image)/255.0
        images.append(image)
    if not images:
        print("No image files found!")
        raise Exception
    if len(images) == 1:
        print("Only one image found. At least two are required!")
        raise Exception
    return images


def face_check(imagesfp):
    """face_check is used to perform
    a preliminary check on the images in the filepath
    to make sure that there won't be any problems down the line
    in the program. For example, if dlib is unable to detect a
    face in one of the images, it will remove it from the
    filepath so that it is not included in the face average.
    If dlib detects more than one face in an image, it will
    create new images corresponding to each face in the original image
    and then remove the original image, so that an accurate average
    can be found. If no faces are found in any of the images, it will
    exit the program.

    **Parameters**
    imagesfp: str
        The name of the folder containing the images
        to be averaged

    **Returns**
    None
    """
    detector = dlib.get_frontal_face_detector()
    detections = []
    for file in glob.glob(os.path.join(imagesfp, "*")):
        filename = file.split('/')[-1]
        image = dlib.load_rgb_image(file)
        imheight, imwidth, channels = image.shape
        faces = detector(image, 1)
        if not faces:
            print("Dlib was unable to detect a face in '{}'.".format(filename))
            print("'{}' will not be included in the final average face.".format(filename))
            os.remove(file)
        if len(faces) >= 2:
            print("Dlib detected two or more faces in '{}'.".format(filename))
            print("Copying image around each cropped face...")
            for k, d in enumerate(faces):
                img_new = image[max(0, d.top()):min(d.bottom(), imheight), max(0, d.left()):min(d.right(), imwidth)]
                dlib.save_image(img_new, os.path.join(imagesfp, 'newerface_{}.png'.format(k)))
            os.remove(file)
        detections.append(len(faces))
    if all(d == 0 for d in detections):
        print("Dlib was unable to detect a face in any of the images!")
        raise Exception

if __name__ == '__main__':
    pass
