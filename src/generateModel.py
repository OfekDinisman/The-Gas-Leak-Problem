import pandas as pd, numpy as np, matplotlib.pyplot as plt
from shapely.geometry import Polygon

from getInput import getPolygonsFromJson, getTasksFromJson
from cluster_manager import ClusterManager
from convex_hull_manager import ConvexHullManager
from voronoi import VoronoiManager
from plot_manager import PlotManager


NUM_OF_CLUSTERS = 4

tasks = getTasksFromJson("src\input\serviceAppointment2.json")
territory = Polygon(getPolygonsFromJson("src\input\polygonInput.json")[2]["coordinates"])

df = pd.DataFrame.from_dict(tasks)
X = np.array(df[['lng', 'lat']]) * 1000000
X.astype(int)

cm = ClusterManager(df, X)
df, cluster_centers = cm.kmeans(NUM_OF_CLUSTERS)
# df, cluster_centers = cm.kmeans_equal(NUM_OF_CLUSTERS, territory)


# ch = ConvexHullManager(NUM_OF_CLUSTERS, df)
# ch.convexPoints()


vor = VoronoiManager(cluster_centers, Polygon(territory))
polys, points, = vor.getVor()

plot = PlotManager()
plot.plotPlolygonsAndPoints(X, polys.values())
