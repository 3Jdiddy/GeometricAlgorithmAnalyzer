import cv2
import sys
import numpy as np
from triangulation import Delaunay2D


def cameraOn():  # add camera argument later
    # camera argument will replace 0, if we get that far
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()  # frame is the image itself (an individual frame)

        cv2.imwrite('frameIMG.jpg', frame)
        cv2.imshow('frame', frame)
        break
    cap.release()
    cv2.destroyAllWindows()


        # temparary break function-- I will integrate this better with a button in the GUI in the future
        #if cv2.waitKey(1) == ord('q'):
        #    break

    #cap.release()
    #cv2.destroyAllWindows()


# This didn't work well as an alternative, so it is unused for now.
def templateMatching():
    img_rgb = cv2.imread('IMG_4100.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('point1.jpg', 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    cv2.imwrite('res.png', img_rgb)


def findTriangulation(imgPath):
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    if img is None:
        sys.exit("Could not read the image.")
    #img = cv2.resize(img, (0, 0), fx=0.40, fy=0.40)
    # Threshold the image to create a binary image
    _, thresholded = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

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
    min_dot_size = (0.0000963 * (dimensions[0] * dimensions[1]))*0.6
    max_dot_size = (0.00140604253 * (dimensions[0] * dimensions[1]))*1.40
    points = []

    # Filter through detected dots to remove garbage (based on size)
    # And add the center of these verified dots to a new set called points

    #print(f"The dimensions are {dimensions}")
    #print("----------------------------")
    for contour in contours:
        if min_dot_size <= cv2.contourArea(contour) <= max_dot_size:
            if cv2.arcLength(contour, True) < max_dot_size:
                #print(f"The dot size is: {cv2.contourArea(contour)}")
                #print(f"The arcLength is: {cv2.arcLength(contour, True)}")
                (x, y), radius = cv2.minEnclosingCircle(contour)
                center = (int(x), int(y))
                points.append(center)

    #print(f"The min_dot_size is: {min_dot_size}")
    #print(f"The max_dot_size is: {max_dot_size}")
    #print("----------------------------")

    for point in points:
        cv2.circle(img, point, int(np.sqrt(min_dot_size)), (0, 255, 0), 2)
    #img = cv2.resize(img, (0, 0), fx=0.40, fy=0.40)
    #thresholded = cv2.resize(thresholded, (0, 0), fx=0.40, fy=0.40)
    #cv2.imshow('test', img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #cv2.imshow('test', thresholded)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #img = cv2.drawContours(img, contours, -1, (0,255,75), 2)
    #cv2.imshow('test', img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

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

    # Create the edited img file that will be swaped with our inputted one
    cv2.imwrite("newIMG.jpg", img)


def convexHull(img):
    #importing the image
    img = cv2.imread(img)

    if img is None:
        sys.exit("Could not read the image.")

    #locating the contours to find the points
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #removing the image border from the contours so it is only the points
    point_contours = contours[1:]
    pts = []

    #for each contour, finding the average x and y values to find the center of the points
    for i in point_contours:
        total_point = np.sum(i, axis = 0)[0]
        num = len(i)
        temp = [int(total_point[0]/num), int(total_point[1]/num)]
        pts.append(temp)

    #functions for finding the cross product of 3 points and if it is a convex or reflex angle
    #Adapted from class notes
    def signedArea(a,b,c):
        cross = (((b[0] - a[0])*(c[1] - a[1])) - ((b[1] - a[1])*(c[0] - a[0])))
        return cross

    def leftOf(a,b,c):
        if signedArea(a,b,c) > 0:
            return True
        else:
            return False
        
    def leftOn(a,b,c):
        if signedArea(a,b,c) >= 0:
            return True
        else:
            return False

    #function to find the lowest point in the set
    def lowest(s):
        btm = s[0]
        
        for i in s:
            if i[1] <= btm[1]:
                if i[1] == btm[1]:
                    if i[0] > btm[0]:
                        btm = i
                else:
                    btm = i
        return btm


    def sortY(s):
        return s[1]

    sortedPts = pts.copy()
    #sorts points by descending x value
    sortedPts.sort(reverse = True)
    #sort points by y value
    sortedPts.sort(key = sortY)

    #Gift Wrapping algorithm
    #Adapted from class notes
    def giftWrapping(s):
        startPoint = lowest(s)
        hull = [startPoint]
        startIndex = s.index(startPoint)
        curIndex = startIndex
        
        while True:
            if curIndex == 0:
                nextIndex = 1
            else:
                nextIndex = 0
            
            i = 1
            while i < len(s):
                if leftOf(s[curIndex], s[i],s[nextIndex]):
                    nextIndex = i
                i = i + 1
                
            if nextIndex == startIndex:
                break
            
            hull.append(s[nextIndex])
            curIndex = nextIndex
        return hull

    conHull = giftWrapping(sortedPts)

    #draws lines between each point in the convex hull
    for i in range(len(conHull)):
        cv2.line(img,conHull[i],conHull[i-1],(255,0,0),1)
    cv2.imwrite("newIMG.jpg", img)



if __name__ == "__main__":
    # templateMatching()
    # cameraOn()
    #findTriangulation('IMG_4103.png')
    pass
