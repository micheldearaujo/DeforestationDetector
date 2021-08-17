"""
Convolutional Neural Network to classify Amazon dataset
Plotting the classification time results

Created on TUE Apr 30 2021     10:00:00

@author: micheldearaujo

"""

# Importing the library
from utilities import *

cnn = pd.read_csv(base_dir+'/'+'cnn_scores_03_.csv')
knn = pd.read_csv(base_dir+'/'+'knn_scores_all_.csv')
rfc = pd.read_csv(base_dir+'/'+'rfc_scores_all_.csv')
#cnn.dropna(inplace=True)
#knn.dropna(inplace=True)
#rfc.dropna(inplace=True)

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
plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = False
plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = True
plt.rcParams['ytick.left'] = plt.rcParams['ytick.labelleft'] = True
plt.rcParams['ytick.right'] = plt.rcParams['ytick.labelright'] = False



    # Classification time


fig, axs = plt.subplots()

# Making plots of the CNN algorithm
axs.set_xlabel('Image size')
axs.set_ylabel('Time(s)')
#axs.set_title('Single classifying time for the CNN on server environment')
#axs.plot(cnn['Target size'][0:5],cnn['Single classifying time (s)'][0:4], marker='o', markersize=9, label='Edge')
axs.plot(cnn['Target size'][5:], cnn['Single classifying time (s)'][5:], marker='D', markersize=9, label='Server')
# axs.xaxis.set_major_locator(MultipleLocator(1))
# axs.yaxis.set_major_locator(MultipleLocator(0.5))
# axs.xaxis.set_minor_locator(AutoMinorLocator(1))
# axs.yaxis.set_minor_locator(AutoMinorLocator(1))
axs.grid(which='major', linestyle='--')
axs.grid(which='minor', linestyle=':')
axs.legend()


fig2, axs = plt.subplots()
# Making plots of the RFC algorithm
axs.set_xlabel('Image size')
axs.set_ylabel('Time(s)')
#axs.set_title('Single classifying time for the RFC on server environment')
axs.plot(rfc[rfc['n Trees']==100][0:5]['Target size'], rfc[rfc['n Trees']==100]['Single classifying time (s)'][0:5], label='n trees = 100/ Edge', marker='o', markersize=7)
#axs.plot(rfc[rfc['n Trees']==100][5:]['Target size'], rfc[rfc['n Trees']==100]['Single classifying time (s)'][5:], label='n trees = 100/ Server', marker='^', markersize=7)
#axs.plot(rfc[rfc['n Trees']==500]['Target size'], rfc[rfc['n Trees']==500]['Single classifying time (s)'], label='n trees = 500/ Server', marker='D', markersize=8)
axs.legend()
# axs.xaxis.set_major_locator(MultipleLocator(1))
# axs.yaxis.set_major_locator(MultipleLocator(5))
# axs.xaxis.set_minor_locator(AutoMinorLocator(0.5))
# axs.yaxis.set_minor_locator(AutoMinorLocator(0.5))
axs.grid(which='major', linestyle='--')
axs.grid(which='minor', linestyle=':')


fig3, axs = plt.subplots()
# Making plots of the KNN algorithm
axs.set_xlabel('Image size')
axs.set_ylabel('Time(s)')
#axs.set_title('Single Classifying time for the KNN on server environment')
axs.plot(knn['Target size'][0:4], knn['Single classifying time (s)'][0:4], marker='o', markersize=9, label='Edge')
#axs.plot(knn['Target size'][4:], knn['Single classifying time (s)'][4:], marker='D', markersize=9, label='Server')
# axs.xaxis.set_major_locator(MultipleLocator(1))
# axs.yaxis.set_major_locator(MultipleLocator(0.5))
# axs.xaxis.set_minor_locator(AutoMinorLocator(1))
# axs.yaxis.set_minor_locator(AutoMinorLocator(1))
axs.grid(which='major', linestyle='--')
axs.grid(which='minor', linestyle=':')
axs.legend()


plt.tight_layout()
plt.show()
