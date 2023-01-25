import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()

    cv.imshow('frame', frame)

    if cv.waitKey(1) == ord('q'):
        break




#img1 = cv.imread('IMG_4101.jpg')

#def rescaleImage(frame, scale=0.50):
#    width = int(frame.shape[1] * scale)
#    height = int(frame.shape[0] * scale)
#    dimensions = (width, height)
#    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

#re_img1 = rescaleImage(img1, scale=0.20)
#cv.imshow('image', re_img1)

#cv.waitKey(0)
#cv.destroyAllWindows()
