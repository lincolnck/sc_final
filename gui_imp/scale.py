# Software Carpentry Final Project
# Lincoln Kartchner
# scale.py
'''
This script takes care of scaling images and landmarks
to a common space to allow for averaging and proper
transformations.

Source:
    https://github.com/spmallick/learnopencv/tree/master/FaceAverage
'''
import numpy as np
import cv2
from transform import similarity_transform

width = 600
height = 600


def scale_images(images, alllandmarks):
    """scale_images takes in images and then
    transforms all the images to a common space.

    Modified from source:
        https://github.com/spmallick/learnopencv/tree/master/FaceAverage

    **Parameters**
    images: list
        A list of lists of numpy arrays
        corresponding to prespecified images
    alllandmarks: list
        A list of lists of tuples correpsonding
        to facial landmarks for each of the images
        in the images list

    **Returns**
    scaled_images: list
        A list of tuples corresponding to the
        coordinates from individual images scaled
        to a common space
    """
    eyecornerDst = [(np.int(0.3 * width), np.int(height / 3)), (np.int(0.7 * width), np.int(height / 3))]
    numImages = len(images)
    # Warp images and trasnform landmarks to output coordinate system,
    scaled_images = []
    for i in range(0, numImages):
        # Corners of the eye in input image
        eyecornerSrc = [alllandmarks[i][36], alllandmarks[i][45]]
        # Compute similarity transform
        tform = similarity_transform(eyecornerSrc, eyecornerDst)
        scaled_images.append(cv2.warpAffine(images[i], tform, (width, height)))
    return scaled_images


def scale_landmarks(images, alllandmarks):
    """scale_images takes in images and then
    transforms all the images to a common space.

    Modified from source:
        https://github.com/spmallick/learnopencv/tree/master/FaceAverage

    **Parameters**
    images: list
        A list of lists of numpy arrays
        corresponding to prespecified images
    alllandmarks: list
        A list of lists of tuples correpsonding
        to facial landmarks for each of the images
        in the images list

    **Returns**
    pointsNorm: list
        A list of tuples corresponding to the
        norm of all the coordinates of facial landmarks
        from all the images in the original filepath
    pointsAvg: list
        A list of tuples corresponding to the
        average of all the coordinates of facial landmarks
        from all the images in the original filepath
    """
    pointsNorm = []
    # Add boundary points for delaunay triangulation
    boundaryPts = np.array([(0, 0), (width/2, 0), (width-1, 0), (width-1, height/2), (width-1, height-1), (width/2, height-1), (0, height-1), (0, height/2)])
    # Initialize location of average points to 0s
    pointsAvg = np.array([(0, 0)] * (len(alllandmarks[0]) + len(boundaryPts)), np.float32())
    eyecornerDst = [(np.int(0.3 * width), np.int(height / 3)), (np.int(0.7 * width), np.int(height / 3))]

    n = len(alllandmarks[0])
    numImages = len(images)
    for i in range(0, numImages):
        eyecornerSrc = [alllandmarks[i][36], alllandmarks[i][45]]
        # Compute similarity transform
        tform = similarity_transform(eyecornerSrc, eyecornerDst)
        points1 = alllandmarks[i]
        points2 = np.reshape(np.array(points1), (68, 1, 2))
        points = cv2.transform(points2, tform)
        points = np.float32(np.reshape(points, (68, 2)))
        # Append boundary points. Will be used in Delaunay Triangulation
        points = np.append(points, boundaryPts, axis=0)
        # Calculate location of average landmark points.
        pointsAvg = pointsAvg + points / numImages
        pointsNorm.append(points)
    return pointsAvg, pointsNorm

if __name__ == '__main__':
    pass
