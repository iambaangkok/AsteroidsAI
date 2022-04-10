
import math

def getLineCircleIntersectionPoint(A,B,C,m,x0,y0,r):
    sqrt = math.sqrt(-(C*C) + 2*y0*(C+m*x0)-2*C*m*x0 + m*m*r*r-m*m*x0*x0+r*r-y0*y0)
    ansX1 = (1/(m**2+1)) * (+ sqrt -C*m+m*y0+x0)
    ansX2 = (1/(m**2+1)) * (- sqrt -C*m+m*y0+x0)

    return ansX1, ansX2

def getLineEquation(p1, p2):
    m = getSlope(p1.x,p2.x,p1.y,p2.y)
    A = m
    B = -1
    C = (-m * p1.x + p1.y)
    return A,B,C,m,p1,p2

def getPointToLineDistance(A,B,C,x0,y0):
    return abs(A*x0 + B*y0 + C)/(math.hypot(A, B))

def getPointDistance(x1,y1,x2,y2):
    return math.hypot(x1-x2,y1-y2)

def getSlope(x1,x2,y1,y2):
    if x1 == x2:
        return math.inf
    return (y1-y2)/(x1-x2)

def checkCollisionCircle(o1, o2):
    distance = math.hypot(o1.x - o2.x, o1.y - o2.y)
    if distance <= o1.circleRadius*o1.scale + o2.circleRadius*o2.scale: # they do collide
        return True
    else:
        return False 

def clamp(value = 1, minValue = 0, maxValue = 1):
    return max(minValue, min(value, maxValue))
