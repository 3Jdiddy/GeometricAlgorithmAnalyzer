class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
  
def Left_index(points):
    minn = 0
    for i in range(1,len(points)):
        if points[i].x < points[minn].x:
            minn = i
        elif points[i].x == points[minn].x:
            if points[i].y > points[minn].y:
                minn = i
    return minn
  
def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - \
          (q.x - p.x) * (r.y - q.y)
  
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2
  
def convexHull(points, n):
    pointsMod = []
    for point in points:
        pointsMod.append(Point(point[0], point[1]))
    if n < 3:
        return
    l = Left_index(pointsMod)
    hull = []
    p = l
    q = 0
    while(True):
        hull.append(p)
        q = (p + 1) % n
        for i in range(n):
            if(orientation(pointsMod[p], 
                           pointsMod[i], pointsMod[q]) == 2):
                q = i
        p = q
        if(p == l):
            break
    return [(pointsMod[i].x, pointsMod[i].y) for i in hull]
