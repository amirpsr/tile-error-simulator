import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

# plt.rcParams["figure.figsize"] = [7.50, 3.50]
# plt.rcParams["figure.autolayout"] = True
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
p1=sp.Point3D(1,1,3.4)
p2 =sp.Point3D(1.5,2.4,1.4)
p3= sp.Point3D(2.5,3.4,2.4)
l1=sp.Line3D(p1,p2)
l2=sp.geometry.Segment3D(p2,p3)
print(l1,l2)
ax.scatter(p1.x, p1.y, p1.z, c='red', s=30)
ax.scatter(p2.x, p2.y, p2.z, c='red', s=30)
ax.scatter(p3.x, p3.y, p3.z, c='red', s=30)
ax.plot([l2.p1.x,l2.p2.x],[l2.p1.y,l2.p2.y],[l2.p1.z,l2.p2.z], color='black')
ax.plot([l1.p1.x,l1.p2.x],[l1.p1.y,l1.p2.y],[l1.p1.z,l1.p2.z], color='black')
ax.text(l2.midpoint.x, l2.midpoint.y, l2.midpoint.z, "{:.2f}".format(float(l2.length)), l2.direction_ratio)
print(l1.length)
print(l2.length)
# print(l2.direction_ratio)
# plt.plot(l1)
plt.show()

