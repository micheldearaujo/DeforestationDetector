"""
Convolutional Neural Network to classify Amazon dataset
Plotting the results

Created on TUE Apr 30 2021     10:00:00

@author: micheldearaujo

"""

# Importing the library
from utilities import *


cnn = pd.read_csv(base_dir+'/'+'cnn_scores_all.csv')

markers =['o','*','v','s','X','D','+','>','p']
sizes=['8x8','16x16','32x32','64x64','128x128']
linestyles=['dashed','solid','dashdot','dotted','dashed']
thresholds = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
cores=['blue','orange','green','red','black']


# Precision Vs Recall Vs Image Size

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


# fig0, axs = plt.subplots()
# axs.set_xlabel('Recall')
# axs.set_ylabel('Precision')
# #axs.set_title('Precision and Recall as Function of Image Size for CNN')
#
# # Threshold X Image Size
# for k in range(len(sizes)):
#     axs.plot(cnn[cnn['Target size']==sizes[k]]['Avg Recall'],
#             cnn[cnn['Target size']==sizes[k]]['Avg Precision'],
#              marker=markers[k],
#              markersize=7,
#              label=sizes[k])
#
# axs2=axs.twinx()
# plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = False
# plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = True
# plt.rcParams['ytick.left'] = plt.rcParams['ytick.labelleft'] = True
# plt.rcParams['ytick.right'] = plt.rcParams['ytick.labelright'] = False
#
# # Plotting the threshold in the same graph as before
# # for k in range(0,9):
# #     x = (cnn[cnn['Target size']=='8x8']['Avg Recall'][0+k],
# #          cnn[cnn['Target size']=='16x16']['Avg Recall'][9+k],
# #          cnn[cnn['Target size']=='32x32']['Avg Recall'][18+k],
# #          cnn[cnn['Target size']=='64x64']['Avg Recall'][27+k])
# #
# #     y = (cnn[cnn['Target size']=='8x8']['Avg Precision'][0+k],
# #          cnn[cnn['Target size']=='16x16']['Avg Precision'][9+k],
# #          cnn[cnn['Target size']=='32x32']['Avg Precision'][18+k],
# #          cnn[cnn['Target size']=='64x64']['Avg Precision'][27+k])
# #     axs2.scatter(x,y, marker=markers[k],
# #                 label=thresholds[k],
# #                 c='black')
#
# axs.grid(which='major', linestyle='--')
# plt.xlim(0.29,1)
# axs.grid(which='minor', linestyle=':')
# axs.legend(title='Image size')
# # axs2.grid(which='major', linestyle='--')
# # axs2.grid(which='minor', linestyle=':')
# # axs2.legend(title='Threshold', loc=3)
#
#
# Accuracy versus threshold
fig1, axs = plt.subplots()
axs.set_xlabel('Threshold')
axs.set_ylabel('Accuracy')
#axs.set_title('Accuracy as Function of Threshold for CNN')

for j in range(len(sizes)):
    axs.plot(cnn[cnn['Target size']==sizes[j]]['Threshold'],
             cnn[cnn['Target size']==sizes[j]]['Avg Accuracy'],
             ls=linestyles[j],
             marker=markers[j],
             markersize=7,
             label=sizes[j])

axs.grid(which='major', linestyle='--')
plt.xlim(0.09,.91)
axs.grid(which='minor', linestyle=':')
axs.legend(title='Image size', loc=4)
plt.show()
# -----------------------------
#
#
# fig2, axs = plt.subplots()
# axs.set_xlabel('Recall')
# axs.set_ylabel('Precision')
# #axs.set_title('Precision and Recall as Function of Threshold for CNN')
#
# for h in range(len(thresholds)):
#     axs.plot(cnn[cnn['Threshold']==thresholds[h]]['Avg Recall'],
#              cnn[cnn['Threshold']==thresholds[h]]['Avg Precision'],
#              marker=markers[h],
#              markersize=7,
#              label=thresholds[h])
#
# axs.grid(which='major', linestyle='--')
# plt.xlim(0.29,1)
# axs.grid(which='minor', linestyle=':')
# axs.legend(title='Threshold', loc=3)




fig0, axs = plt.subplots(1, 2)
#plt.suptitle('Precision and Recall As Function of The Trees Number and Image Size for RFC')
axs[0].set_xlabel('Threshold')
axs[1].set_xlabel('Threshold')
axs[0].set_ylabel('Precision')
axs[1].set_ylabel('Recall')
#axs.set_title('Precision and Recall As Function of The Trees Number and Image Size for RFC')
axs[0].grid(which='major', linestyle='--')
axs[0].grid(which='minor', linestyle=':')
axs[1].grid(which='major', linestyle='--')
axs[1].grid(which='minor', linestyle=':')

for k in range(len(sizes)):
    axs[0].plot(cnn[cnn['Target size']==sizes[k]]['Threshold'],
              cnn[cnn['Target size']==sizes[k]]['Avg Precision'],
             marker=markers[k],
                markersize=9,
             label=sizes[k])
for k in range(len(sizes)):
    axs[1].plot(cnn[cnn['Target size']==sizes[k]]['Threshold'],
            cnn[cnn['Target size']==sizes[k]]['Avg Recall'],
             marker=markers[k],
                markersize=8,
             label=sizes[k])

axs[0].legend(title='Image size')
axs[1].legend(title='Image size')
plt.show()