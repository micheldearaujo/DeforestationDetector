"""
Random Forest Classifier to classify Amazon dataset
Plotting the classification results

Created on TUE Apr 30 2021     10:00:00

@author: micheldearaujo

"""
from utilities import *

rfc = pd.read_csv(base_dir+'/'+'rfc_scores_all.csv')

#matplotlib.rcParams.update({'font.size': 20})
SMALL_SIZE = 22
MEDIUM_SIZE = 22
BIGGER_SIZE = 22

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=24)     # fontsize of the axes title
plt.rc('axes', labelsize=22)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=18)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = False


markers =['o','*','v','X','s','D','+','>','p']
sizes=['8x8','16x16','32x32','64x64','128x128']
linestyles=['dashed','solid','dashdot','dotted']
n_trees = ['100','500']
cores=['blue','orange','green','red']
ss = [200,120,120,120,120]

fig0, axs = plt.subplots(1, 2)
#plt.suptitle('Precision and Recall As Function of The Trees Number and Image Size for RFC')

axs[0].set_xlabel('N trees')

axs[1].set_xlabel('N trees')
axs[0].set_ylabel('Precision')
axs[1].set_ylabel('Recall')
#axs.set_title('Precision and Recall As Function of The Trees Number and Image Size for RFC')
axs[0].grid(which='major', linestyle='--')
axs[0].grid(which='minor', linestyle=':')
axs[1].grid(which='major', linestyle='--')
axs[1].grid(which='minor', linestyle=':')


for k in range(len(sizes)):
    axs[0].plot(rfc[rfc['Target size']==sizes[k]]['n Trees'],
            rfc[rfc['Target size']==sizes[k]]['Avg Precision'],
             marker=markers[k],
                markersize=10,
             label=sizes[k])
for k in range(len(sizes)):
    axs[1].plot(rfc[rfc['Target size']==sizes[k]]['n Trees'],
            rfc[rfc['Target size']==sizes[k]]['Avg Recall'],
             marker=markers[k],
                markersize=10,
             label=sizes[k])
axs[0].legend(title='Image size', loc=4)
axs[1].legend(title='Image size', loc=4)

# axs[0].scatter(rfc[rfc['Target size']=='128x128']['Avg Recall'],
#             rfc[rfc['Target size']=='128x128']['Avg Precision'])
# axs[0].legend(title='Image Size')
# axs[1].legend(title='n trees')
# axs2=axs.twiny()
# for k in [0,5]:
#     x = (rfc[rfc['Target size']=='8x8']['Avg Recall'][0+k],
#          rfc[rfc['Target size']=='16x16']['Avg Recall'][1+k],
#          rfc[rfc['Target size']=='32x32']['Avg Recall'][2+k],
#          rfc[rfc['Target size']=='64x64']['Avg Recall'][3+k])
#
#     y = (rfc[rfc['Target size']=='8x8']['Avg Precision'][0+k],
#          rfc[rfc['Target size']=='16x16']['Avg Precision'][1+k],
#          rfc[rfc['Target size']=='32x32']['Avg Precision'][2+k],
#          rfc[rfc['Target size']=='64x64']['Avg Precision'][3+k])
#     axs2.scatter(x,y, marker=markers[k],
#                 label=n_trees[k],
#                  color='black',
#                  s=90)
#axs[0].set_ylim(0.966,0.98)

#plt.ylim(0.965,0.985)

plt.show()
