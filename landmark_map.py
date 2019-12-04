'''
'''
import os
import cv2
import dlib 

def find_landmarks(image_path, predictor_path):
	'''
	use dlib to find the 68 landmarks and output them in a
	list of lists of tuples
	'''
	# predictor_path = 'shape_predictor_68_face_landmarks.dat'
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor(predictor_path)
	img = dlib.load_rgb_image(image_path)
	dets = detector(img, 1)
	print("Number of faces detected: {}".format(len(dets)))
	alllandmarks = []
	for k, d in enumerate(dets):
		shape = predictor(img, d)
		landmarks = []
		for point in range(0, shape.num_parts):
			landmarks.append((int(shape.part(point).x), int(shape.part(point).y)))
		alllandmarks.append(landmarks)
	return alllandmarks

def plot_landmarks(image, landmarks):
	'''
	'''
	image = cv2.imread(image)
	for face in landmarks:
		for point in face:
			cv2.circle(image, point, 5, (255, 0, 255), -1)
	return image

if __name__ == '__main__':
	os.chdir('./static/images')
	landmarks = find_landmarks('curies.jpg', '../../shape_predictor_68_face_landmarks.dat')
	print(landmarks)
	image = plot_landmarks('curies.jpg', landmarks)
	# image = image * 255
	image = image.astype('uint8')
	cv2.imwrite('curies_face_landmarks.png', image);
