# Software Carpentry Final Project
# Lincoln Kartchner
# transform.py
'''
This script takes care of the math behind the
face averaging. It contains seven different functions:
    similarity_transform
    rectContains
    calculateDelaunayTriangles
    constrainPoint
    applyAffineTransform
    warpTriangle
    image_transform

Sources:
    1. https://docs.opencv.org/3.4/d4/d61/tutorial_warp_affine.html
    2. https://github.com/spmallick/learnopencv/tree/master/FaceAverage
    3. stack exchange
'''
import math
import cv2
import numpy as np


def similarity_transform(inPoints, outPoints):
    """ similarity_transform takes in a set of input points
    and a set of output points and finds an affine transformation
    between the two. cv2.estimateAffinePartial2D requires
    a two sets of three coordinates in order to find an
    affine transformation between them. similarity_transform will
    take two sets of two coordinates and find the corresponding
    third coordinate by finding a point that forms an equilateral
    triangle with the original two points.

    For more information look at:
        https://docs.opencv.org/3.4/d4/d61/tutorial_warp_affine.html

    Source:
        https://github.com/spmallick/learnopencv/tree/master/FaceAverage

    **Parameters**

    inPoints: list
        A list of tuples, in this case corresponding to specific
        image coordinate pairs
    outPoints: list
        A list of tuples, in this case corresponding to specific
        image coordinate pairs

    **Returns**

    tform[0]: array
        A 2 x 3 matrix corresponding to the optimal affine
        transformation between the two sets of points.
    """
    s60 = math.sin(60*math.pi/180)
    c60 = math.cos(60*math.pi/180)
    inPts = np.copy(inPoints).tolist()
    outPts = np.copy(outPoints).tolist()
    xin = c60*(inPts[0][0] - inPts[1][0]) - s60*(inPts[0][1] - inPts[1][1]) + inPts[1][0]
    yin = s60*(inPts[0][0] - inPts[1][0]) + c60*(inPts[0][1] - inPts[1][1]) + inPts[1][1]
    inPts.append([np.int(xin), np.int(yin)])
    xout = c60*(outPts[0][0] - outPts[1][0]) - s60*(outPts[0][1] - outPts[1][1]) + outPts[1][0]
    yout = s60*(outPts[0][0] - outPts[1][0]) + c60*(outPts[0][1] - outPts[1][1]) + outPts[1][1]
    outPts.append([np.int(xout), np.int(yout)])
    tform = cv2.estimateAffinePartial2D(np.array([inPts]), np.array([outPts]))
    return tform[0]


def rectContains(rect, point):
    """ rectContains checks if a
    rectangle contains a given point.

    Source:
        https://github.com/spmallick/learnopencv/tree/master/FaceAverage

    **Parameters**
    rect: tuple
        A tuple containing the four points
        corresponding to the four corners of the
        rectangle.

    point: tuple
        A tuple corresponding to the coordinates
        of the given point

    **Returns**
    True if point is in rectangle
    False otherwise
    """
    if point[0] < rect[0]:
        return False
    elif point[1] < rect[1]:
        return False
    elif point[0] > rect[2]:
        return False
    elif point[1] > rect[3]:
        return False
    return True


def calculateDelaunayTriangles(points, width=600, height=600):
    """calculateDelaunayTriangles finds the
    Delaunay Triangulation of a set of points. The
    Delaunay Triangluation is a method of triangulation
    in which for a given set of P points, DT triangles are
    created so that no point in P is within the circumcircle
    of any DT.

    Source:
        https://github.com/spmallick/learnopencv/tree/master/FaceAverage

    **Parameters**
    points: list
        A list of tuples corresponding to the
        coordinates of specific image landmarks in a given image
    width: int
        The desired ouput image width. Default is 600.
    height: int
        The desired output image height. Default is 600.

    **Returns**
    delaunayTri: list
        A list of tuples corresponding to the triangles
        from any Delaunay Triangulation of a given set
        of image landmarks.
    """
    rect = (0, 0, width, height)
    subdiv = cv2.Subdiv2D(rect)

    for p in points:
        subdiv.insert((p[0], p[1]))

    triangleList = subdiv.getTriangleList()

    delaunayTri = []
    for t in triangleList:
        pt = []
        pt.append((t[0], t[1]))
        pt.append((t[2], t[3]))
        pt.append((t[4], t[5]))
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])
        if rectContains(rect, pt1) and rectContains(rect, pt2) and rectContains(rect, pt3):
            ind = []
            for j in range(0, 3):
                for k in range(0, len(points)):
                    if(abs(pt[j][0] - points[k][0]) < 1.0 and abs(pt[j][1] - points[k][1]) < 1.0):
                        ind.append(k)
            if len(ind) == 3:
                delaunayTri.append((ind[0], ind[1], ind[2]))
    return delaunayTri


def constrainPoint(p, width, height):
    """constrainPoint constrains a given
    point to be within specified dimensions

    Source:
        https://github.com/spmallick/learnopencv/tree/master/FaceAverage

    **Parameters**
    p: tuple
        A tuple correponding to a point coordinate
    width: int
        The desired ouput image width. Default is 600.
    height: int
        The desired output image height. Default is 600.

    **Returns**
    p: tuple
        The constrained point, now within the image boundaries
    """
    p = (min(max(p[0], 0), width - 1), min(max(p[1], 0), height - 1))
    return p


def applyAffineTransform(src, srcTri, dstTri, size):
    """applyAffineTransform takes in a source image,
    and a source triangle, and then finds the affine
    transformation between the source triangle and some
    target triangle.

    Sources:
        https://github.com/spmallick/learnopencv/tree/master/FaceAverage
        https://docs.opencv.org/3.4/d4/d61/tutorial_warp_affine.html

    **Parameters**
    src: list
        A list of tuples
    srcTri: list
        A list of tuples corresponding to the image
        triangles
    dstTri: list
        A list of tuples corresponding to the target
        triangles
    size: tuple
        A tuple corresponding to the size of the target
        image

    **Returns**
    dst: numpy array
        A numpy array of the warped image
    """
    # Given a pair of triangles, find the affine transform.
    warpMat = cv2.getAffineTransform(np.float32(srcTri), np.float32(dstTri))
    # Apply the Affine Transform just found to the src image
    dst = cv2.warpAffine(src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    return dst


def warpTriangle(img1, img2, t1, t2):
    """ warpTriangle takes care of matching
    warped triangles between sets of images

    Source:
        https://github.com/spmallick/learnopencv/tree/master/FaceAverage

    **Parameters**
    img1: numpy array
        A numpy array of the source image
    img2: numpy array
        A numpy array of the target image
    t1: list
        A list of tuples corresponding to
        specific points in the source image
    t2: list
        A list of tuples corresponding to
        specific points in the target image

    **Returns**

    None
    """
    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))

    # Offset points by left top corner of the respective rectangles
    t1Rect = []
    t2Rect = []
    t2RectInt = []

    for i in range(0, 3):
        t1Rect.append(((t1[i][0] - r1[0]), (t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))
        t2RectInt.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))

    # Get mask by filling triangle
    mask = np.zeros((r2[3], r2[2], 3), dtype=np.float32)
    cv2.fillConvexPoly(mask, np.int32(t2RectInt), (1.0, 1.0, 1.0), 16, 0)

    # Apply warpImage to small rectangular patches
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    size = (r2[2], r2[3])
    img2Rect = applyAffineTransform(img1Rect, t1Rect, t2Rect, size)
    img2Rect = img2Rect * mask
    # Copy triangular region of the rectangular patch to the output image
    img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] * ((1.0, 1.0, 1.0) - mask)
    img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] + img2Rect


def image_transform(scaled_images, pointsNorm, pointsAvg, dt, width=600, height=600):
    """image_transform uses the helper functions above
    to actually transform specific images to a target space

    Modified from:
        https://github.com/spmallick/learnopencv/tree/master/FaceAverage

    **Parameters**
    scaled_images: list
        A list of tuples corresponding to the
        coordinates of facial landmarks from
        individual images scaled to a common space
    pointsNorm: list
        A list of tuples corresponding to the
        norm of all the coordinates of facial landmarks
        from all the images in the original filepath
    pointsAvg: list
        A list of tuples corresponding to the
        average of all the coordinates of facial landmarks
        from all the images in the original filepath
    dt: list
        A list of tuples corresponding to the triangles
        from any Delaunay Triangulation of a given set
        of image landmarks.
    width: int
        The desired ouput image width. Default is 600.
    height: int
        The desired output image height. Default is 600.

    **Returns**
    output: numpy array
        A numpy array corresponding to the final
        face average image
    """
    output = np.zeros((height, width, 3), np.float32())
    for i in range(len(scaled_images)):
        img = scaled_images[i]/len(scaled_images)
    # Warp input images to average image landmarks
    for i in range(0, len(scaled_images)):
        img = np.zeros((height, width, 3), np.float32())
        # Transform triangles one by one
        for j in range(0, len(dt)):
            tin = []
            tout = []
            for k in range(0, 3):
                pIn = pointsNorm[i][dt[j][k]]
                pIn = constrainPoint(pIn, width, height)
                pOut = pointsAvg[dt[j][k]]
                pOut = constrainPoint(pOut, width, height)
                tin.append(pIn)
                tout.append(pOut)
            warpTriangle(scaled_images[i], img, tin, tout)
        # Add image intensities for averaging
        output += img
    # Divide by number of images to get average
    output = output / len(scaled_images)
    return output


if __name__ == '__main__':
    pass
