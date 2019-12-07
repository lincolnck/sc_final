# Software Carpentry Final Project
# Lincoln Kartchner
# landmark_map.py
'''
This script will find facial landmarks using dlib.
It contains two different functions:
    find_landmarks
    plot_landmarks

Sources:
    http://dlib.net/face_landmark_detection.py.html
    https://opencv.org
    stack overflow
'''
import os
import cv2
import dlib
import glob
from process_images import face_check


def find_landmarks(imagesfp, predictorfp='shape_predictor_68_face_landmarks.dat'):
    """find_landmarks uses the dlib software
    library to take in an image file and then
    return a list of coordinates of facial landmarks
    within that image. For more information read the
    DLIB documentation

    Modified from:
        http://dlib.net/face_landmark_detection.py.html

    **Parameters**
    imagesfp: str
        The filepath name containing images that should be processed
        to look for faces and corresponding facial landmarks
    predictorfp: str
        The filepath name containing the predictor file. Default is
        'shape_predictor_68_face_landmarks.dat' which is a pre-trained
        model created by dlib. Other models can be used, and personal
        models can be trained. Refer to dlib documentation for how to do this.

    **Returns**
    allllandmarks: list
        A list of lists of tuples corresponding to
        coordinates of specific facial landmarks for each face in
        each image file in the specified filepath.
    """
    predictor = dlib.shape_predictor(predictorfp)
    detector = dlib.get_frontal_face_detector()
    alllandmarks = []
    for file in glob.glob(os.path.join(imagesfp, "*")):
        image = dlib.load_rgb_image(file)
        face = detector(image, 1)
        for k, d in enumerate(face):
            shape = predictor(image, d)
            landmarks = []
            for point in range(0, shape.num_parts):
                landmarks.append((int(shape.part(point).x), int(shape.part(point).y)))
        alllandmarks.append(landmarks)
    return alllandmarks


def plot_landmarks(image, landmarks):
    """plot_landmarks uses opencv to plot the
    landmarks found from find_landmarks over the
    original image.

    **Parameters**
    image = str
        The filepath of the specific image you
        have landmarks for that you want to plot
        the landmarks over
    landmarks = list
        A list of tuples corresponding to
        facial landmarks in the image you have.
        These can be found using find_landmarks
        on the image specified.

    **Returns**
    image: the image with the specified
    landmarks plotted over it. It can be
    viewed with cv2.imshow(image) or saved
    with cv2.imwrite(image)
    """
    image = cv2.imread(image)
    for face in landmarks:
        for point in face:
            cv2.circle(image, point, 5, (255, 0, 255), -1)
    return image

if __name__ == '__main__':
    os.chdir('./static/images')
    landmarks = find_landmarks('curies.jpg')
    print(landmarks)
    image = plot_landmarks('curies.jpg', landmarks)
    image = image.astype('uint8')
    cv2.imwrite('curies_face_landmarks.png', image)
