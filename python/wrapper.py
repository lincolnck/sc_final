from final import process_images, find_landmarks, scale_images, scale_landmarks, calculateDelaunayTriangles, constrainPoint, warpTriangle
import numpy as np
import cv2
from PIL import Image

def wrapper(file_path):
	images = process_images(file_path)
	allPoints = find_landmarks(file_path)
	scaled_images = (scale_images(images, allPoints))
	img = scaled_images[0]+scaled_images[1] / 2
	pointsAvg, pointsNorm = scale_landmarks(images, allPoints)
	width = 600
	height = 600
	# Delaunay triangulation
	rect = (0, 0, width, height);
	dt = calculateDelaunayTriangles(rect, np.array(pointsAvg));

	# Output image
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
		output = output + img

	# Divide by numImages to get average
	output = output / len(images);
	output = output * 255
	output = output.astype('uint8')
	cv2.imwrite('faces/average_face.png', output);
	

if __name__ == '__main__':
	wrapper('faces')