import pandas as pd, numpy as np
from shapely.geometry import Polygon, Point

from getInput import getPolygonsFromJson, getTasksFromJson
from cluster_manager import ClusterManager
# from convex_hull_manager import ConvexHullManager
from voronoi import VoronoiManager
from plot_manager import PlotManager
from const import MILLION


NUM_OF_CLUSTERS = 4
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
        self.df_tasks = pd.DataFrame.from_dict(self.tasks)
        # self.add_task_point()


    def _calculate_standard_weight(self):
        return self.compliance_rate * MAGIC

    @staticmethod
    def add_task_weights(row, standard_weight):
        if row['workType'] == "Standard":
            return standard_weight
        elif row['workType'] == "Emergency":
            return 1 - standard_weight

    def add_task_point(self):
        self.df_tasks['point'] = self.df_tasks.apply(lambda row: Point(row['lng'] * MILLION, row['lat'] * MILLION), axis=1)

    def run(self):
        standard_weight = self._calculate_standard_weight()
        self.df_tasks['weight'] = self.df_tasks.apply(
            lambda row: self.add_task_weights(row, standard_weight), axis=1)
        X = np.array(self.df_tasks[['lng', 'lat']]) * MILLION
        W = np.array(self.df_tasks['weight'])
        X.astype(int)

        cm = ClusterManager(self.df_tasks, X)
        df, cluster_centers = cm.kmeans(NUM_OF_CLUSTERS, W)
        # df, cluster_centers = cm.kmeans_equal(NUM_OF_CLUSTERS, territory)

        # ch = ConvexHullManager(NUM_OF_CLUSTERS, df)
        # ch.convexPoints()

        vor = VoronoiManager(cluster_centers, self.territory)
        polys, points, = vor.getVor()

        plt = PlotManager()
        plt.plotPolygonsAndPoints(X, polys.values())

        return list(polys.values())
