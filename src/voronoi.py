# import numpy as np, matplotlib.pyplot as plt
# from scipy.spatial import Voronoi, voronoi_plot_2d
# from shapely.geometry import LineString, MultiLineString, MultiPolygon
# from shapely.ops import polygonize, cascaded_union
from geovoronoi import voronoi_regions_from_coords


class VoronoiManager():
    def __init__(self, points, boundary):
        self.points = points
        # self.vor = Voronoi(self.points)
        self.boundary = boundary

    # def getVorPolygons(self, territory):
    #     vertices = [ x for x in self.vor.ridge_vertices if -1 not in x]
    #     lines = [LineString(self.vor.vertices[x]) for x in vertices]
    #     polygons = []
    #     for poly in polygonize(lines):
    #         polygons.append(poly)
    #     return polygons

    # def plotVor(self):
    #     fig = voronoi_plot_2d(self.vor)
    #     plt.show()


    def getVor(self):
        region_polys, region_pts = voronoi_regions_from_coords(self.points, self.boundary)
        return region_polys, region_pts