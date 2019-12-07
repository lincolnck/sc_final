'''
'''
from PIL import Image
import glob
import os
import numpy as np
import math
import cv2
import dlib

def get_images():
	image_path = input('Please input image folder name: ')
	return image_path

def process_images(image_path):
	'''
	Read in images
	'''
	images = []
	for f in glob.glob(os.path.join(image_path, "*")):
		image = cv2.imread(f)
		image = np.float32(image)/255.0
		images.append(image)
	return images
	
def find_landmarks(image_path):
	'''
	use dlib to find the 68 landmarks and output them in a
	list of lists of tuples
	'''
	predictor_path = 'shape_predictor_68_face_landmarks.dat'
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor(predictor_path)

	alllandmarks = []
	for f in glob.glob(os.path.join(image_path, "*")):
		img = dlib.load_rgb_image(f)
		dets = detector(img, 1)
		print(dets)
		print("Number of faces detected: {}".format(len(dets)))

		for k, d in enumerate(dets):
			shape = predictor(img, d)
			landmarks = []
			for point in range(0, shape.num_parts):
				landmarks.append((int(shape.part(point).x), int(shape.part(point).y)))
		alllandmarks.append(landmarks)
	return alllandmarks

def similarityTransform(inPoints, outPoints) :
	s60 = math.sin(60*math.pi/180);
	c60 = math.cos(60*math.pi/180);  
  
	inPts = np.copy(inPoints).tolist();
	outPts = np.copy(outPoints).tolist();
	
	xin = c60*(inPts[0][0] - inPts[1][0]) - s60*(inPts[0][1] - inPts[1][1]) + inPts[1][0];
	yin = s60*(inPts[0][0] - inPts[1][0]) + c60*(inPts[0][1] - inPts[1][1]) + inPts[1][1];
	
	inPts.append([np.int(xin), np.int(yin)]);
	
	xout = c60*(outPts[0][0] - outPts[1][0]) - s60*(outPts[0][1] - outPts[1][1]) + outPts[1][0];
	yout = s60*(outPts[0][0] - outPts[1][0]) + c60*(outPts[0][1] - outPts[1][1]) + outPts[1][1];
	
	outPts.append([np.int(xout), np.int(yout)]);
	
	tform = cv2.estimateAffinePartial2D(np.array([inPts]), np.array([outPts]));
	return tform[0]

def scale_images(images, alllandmarks, width=600, height=600):
	'''
	scale images
	'''
	eyecornerDst = [ (np.int(0.3 * width), np.int(height / 3)), (np.int(0.7 * width), np.int(height / 3)) ];

	numImages = len(images)
	
	# Warp images and trasnform landmarks to output coordinate system,
	# and find average of transformed landmarks.
	scaled_images = []
	for i in range(0, numImages):
		# Corners of the eye in input image
		eyecornerSrc  = [alllandmarks[i][36], alllandmarks[i][45]]
		# Compute similarity transform
		tform = similarityTransform(eyecornerSrc, eyecornerDst)
		scaled_images.append(cv2.warpAffine(images[i], tform, (width, height)))
	return scaled_images

def scale_landmarks(images, alllandmarks):
	width = 600
	height = 600
	pointsNorm = [];
	# Add boundary points for delaunay triangulation
	boundaryPts = np.array([(0,0), (width/2,0), (width-1,0), (width-1,height/2), ( width-1, height-1 ), ( width/2, height-1 ), (0, height-1), (0,height/2) ]);
	
	# Initialize location of average points to 0s
	pointsAvg = np.array([(0,0)]* ( len(alllandmarks[0]) + len(boundaryPts) ), np.float32());
	eyecornerDst = [ (np.int(0.3 * width), np.int(height / 3)), (np.int(0.7 * width), np.int(height / 3)) ];

	n = len(alllandmarks[0]);
	numImages = len(images)
	for i in range(0, numImages):
		eyecornerSrc  = [alllandmarks[i][36], alllandmarks[i][45]]
		# Compute similarity transform
		tform = similarityTransform(eyecornerSrc, eyecornerDst)
		points1 = alllandmarks[i]
		points2 = np.reshape(np.array(points1), (68,1,2));        
		
		points = cv2.transform(points2, tform);
		
		points = np.float32(np.reshape(points, (68, 2)));
		
		# Append boundary points. Will be used in Delaunay Triangulation
		points = np.append(points, boundaryPts, axis=0)
		
		# Calculate location of average landmark points.
		pointsAvg = pointsAvg + points / numImages;

		pointsNorm.append(points);
	return pointsAvg, pointsNorm

def rectContains(rect, point):
	if point[0] < rect[0] :
		return False
	elif point[1] < rect[1] :
		return False
	elif point[0] > rect[2] :
		return False
	elif point[1] > rect[3] :
		return False
	return True
	
def calculateDelaunayTriangles(rect, points):
	'''
	find the triangles
	'''
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
	p =  ( min( max( p[0], 0 ) , width - 1 ) , min( max( p[1], 0 ) , height - 1 ) )
	return p;
	

def applyAffineTransform(src, srcTri, dstTri, size) :
	
	# Given a pair of triangles, find the affine transform.
	warpMat = cv2.getAffineTransform( np.float32(srcTri), np.float32(dstTri) )
	
	# Apply the Affine Transform just found to the src image
	dst = cv2.warpAffine( src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

	return dst

def warpTriangle(img1, img2, t1, t2) :

	# Find bounding rectangle for each triangle
	r1 = cv2.boundingRect(np.float32([t1]))
	r2 = cv2.boundingRect(np.float32([t2]))

	# Offset points by left top corner of the respective rectangles
	t1Rect = [] 
	t2Rect = []
	t2RectInt = []

	for i in range(0, 3):
		t1Rect.append(((t1[i][0] - r1[0]),(t1[i][1] - r1[1])))
		t2Rect.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))
		t2RectInt.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))


	# Get mask by filling triangle
	mask = np.zeros((r2[3], r2[2], 3), dtype = np.float32)
	cv2.fillConvexPoly(mask, np.int32(t2RectInt), (1.0, 1.0, 1.0), 16, 0);

	# Apply warpImage to small rectangular patches
	img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
	
	size = (r2[2], r2[3])

	img2Rect = applyAffineTransform(img1Rect, t1Rect, t2Rect, size)
	
	img2Rect = img2Rect * mask

	# Copy triangular region of the rectangular patch to the output image
	img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] * ( (1.0, 1.0, 1.0) - mask )
	 
	img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] + img2Rect



def applyTriangle():
	pass

def warpImages():
	pass


if __name__ == '__main__':
	image_path = get_images()
	# Read points for all images
	images = process_images(image_path)
	print('Processing images. Please wait.')
	# print(images)
	alllandmarks = find_landmarks(image_path)
	print('Finding faces and landmark points.')
	# Read all images
	

	scaled_images = (scale_images(images, alllandmarks))
	img = scaled_images[0]+scaled_images[1] / 2

	pointsAvg, pointsNorm = scale_landmarks(images, alllandmarks)
	# cv2.imshow('im', img)
	# cv2.waitKey(0)

	width = 600
	height = 600
	# Delaunay triangulation
	rect = (0, 0, width, height);
	dt = calculateDelaunayTriangles(rect, np.array(pointsAvg));
	# print(dt)
	# # Output image
	output = np.zeros((height,width,3), np.float32());

	# Warp input images to average image landmarks
	for i in range(0, len(scaled_images)) :
		img = np.zeros((height,width,3), np.float32());
		# Transform triangles one by one
		for j in range(0, len(dt)) :
			tin = []; 
			tout = [];
			
			for k in range(0, 3) :                
				pIn = pointsNorm[i][dt[j][k]];
				pIn = constrainPoint(pIn, width, height);
				
				pOut = pointsAvg[dt[j][k]];
				pOut = constrainPoint(pOut, width, height);
				
				tin.append(pIn);
				tout.append(pOut);
			
			
			warpTriangle(scaled_images[i], img, tin, tout);


		# Add image intensities for averaging
		output = output + img;


	# Divide by numImages to get average
	output = output / len(images);

	# Display result
	cv2.imshow('image', output);
	cv2.waitKey(0);



