class Point:
    x = -1
    y = -1

    def __init__(self, x, y):
		self.x = x
		self.y = y



p1 = Point(3,5)
p2 = p1

points =[]
points.append(p2)
if p1 in points:
    print ("In uses value equality")