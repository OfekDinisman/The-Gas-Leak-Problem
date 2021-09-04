import pandas as pd, numpy as np, matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from scipy.spatial.qhull import ConvexHull


class ConvexHullManager():
    def __init__(self, num_clusters, df) -> None:
        self.num_clusters = num_clusters
        self.df = df

    def convexPoints(self):
        z=[] #HULL simplices coordinates will be appended here

        for i in range (0,self.num_clusters-1):
            dfq=self.df[self.df['CLUSTER_LABEL']==i]
            Y = np.array(dfq[['lat', 'lng']])
            hull = ConvexHull(Y)
            plt.plot(Y[:, 1],Y[:, 0],  'o')
            z.append(hull.simplices)
            for simplex in hull.simplices:
                plt.plot( Y[simplex, 1], Y[simplex, 0],c='m')
        plt.show()
        print(z)

    def convexLines(self):
        pass