from pylab import *
import math
x = range(10)
y=[]
for i in x:
    y.append(math.cos(i/2))
plot(x, y)
show()