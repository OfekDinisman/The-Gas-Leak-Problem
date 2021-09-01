import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from shapely.geometry import LineString, MultiLineString, MultiPolygon
from shapely.ops import polygonize


class VoronoiManager():
    def __init__(self, points):
        self.points = points
        self.vor = Voronoi(self.points)

    def getVorPolygons(self):
        vertices = [ x for x in self.vor.ridge_vertices if -1 not in x]
        lines = [LineString(self.vor.vertices[x]) for x in vertices]
        polygons = []
        for poly in polygonize(lines):
            polygons.append(poly)
        return polygons

    def plotVor(self):
        fig = voronoi_plot_2d(self.vor)
        plt.show()