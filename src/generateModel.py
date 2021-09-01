import pandas as pd, numpy as np, matplotlib.pyplot as plt
from getInput import getTasksFromJson
from voronoi import VoronoiManager
from plot_manager import PlotManager

from cluster_manager import ClusterManager
from convex_hull_manager import ConvexHullManager

NUM_OF_CLUSTERS = 5

tasks = getTasksFromJson("src\input\serviceAppointment.json")

df = pd.DataFrame.from_dict(tasks)
X = np.array(df[['lat', 'lng']]) * 1000000
X.astype(int)

cm = ClusterManager(df, X)
df, cluster_center = cm.kmeans(NUM_OF_CLUSTERS)

ch = ConvexHullManager(NUM_OF_CLUSTERS, df)
ch.convexPoints()


# vor = VoronoiManager(X)
# polygons = vor.getVorPolygons()
# vor.plotVor()

# plot = PlotManager()
# plot.plotPolygons(polygons)