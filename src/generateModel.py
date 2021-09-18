import pandas as pd, numpy as np
from shapely.geometry import Polygon, Point
import math

from cluster_manager import ClusterManager
from voronoi import VoronoiManager
from plot_manager import PlotManager
from const import MILLION



class GenerateModel():
    def __init__(self, tasks, service_resources, territory, compliance_rate, delay_time, speed) -> None:
        # type: (dict, dict, Polygon, float, int, int) -> None
        self.tasks = tasks # either only std tasks or also emg historical tasks.
        self.service_resources = service_resources
        self.territory = territory
        self.compliance_rate = compliance_rate
        self.delay_time = delay_time
        self.speed = speed
        self.number_of_resources = len(self.service_resources)
        self.df_tasks = pd.DataFrame.from_dict(self.tasks)
        # self.add_task_point()


    def _calculate_standard_weight(self):
        '''
        This returns the weight given to std points. If compliance rate lower than 50%, emg tasks have no weight.
        Otherwise linear to compliance weight. Comp rate = 1 -> Ratio Std weight / Emg weight = 1.
        '''
        if self.compliance_rate >= 0.5:
            return (1.5 - self.compliance_rate)
        return 1

    @staticmethod
    def add_task_weights(row, standard_weight):
        if row['workType'] == "Standard":
            return standard_weight
        elif row['workType'] == "Emergency":
            return 1 - standard_weight

    def add_task_point(self):
        self.df_tasks['point'] = self.df_tasks.apply(lambda row: Point(row['lng'] * MILLION, row['lat'] * MILLION), axis=1)

    def max_polygon_area(self):
        max_dist = (self.delay_time / 60) * self.speed  # [min/60] * [KM/H] = KM
        return math.pi() * ((max_dist /2) ^ 2)

    def run(self):
        standard_weight = self._calculate_standard_weight()
        self.df_tasks['weight'] = self.df_tasks.apply(
            lambda row: self.add_task_weights(row, standard_weight), axis=1)
        X = np.array(self.df_tasks[['lng', 'lat']]) * MILLION
        W = np.array(self.df_tasks['weight'])
        X.astype(int)

        cm = ClusterManager(self.df_tasks, X)
        df, cluster_centers = cm.kmeans(self.number_of_resources, W)

        vor = VoronoiManager(cluster_centers, self.territory)
        polys, points, = vor.getVor()

        plt = PlotManager()
        plt.plotPolygonsAndPoints(X, polys.values())

        return list(polys.values())
