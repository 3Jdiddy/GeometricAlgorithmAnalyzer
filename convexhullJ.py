import numpy as np
import cv2
import sys

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
        
    cv2.imshow("Display window", img)
    cv2.waitKey(0)
    cv2.imwrite("newImg.jpg", img)
