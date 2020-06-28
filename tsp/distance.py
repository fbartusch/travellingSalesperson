import logging
import math
import numpy as np

def euclidian_dist(x,y):
    # Just for members of the flat earth society ...
    return math.sqrt((x[0]-y[0]) ** 2 + (x[1]-y[1]) ** 2)

def orthodromic_dist(x, y, radius=1):
    # convert degree to radian
    lon1 = math.radians(x[0])
    lon2 = math.radians(y[0])
    lat1 = math.radians(x[1])
    lat2 = math.radians(y[1])

    delta_lon = lon2 - lon1
    delta_lat = lat2 - lat1
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    #delta_omega = 2 * math.sqrt(math.asin(math.sin(delta_lat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(delta_lon/2)**2))
    return radius * c

def compute_distance_matrix(xs, ys, method='euclidian', radius='1'):
    num_points = len(xs)
    # Check feasability
    if not len(xs) == len(ys):
        logging.error("Length of x-coordinates and y-coordinates do not match: " + str(len(xs)) + " vs. " + str(len(ys)))


    d = np.zeros((num_points, num_points))
    for i in range(num_points):
        for j in range(num_points):
            # xs: longitudes
            # ys: latitudes
            p = [xs[i], ys[i]]
            q = [xs[j], ys[j]]
            if i == j:
                d_pq = 0
            elif method == 'euclidian':
                d_pq = euclidian_dist(p, q)
            elif method == 'orthodromic':
                d_pq = orthodromic_dist(p, q, radius=radius)
            d[i,j] = d_pq
            d[j,i] = d_pq
    return d
