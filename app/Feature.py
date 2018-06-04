import face_recognition_models
import face_recognition
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.feature import hog

class Feature:
    """
    Feature:
    - face shape:
        Mouth 0-16
        Right eyebrow 17-21 
        Left eyebrow 22-26
        Nose 27-30
        Nose Hole 31-35
        Right eye 36-41
        Left eye 42-47
        Jaw 48-67
    - face colors:
        Gabor filter
    """
    def __init__(self):
        pass

    def getBigestFaceRect(self, rects):
        bigest = lambda rect: rect[2]-rect[0] * rect[1]-rect[3] # (top, right, bottom, left)
        return max(rects, key=bigest)

    def colorFeature(self, img):
        # plt.imshow(img)
        # plt.show()
        colorsFeatures = np.array([])

        # color RGB feature
        chans = cv2.split(img)
        for chan in chans:
            hist = cv2.calcHist([chan], [0], None, [8], [0, 256])
            hist = hist/hist.sum()
            colorsFeatures = np.append(colorsFeatures, hist[:,0])

        # hsv only s channel
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        chans = cv2.split(hsv)  # take the S channel
        S = chans[1]
        hist2 = cv2.calcHist([S], [0], None, [8], [0, 256])
        hist2 = hist2/hist2.sum()
        colorsFeatures = np.append(colorsFeatures, hist2[:,0])

        return colorsFeatures


    def hogFeature(self, img):
        def rgb2gray(rgb):
            return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])
        img = rgb2gray(img)
        # plt.imshow(img, cmap = plt.get_cmap('gray'))
        # plt.show()
        img = cv2.resize(img, (128, 128))
        scale_cell = (8, 8) #(img.shape[0]//100, img.shape[1]//100) 
        fhog = hog(img, orientations=8, pixels_per_cell=scale_cell)
        return fhog

    def getFeature(self, path):
        """
        Input: Image path
        Output: np.array
        """
        img = face_recognition.load_image_file(path)
        face_rects = face_recognition.face_locations(img) # return (top, right, bottom, left)
        if len(face_rects) == 0: # if face not found use np zeroes shape 128 
            return None
        features = np.array([])

        bigest_face_rect= self.getBigestFaceRect(face_rects)
        # add face shape feature
        features = np.append(features, face_recognition.face_encodings(img, known_face_locations=[bigest_face_rect])[0]) 

        # faceImage = img[bigest_face_rect[0]:bigest_face_rect[2],bigest_face_rect[3]:bigest_face_rect[1]]
        # features = np.append(features, self.colorFeature(faceImage)) # add colors feature

        # features = np.append(features, self.hogFeature(faceImage)) # add hog feature (still bug)

        return features

if __name__ == '__main__':
    f = Feature()
    print(f.getFeature('image/too/mSQWlZdCq5b6ZLkmxrgVAJBa1cWF5QOh.jpg'))
