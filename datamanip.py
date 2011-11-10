import numpy as np
import matplotlib.pyplot as plt

def plot_histogram(degrees,bins=10):
    """This function plots the degrees list 
     using the specified number of bins"""
    if(not isinstance(degrees, np.ndarray)):
        np.array(degrees)
    #Normed allows to show the probability of appearance
    plt.hist(degrees, bins=bins, normed=True)

    plt.show()

if __name__ == '__main__':
    #Sample degree data from only two levels to test
    a=np.array([3, 4, 3, 2, 5, 8, 2, 2, 1, 6, 12, 93, 12, 11, 14, 14, 16, 28, 70, 44, 34, 7, 57, 76, 8, 61, 128, 107, 155, 59, 18, 13, 102, 102, 2, 13, 21, 137, 140, 37, 117, 122, 188, 36, 115, 104, 48, 125, 117, 76, 25, 122, 132, 40, 90, 123, 158, 229, 199, 91, 150, 92, 41, 44, 206, 160, 41, 216, 191, 134, 207, 109, 148, 30, 205, 66, 12, 45, 124, 234, 268, 154, 234, 98, 389, 49, 426, 462, 1244])
    bins=np.array([1,2,5,10,20,50,100,200,500,1000,2000]) 
    plot_histogram(a)
