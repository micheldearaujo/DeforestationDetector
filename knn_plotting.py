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

markers =['o','*','v','s','X','D','+','>','p']
sizes=['8x8','16x16','32x32','64x64']
linestyles=['dashed','solid','dashdot','dotted']


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

fig0, axs = plt.subplots(1, 2)

axs[0].set_xlabel('Image size')
axs[1].set_xlabel('Image size')
axs[0].set_ylabel('Precision')
axs[1].set_ylabel('Recall')

x,y = list(), list()
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