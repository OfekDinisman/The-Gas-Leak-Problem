import pandas as pd, numpy as np
from sklearn.cluster import DBSCAN, KMeans
from shapely.geometry import Point

from voronoi import VoronoiManager


class ClusterManager():
    def __init__(self, df, X) -> None:
        self.df = df
        self.X = X

    def dbscan(self):
        # DBSCAN clustering method
        epsilon = 0.0015
        db = DBSCAN(eps=epsilon, min_samples=3)
        db.fit(np.radians(self.X))
        cluster_labels = db.labels_
        num_clusters = len(set(cluster_labels))
        cluster_labels = cluster_labels.astype(float)
        cluster_labels[cluster_labels == -1] = np.nan
        labels = pd.DataFrame(db.labels_,columns=['CLUSTER_LABEL'])
        dfnew=pd.concat([self.df,labels],axis=1,sort=False)
        return num_clusters, dfnew

    def kmeans(self, NUM_CLUSTERS):
        kmeans = KMeans(n_clusters = NUM_CLUSTERS, init ='k-means++')
        kmeans.fit(self.X, sample_weight=None) # Compute k-means clustering.
        self.df['CLUSTER_LABEL'] = kmeans.fit_predict(self.X)
        centers = kmeans.cluster_centers_ # Coordinates of cluster centers.
        labels = kmeans.predict(self.X) # Labels of each point
        # labels = pd.DataFrame(kmeans.labels_,columns=['CLUSTER_LABEL'])
        # dfnew=pd.concat([self.df,labels],axis=1,sort=False)
        return self.df, centers

    def kmeans_equal(self, k, boundary):
        # create k clusters
        df, clusters = self.kmeans(k)
        # get centroids
        vor = VoronoiManager(clusters, boundary)
        polys, centers = vor.getVor() # TO DO: centers is index
        # get cluster_size
        cluster_size = {}
        for i in range(len(polys)):
            size = 0
            for x in self.X:
                if polys[i].contains(Point(x)):
                    size += 1
            cluster_size[i] = size
        # sort according to cluster size
        cluster_size = {key: val for key, val in sorted(cluster_size.items(), key=lambda item: item[1], reverse=True)}
        
    
        return self.df, centers


        