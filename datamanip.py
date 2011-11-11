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
def plot_xy (x_list, y_list):
    plt.ylabel('Avg. number of node degree (so far)')
    plt.xlabel('Number of visited nodes')
    plt.title('Visited nodes vs. average node degree')
    plt.plot(x_list, y_list)
    plt.show()
def prepare_data(degree_list):
    x_list, y_list=[],[]
    i=0
    for d in degree_list:
        x_list.append(i+1)
        if( i== 0):
            y_list.append(d)
        else:
            avg = float( (degree_list[i] + y_list[i-1] )) / 2
            y_list.append( avg)
        i+=1
    plot_xy (np.array(x_list), np.array(y_list))
    
   # print y_list
   # print
   # print degree_list


if __name__ == '__main__':
    #Sample degree data from only two levels to test
    a=np.array([3, 4, 3, 2, 5, 8, 2, 2, 1, 6, 12, 93, 12, 11, 14, 14, 16, 28, 70, 44, 34, 7, 57, 76, 8, 61, 128, 107, 155, 59, 18, 13, 102, 102, 2, 13, 21, 137, 140, 37, 117, 122, 188, 36, 115, 104, 48, 125, 117, 76, 25, 122, 132, 40, 90, 123, 158, 229, 199, 91, 150, 92, 41, 44, 206, 160, 41, 216, 191, 134, 207, 109, 148, 30, 205, 66, 12, 45, 124, 234, 268, 154, 234, 98, 389, 49, 426, 462, 1244])
    #bins=np.array([1,2,5,10,20,50,100,200,500,1000,1500]) 
    #plot_histogram(a,bins)
    prepare_data(a)
