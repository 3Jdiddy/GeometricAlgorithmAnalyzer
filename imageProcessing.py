import cv2
import os
import numpy as np
from triangulation import Delaunay2D


def findTriangulation(imgPath):
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (0, 0), fx=0.40, fy=0.40)
    # Threshold the image to create a binary image
    _, thresholded = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(
        thresholded, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    """
    Here I define the minimum and maximum size for the dots
    I made sure the the min and max dot size scales with the size of our image.
    Looks confusing, but its just based on a control I crunched some numbers on
    The important thing is to make sure the dot size boundries on dependent on the size of the image.
    A dot of size 50x50px could be resonable on an 2500x2500px image, but on a 100x100 image, it would be far too big.
    """
    dimensions = img.shape
    min_dot_size = np.sqrt((0.005* (dimensions[0] * dimensions[1])))
    max_dot_size = np.sqrt((0.36* (dimensions[0] * dimensions[1])))
    points = []

    # Filter through detected dots to remove garbage (based on size)
    # And add the center of these verified dots to a new set called points
    for contour in contours:
        if min_dot_size <= cv2.contourArea(contour) <= max_dot_size:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            points.append(center)

    #convexHull = ja.convexHull(points, len(points))
 
    for point in points:
        cv2.circle(img, point, int(min_dot_size/10), (0, 255, 0), 2)

    # computing triangles of our filterd set of points
    dt = Delaunay2D()
    for point in points:
        dt.addPoint(point)
    triangles = dt.exportTriangles()


    for triangle in triangles:
        img = cv2.line(img, points[triangle[0]],
                       points[triangle[1]], (0, 0, 0), 1)
        img = cv2.line(img, points[triangle[0]],
                       points[triangle[2]], (0, 0, 0), 1)
        img = cv2.line(img, points[triangle[1]],
                       points[triangle[2]], (0, 0, 0), 1)

    #Create the edited img file that will be swaped with our inputted one
    cv2.imwrite("newIMG.jpg", img)

if __name__ == "__main__":
    findTriangulation('IMG_4102.png')
    
