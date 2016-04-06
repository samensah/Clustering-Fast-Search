__author__ = 'Samuel Angmor Mensah (LJ1506205)'
"""
Functions for Clustering by fast search and find of density peaks
"""
import numpy as np
import matplotlib.pyplot as plt


def load_data(distance_file):
    """
    Loads distance matrix file and creates a distance dictionary

    @param distance_file: distance matrix file
    @return: distance file and the max distance between points
    """
    max_dist = 0.0
    distances = {}
    with open(distance_file, 'r') as file:
        for line in file:
            point_a, point_b, dist = [float(x) for x in line.split()]
            point_a, point_b = int(point_a), int(point_b)
            max_dist = max(max_dist, dist)
            distances[(point_a, point_b)] = dist
    return distances, max_dist



def local_density(num_points, distances, dc):
    """
    Creates an array of local densities of the data points

    @param max_id: ID of the last point read in.
    @param num_points: Number of data points
    @param distances: distance dictionary between points
    @param dc: distance cut of algorithm
    @return: local density of points given dc
    """
    def density(dij, dc):
        if dij < dc:
            return 1 #If point is in dc neighbourhood
        else:
            return 0 #If point is outside dc neighbourhood
    rho = [0] * num_points
    for i in range(0, num_points-1):
        for j in range(i + 1, num_points):
            rho[i] += float(density(distances[(i, j)], dc))
            rho[j] += float(density(distances[(i, j)], dc))
    return np.array(rho)



def delta_dist(max_dist, distances, num_points, rho):
    """
    Creates an array for delta and nearest neighbour of each point

    @param max_dist: max distance between points
    @param rho: density array for points
    @return: array for delta and nearest neighbour (nn)
    """
    idx = np.argsort(-rho)
    #initialize delta, nn
    delta = [float(max_dist)]*num_points
    nn = [0] * len(rho)
    delta[idx[0]] = -1.
    #update delta and nn
    for i in range(1, num_points):
        for j in range(0, i):
            a_idx, b_idx = idx[i], idx[j]
            if distances[(a_idx, b_idx)] < delta[a_idx]:
                delta[a_idx] = distances[(a_idx, b_idx)]
                nn[a_idx] = b_idx
    delta[idx[0]] = max(delta)
    return delta, nn


def plot_rho_delta(x, y):
    """
    Plot of delta on rho

    @param x: rho for point i
    @param y: delta for point i
    @return:
    """
    plt.plot(x, y, 'k.')
    plt.title('delta on rho')
    plt.xlabel('rho')
    plt.ylabel('delta')
    plt.xlim(-0.5, max(x)+1)
    plt.ylim(0, max(y)+1)



def cluster_func(max_dist, num_points, distances, dc, rho_threshold, delta_threshold):
    """
    Returns clusters

    @param rho_threshold: Density threshold to select centers
    @param delta_threshold: Delta threshold to select centers
    @return: dictionary of centers and clusters
    """
    cluster, centers = {}, {}
    #Choose centers
    rho = local_density(num_points, distances, dc)
    delta, nn = delta_dist(max_dist, distances, num_points, rho)
    for idx, (rho_val, delta_val, nn_val) in enumerate(zip(rho, delta, nn)):
        if rho_val >= rho_threshold and delta_val >= delta_threshold:
            centers[idx] = idx; cluster[idx] = idx
    count = 0
    while len(cluster) < (num_points):
        if len(cluster) == 0:
            print('No center selected (Check threshold values)')
            break
        for idx, (rho_val, delta_val, nn_val) in enumerate(zip(rho, delta, nn)):
            if idx not in centers:
                if rho_val == 0:
                    cluster[idx] = -1
                elif nn_val in cluster:
                    cluster[idx] = cluster[nn_val]
        count += 1
    return cluster, centers
