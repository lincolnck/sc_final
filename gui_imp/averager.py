import cv2
import os
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
    cv2.imwrite('static/outputimage/average_face.png', output)
    # os.chdir('./static/faces')
    # for file in os.listdir('.'):
    #     print(file)
    #     if file.endswith('.jpg'):
    #         os.remove(file)
    #     elif file.endswith('.tiff'):
    #         os.remove(file)
    #     elif file.endswith('.jpeg'):
    #         os.remove(file)
    #     elif file.endswith('.jpg'):
    #         os.remove(file)
    #     else:
    #         continue
    # os.chdir('../..')
    
if __name__ == '__main__':
    main('./static/faces')