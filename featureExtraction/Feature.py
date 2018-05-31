import dlib

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
		shape = self.predictor(img, rect)
		return shape.parts()

	def show(self):
		pass

	def getFeature(self, path):
		img = dlib.load_rgb_image(path)
		rect_faces = self.getFaceRects(img)
		if not rect_faces:
			return None
		rectFace = self.getBigestFaceRect(rect_faces)
		faceShape = self.getFaceShape(img, rectFace)
		return faceShape

if __name__ == '__main__':
	f = Feature()
	print(f.getFeature('image/too/mSQWlZdCq5b6ZLkmxrgVAJBa1cWF5QOh.jpg'))
