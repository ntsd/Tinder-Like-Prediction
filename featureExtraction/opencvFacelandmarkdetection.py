#https://www.pyimagesearch.com/2018/04/02/faster-facial-landmark-detector-with-dlib/
import sys
import os
import dlib
import glob


predictor_path = "shape_predictor_68_face_landmarks.dat"
faces_folder_path = "image/"#sys.argv[2]

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
win = dlib.image_window()

for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
    print("Processing file: {}".format(f))
    img = dlib.load_rgb_image(f)


    win.clear_overlay()
    win.set_image(img)

    # Ask the detector to find the bounding boxes of each face. The 1 in the
    # second argument indicates that we should upsample the image 1 time. This
    # will make everything bigger and allow us to detect more faces.
    dets = detector(img, 1)
    print("Number of faces detected: {}".format(len(dets)))
    for k, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
        # Get the landmarks/parts for the face in box d.
        shape = predictor(img, d)
        print(shape)
        print("Part 0: {}, Part 1: {} ...".format(shape.part(0),
                                                  shape.part(1)))
       	print(shape.parts(), len(shape.parts()))

        # Draw the face landmarks on the screen.
        win.add_overlay(shape)

    win.add_overlay(dets)

    dlib.hit_enter_to_continue()
    # break