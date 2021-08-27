from utilities import *

df = pd.read_csv(base_dir+'/knn_scores_all_.csv')
print(df[df['Computer'] == "Server"])