"""
K-Nearest Neighbors to classify Amazon dataset
Plotting the knn results
Created on TUE Apr 30 2021     10:00:00

@author: micheldearaujo

"""
from utilities import *
# the best size is 64x64

# Defining the hyperams
knn = pd.read_csv(base_dir+'/'+'knn_scores_all.csv')
sizess = [8, 16, 32, 64]



markers =['o','*','v','s','X','D','+','>', 'p']
sizes=['8x8','16x16','32x32','64x64']
linestyles=['dashed', 'solid', 'dashdot', 'dotted']


SMALL_SIZE = 22
MEDIUM_SIZE = 22
BIGGER_SIZE = 22
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=24)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

def plot_knn():
    fig0, axs = plt.subplots(1, 2)

    axs[0].set_xlabel('Image size')
    axs[1].set_xlabel('Image size')
    axs[0].set_ylabel('Precision')
    axs[1].set_ylabel('Recall')

    x, y = list(), list()
    for k in range(len(sizes)):
        x.append(knn[knn['Target size']==sizes[k]]['Target size'][k])
        y.append(knn[knn['Target size']==sizes[k]]['Avg Precision'][k])
    axs[0].plot(x,y, marker ='o', markersize=10)
    x,y = list(), list()


    for k in range(len(sizes)):
        x.append(knn[knn['Target size']==sizes[k]]['Target size'][k])
        y.append(knn[knn['Target size']==sizes[k]]['Avg Recall'][k])

    axs[1].plot(x,y, marker='o', markersize=10)
    #axs[0].legend(title='Image size')
    #axs[1].legend(title='Image size')

    axs[0].grid(which='major', linestyle='--')
    axs[0].grid(which='minor', linestyle=':')
    axs[1].grid(which='major', linestyle='--')
    axs[1].grid(which='minor', linestyle=':')
    plt.show()


def plot_ks():
    k8 = []
    k16 = []
    k32 = []
    k64 = []
    k = [k8, k16, k32, k64]

    # Creating a loop to extract the numbers of each file
    # But the numbers come in string type, so we create a new list to convert one by one to float
    for size in range(0, 4):
        with open(f'K_numbers_{sizess[size]}.txt') as f:
            aux = f.read().splitlines()
            for number in aux:
                k[size].append(float(number))


    # Plotting the results
    fig, ax = plt.subplots()
    ax.set_xlabel('K')
    ax.set_ylabel('Error Rate')

    ax.plot(range(1, 41), k8, ls=linestyles[0], marker=markers[0], label=sizes[0])
    ax.plot(range(1, 41), k16, ls=linestyles[1], marker=markers[2], label=sizes[1])
    ax.plot(range(1, 41), k32, ls=linestyles[2], marker=markers[3], label=sizes[2])
    ax.plot(range(1, 41), k64, ls=linestyles[3], marker=markers[4], label=sizes[3])

    # Plotting the minimal values
    ax.scatter(k8.index(min(k8)), min(k8), marker=markers[0], s=150)
    print(f'the minimum error rate for the 8x8 is: {k8.index(min(k8))} and {min(k8)}')
    ax.scatter(k16.index(min(k16)), min(k16), marker=markers[0], s=150)
    print(f'the minimum error rate for the 16x16 is: {k16.index(min(k16))} and {min(k16)}')
    ax.scatter(k32.index(min(k32)), min(k32), marker=markers[0], s=150)
    print(f'the minimum error rate for the 32x32 is: {k32.index(min(k32))} and {min(k32)}')
    ax.scatter(k64.index(min(k64)), min(k64), marker=markers[0], s=150)
    print(f'the minimum error rate for the 64x64 is: {k64.index(min(k64))} and {min(k64)}')

    ax.legend(title='Image size', loc='best')
    ax.grid()
    plt.show()


plot_ks()
