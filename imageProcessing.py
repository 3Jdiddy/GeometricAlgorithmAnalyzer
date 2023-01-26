import cv2
import os
import numpy as np
import jarvisAlgorithm as ja
from triangulation import Delaunay2D


def findHull(imgPath):
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (0, 0), fx=0.40, fy=0.40)
    # Threshold the image to create a binary image
    _, thresholded = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(
        thresholded, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Define the minimum and maximum size for the dots
    min_dot_size = 50
    max_dot_size = 1000
    points = []

    # Filter through detected dots to remove garbage (based on size)
    # And add the center of these verified dots to a new set called points
    for contour in contours:
        if min_dot_size <= cv2.contourArea(contour) <= max_dot_size:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            points.append(center)

    #convexHull = ja.convexHull(points, len(points))
    print(points)
    for point in points:
        cv2.circle(img, point, 5, (0, 255, 0), 2)

    # computing triangles of our filterd set of points
    dt = Delaunay2D()
    for point in points:
        dt.addPoint(point)
    triangles = dt.exportTriangles()
    print(dt.exportTriangles())

    for triangle in triangles:
        img = cv2.line(img, points[triangle[0]],
                       points[triangle[1]], (0, 0, 0), 3)
        img = cv2.line(img, points[triangle[0]],
                       points[triangle[2]], (0, 0, 0), 3)
        img = cv2.line(img, points[triangle[1]],
                       points[triangle[2]], (0, 0, 0), 3)

    cv2.imshow("Black Dots", img)
    #newIMG = cv2.imwrite('newImg.jpg', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    findHull('IMG_4102.png')
    try:
        os.remove(
            '/home/joneseaw/code/compGeo/GeometricAlgorithmAnalyzer/newImg.jpg')
    except:
        pass
