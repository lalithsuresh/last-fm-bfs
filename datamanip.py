import numpy as np
import sys
import matplotlib.pyplot as plt

def plot_histogram(degrees,bins=10):
    """This function plots the degrees list 
     using the specified number of bins"""
    if(not isinstance(degrees, np.ndarray)):
        np.array(degrees)
    #Normed allows to show the probability of appearance
    plt.xscale('log')
    plt.yscale('log')
    plt.hist(degrees, bins=bins )

    plt.show()
def plot_xy (x_list, y_list):
    plt.ylabel('Avg. number of node degree (so far)')
    plt.xlabel('Number of visited nodes')
    plt.title('Visited nodes vs. average node degree')
    
    #plt.yscale('log')
    plt.plot( y_list)
    """Plotted some polynomial aprox
    c = np.polyfit(x_list, y_list, 10)
    y2 = np.polyval(c, x_list)
    plt.plot(x_list, y2, label="10" )
    """
    plt.show()
def prepare_data(degree_list):
    x_list, y_list=[],[]
    i=0
    for d in degree_list:
        x_list.append(i+1)
        if( i== 0):
            y_list.append(d)
        else:
            avg = float( (degree_list[i] + y_list[i-1]*(i-1) )) / i
            y_list.append(avg)
        i+=1
    print np.average(degree_list), "with std dev", np.std(degree_list)
    plot_xy (np.array(x_list), np.array(y_list))
    
def savetofile(degree_list, filename='output'):
    fd = open(filename, "w")
    fd.writelines(str(degree_list))
    fd.close()

if __name__ == '__main__':
    if( len(sys.argv) > 1):
        f = open(sys.argv[1], 'r')

        degree_list_from_file=f.readline().split(",")
        tmp =map(lambda x: float(x), degree_list_from_file)
    
        print tmp 
    
        bins=np.array([1,2,5,10,20,50,100,200,500,1000,1500]) 
        #plot_histogram(tmp,bins)
        #savetofile(a)
        prepare_data(tmp)

