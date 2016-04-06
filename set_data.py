__author__ = 'Samuel Angmor Mensah (LJ1506205)'
"""
Load data and write distance matrix on to text file
"""
from scipy.spatial import distance


def load_datapoints(filename):
    """
    Loads data set from file into memory

    @param filename: data set containing x,y values
                    some data set contains x,y,label
    @return: a list of data points in 2D, (x,y)
    """
    data_set = []
    with open(filename) as file:
        for line in file:
            if len(line.split()) == 3:
                x,y,label = [float(val) for val in line.split()]
                data_set.append([x,y])
            else:
                x,y = [float(val) for val in line.split()]
                data_set.append([x,y])
    return data_set

#Input data file name and load data into data_set list
data = raw_input('Enter name of data set: ')
data_set = load_datapoints('./Data_Set/'+data)


#create dictionary for data set
def data_dict(data_set):
    """
    Creates dictionary of the data set

    @param data_set: data points (x,y) in a list
    @return: a dictionary, every point has a unique key
    """
    data_dictionary = {}
    for key, val in enumerate(data_set):
            data_dictionary[key] = val
    return data_dictionary

data_dictionary = data_dict(data_set)


def distance_matrix(data_dictionary, dist_output):
    """
    Creates a distance matrix from dictionary on to text file

    @param data_dictionary: dictionary of data set
    @param dist_output: file name of output file to contain
                        distance matrix
    """
    f = open(dist_output, 'w')
    for i_key, i_value in data_dictionary.iteritems():
        for j_key, j_value in data_dictionary.iteritems():
            f.write(str(i_key)+' '+ str(j_key)+' '+str(distance.euclidean(i_value, j_value))+'\n')

distance_output = './Distance_Matrix/distance_'+data



if __name__ == '__main__':
    distance_matrix(data_dictionary, distance_output)
    print('Distance matrix created')