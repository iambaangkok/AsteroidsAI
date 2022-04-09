
import math


def checkCollisionCircle(o1, o2):
    distance = math.hypot(o1.x - o2.x, o1.y - o2.y)
    if distance <= o1.circleRadius*o1.scale + o2.circleRadius*o2.scale: # they do collide
        return True
    else:
        return False 

def clamp(value = 1, minValue = 0, maxValue = 1):
    return max(minValue, min(value, maxValue))
