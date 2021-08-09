import pandas as pd, numpy as np, matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from scipy.spatial import ConvexHull
from getInput import getTasksFromJson

tasks = getTasksFromJson("src\input\serviceAppointment.json")

df = pd.DataFrame.from_dict(tasks)

X=np.array(df[['lat', 'lng']])


epsilon = 0.0015
db = DBSCAN(eps=epsilon, min_samples=5) 


model=db.fit(np.radians(X))
cluster_labels = db.labels_


num_clusters = len(set(cluster_labels))


cluster_labels = cluster_labels.astype(float)
cluster_labels[cluster_labels == -1] = np.nan


labels = pd.DataFrame(db.labels_,columns=['CLUSTER_LABEL'])

dfnew=pd.concat([df,labels],axis=1,sort=False)



z=[] #HULL simplices coordinates will be appended here

for i in range (0,num_clusters-1):
    dfq=dfnew[dfnew['CLUSTER_LABEL']==i]
    Y = np.array(dfq[['lat', 'lng']])
    hull = ConvexHull(Y)
    plt.plot(Y[:, 1],Y[:, 0],  'o')
    z.append(hull.simplices)
    for simplex in hull.simplices:
        ploted=plt.plot( Y[simplex, 1], Y[simplex, 0],'k-',c='m')


plt.show()

print(z)