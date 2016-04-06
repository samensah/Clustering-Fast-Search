__author__ = 'Samuel Angmor Mensah (LJ1506205)'
"""
Clustering by fast search and find of density peaks
Run program
"""

from set_data import data_set, \
    data_dictionary, distance_output
from functions import *



num_points = len(data_set)
max_id = num_points - 1
distances, max_dist = load_data(distance_output)

plt.figure(1)
for point in data_set:
    plt.scatter(point[0], point[1])
plt.show()

arg = 1
while arg == 1:
    dc = input('Enter cutting distance(dc): ')
    rho = local_density(num_points, distances, dc)
    delta, nn = delta_dist(max_dist,distances, num_points, rho)


    plt.figure(1)
    plt.subplot(121)
    for point in data_set:
        plt.scatter(point[0], point[1])


    plt.subplot(122)
    plot_rho_delta(rho[0:], delta[0:])
    plt.show()

    decision = raw_input('"No" to change dc, "Yes" to continue: ')
    if decision == 'Yes':
        arg = 0

rho_thresh = input('Enter density threshold to select center: ')
delta_thresh = input('Enter delta threshold to select center: ')

#cluster_func(max_id, max_dist, num_points, distances, dc, rho_threshold, delta_threshold)
cluster, center = cluster_func(max_dist, num_points,distances,
                                dc, rho_threshold=rho_thresh, delta_threshold=delta_thresh)

for idx, cent in enumerate(center):
    print('Center point of cluster'+' '+str(idx)+':', data_dictionary[cent])


colours = 10*['r','g','b','c','y', '#ff8100','m','#d5d8da', '#bb746b']

i = 0
plt.figure(2)
for cent in center:
    for key, value in cluster.iteritems():
        x = data_dictionary[key][0]
        y = data_dictionary[key][1]
        if value == -1:
            plt.scatter(x,y, color= 'k')
        if value == cent:
            plt.scatter(x,y, color=colours[i])
    i +=1
    if i == len(colours):
        i = 0

for cent in center:
    for key, value in cluster.iteritems():
        x = data_dictionary[key][0]
        y = data_dictionary[key][1]
        if key == value:
            plt.plot(x, y, marker='x', markersize=9, color= 'k')
plt.title(str(len(center))+' clusters, dc = '+str(dc))
plt.show()
