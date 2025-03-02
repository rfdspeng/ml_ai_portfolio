Imagine you have 1000 data points randomly (uniformly) scattered in a $D$-dimensional space. We want to measure how "far" the **nearest** and **farthest** points are from a given query point.

In the $1D$ case, let your space be a unit line segment, $[0, 1]$. Then the nearest neighbor is $1/1000 = 0.001$ units away, and the farthest neighbor is at most $1$ unit away. **The ratio of farthest to nearest is $\approx 1000$, which is a big difference; therefore, nearest neighbors are meaningful in $1D$!**

In the $2D$ case, your space is a $1 \times 1$ square. The nearest neighbor is now $1/\sqrt{1000} \approx 0.03$ units away, and the farthest neighbor is about $\sqrt{2} = 1.41$ units away (the diagonal of the square). **The ratio of farthest to nearest is $\approx 47$, which is still a healthy ratio.**

In the $3D$ case, your space is a $1 \times 1 \times 1$ cube. The nearest neighbor is $1/\sqrt[3]{1000} \approx 0.1$ units away, and the farthest neighbor is $\sqrt{3} \approx 1.73$ units away. **The ratio of farthest to nearest is $\approx 17$. The ratio is shrinking, that is, nearest and farthest points are getting closer in relative distance.**

In the general case, the nearest point is $\approx 1/\sqrt[D]{1000}$ units away, and the farthest point is $\approx \sqrt{D}$ units away. 

For $100D$, the nearest neighbor is 






Query point = inference point









https://www.cs.cornell.edu/courses/cs4780/2022fa/lectures/lecturenote02_kNN.html

The KNN classifier assumes that similar points (vectors) have similar labels. However, as the number of dimensions in the vector space increases, points that are drawn from a probability distribution start to be equidistant from all other points - that is, given a test point, all training samples become equidistant from the test point and the concept of nearest neighbors starts to fail.

Let $d$ be the dimension of the vector space, and consider the unit hypercube defined by $[0, 1]^d$. Let the training data be sampled uniformly within this hypercube. We want to find the $k$ nearest neighbors of a test point.

Let $l$