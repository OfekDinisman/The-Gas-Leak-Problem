import pandas as pd, numpy as np, matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point

from getInput import getPolygonsFromJson, getTasksFromJson
from cluster_manager import ClusterManager
from convex_hull_manager import ConvexHullManager
from voronoi import VoronoiManager
from plot_manager import PlotManager


NUM_OF_CLUSTERS = 8
MAGIC = 0.9


class GenerateModel():
    def __init__(self, tasks, service_resources, territory, compliance_rate, delay_time) -> None:
        # type: (dict, dict, Polygon, float, int) -> None
        self.tasks = tasks
        self.service_resources = service_resources
        self.territory = territory
        self.compliance_rate = compliance_rate
        self.delay_time = delay_time
        self.number_of_resources = len(self.service_resources)
        self.df = pd.DataFrame.from_dict(self.tasks)
        self.add_df_point()


    def _calculate_standard_weight(self):
        return self.compliance_rate * MAGIC

    @staticmethod
    def add_df_weights(row, standard_weight):
        if row['workType'] == "Standard":
            return standard_weight
        elif row['workType'] == "Emergency":
            return 1 - standard_weight

    def add_df_point(self):
        self.df['point'] = self.df.apply(lambda row: Point(row['lng'] * 1000000, row['lat'] * 1000000), axis=1)
    
    def run(self):
        standard_weight = self._calculate_standard_weight()
        self.df['weight'] = self.df.apply(
            lambda row: self.add_df_weights(row, standard_weight), axis=1)
        X = np.array(self.df[['lng', 'lat']]) * 1000000
        W = np.array(self.df['weight'])
        X.astype(int)

        cm = ClusterManager(self.df, X)
        df, cluster_centers = cm.kmeans(NUM_OF_CLUSTERS, W)
        # df, cluster_centers = cm.kmeans_equal(NUM_OF_CLUSTERS, territory)

        # ch = ConvexHullManager(NUM_OF_CLUSTERS, df)
        # ch.convexPoints()

        vor = VoronoiManager(cluster_centers, self.territory)
        polys, points, = vor.getVor()

        plot = PlotManager()
        plot.plotPlolygonsAndPoints(X, polys.values())
