from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

xs =[1,2,3,4,5,6,7,8,9,10]
ys =[5,6,2,3,13,4,1,2,4,8]
zs =[2,3,3,3,5,7,9,11,9,10]

xt =[-1,-2,-3,-4,-5,-6,-7,8,-9,-10]
yt =[-5,-6,-2,-3,-13,-4,-1,2,-4,-8]
zt =[-2,-3,-3,-3,-5,-7,9,-11,-9,-10]

ax.scatter(xs, ys, zs, c='red', marker='o')
ax.scatter(xt, yt, zt, c='blue', marker='^')

ax.set_xlabel('X label')
ax.set_ylabel('Y label')
ax.set_zlabel('Z label')

plt.show()
