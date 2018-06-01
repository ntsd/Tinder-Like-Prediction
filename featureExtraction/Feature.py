import dlib
import math
import cv2
import face_recognition_models
import face_recognition
import numpy as np
from skimage.feature import hog


class Feature:
	def __init__(self, predictor_path='shape_predictor_68_face_landmarks.dat'):
		self.detector = dlib.get_frontal_face_detector()
		self.predictor = dlib.shape_predictor(predictor_path)
		
	def getFaceRects(self, img):
		dets = self.detector(img, 1)
		return dets

	def getBigestFaceRect(self, rects):
		bigest = lambda rect: rect.height() * rect.width()
		return max(rects, key=bigest)

	def getFaceShape(self, img, rect):
		# Mouth 0-16
		# Right eyebrow 17-21 
		# Left eyebrow 22-26
		# Nose 27-30
		# Nose Hole 31-35
		# Right eye 36-41
		# Left eye 42-47
		# Jaw 48-67
		shape = self.predictor(img, rect)
		return shape.parts() 

	def show(self):
		pass

	def angle(self, vector1, vector2):
		length1 = math.sqrt(vector1[0] * vector1[0] + vector1[1] * vector1[1])
		length2 = math.sqrt(vector2[0] * vector2[0] + vector2[1] * vector2[1])
		return math.acos((vector1[0] * vector2[0] + vector1[1] * vector2[1])/ (length1 * length2))

	def shape_to_directions_feature(self, shape):
		directions = []
		shapes = [shape[0:17],
					shape[17:22],
					shape[22:27],
					shape[27:31],
					shape[31:36],
					shape[36:42],
					shape[42:48],
					shape[48:]]
		for shape in shapes:
			ox, oy = shape[0]
			for x, y in shape[1:]:
				angle = self.angle([x, y], [ox, oy])
				directions.append(angle)
				ox, oy = x, y
		return directions

	def shape_to_distance_feature(self, shape):
		distances = []
		ox, oy = shape[0]
		for x, y in shape[1:]:
			dis = math.sqrt((ox-x)**2 + (oy-y)**2)
			distances.append(dis)
			ox, oy = x, y
		return distances

	def norm_size(self, img_path, points):
		img = cv2.imread(img_path)
		height, width, _ = img.shape
		# print(height, width)
		return [ [point.x/width, point.y/height] for point in points]

	def hog_feature(self, img, faceRect):
		# print(faceRect.tl_corner().x,faceRect.br_corner().x,faceRect.tl_corner().y,faceRect.br_corner().y)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# print(img.shape)
		crop_img = img[faceRect.tl_corner().y:faceRect.br_corner().y,faceRect.tl_corner().x:faceRect.br_corner().x]
		# print(crop_img.shape)
		img = cv2.resize(crop_img, (128, 128))
		scale_cell = (8, 8) #(img.shape[0]//100, img.shape[1]//100)
		fHOG1 = hog(img, orientations=8, pixels_per_cell=scale_cell)
		return fHOG1

	def getFeatureOld(self, path):
		img = dlib.load_rgb_image(path)
		rect_faces = self.getFaceRects(img)
		if not rect_faces:
			return None
		rectFace = self.getBigestFaceRect(rect_faces) # get bigest face
		faceShape = self.getFaceShape(img, rectFace) # get face shape
		normShape = self.norm_size(path, faceShape)
		# Features
		features = self.shape_to_directions_feature(normShape)
		features = self.shape_to_distance_feature(normShape)
		features = list(self.hog_feature(img, rectFace))
		features = list(self.hog_feature(img, rectFace)) + self.shape_to_directions_feature(normShape) + self.shape_to_distance_feature(normShape)
		return features

	def getFeature(self, path):
		img = dlib.load_rgb_image(path)
		face_bounding_boxes = face_recognition.face_locations(img)
		if len(face_bounding_boxes) == 0: # if face not found use np zeroes shape 128 
			return np.zeros(shape=(128))
		features = face_recognition.face_encodings(img, known_face_locations=face_bounding_boxes)[0]
		return features

if __name__ == '__main__':
	f = Feature()
	print(f.getFeature('image/too/mSQWlZdCq5b6ZLkmxrgVAJBa1cWF5QOh.jpg'))
