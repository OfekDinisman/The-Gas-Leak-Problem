import pandas as pd, numpy as np, matplotlib.pyplot as plt


class PlotManager():
    def __init__(self) -> None:
        pass


    def plotPoints(self, points):
        plt.figure()
        x, y = points.T
        plt.scatter(x, y)
        plt.show()


    def plotPolygons(self, polygons):
        plt.figure()
        for poly in polygons:
            xs, xy = poly.exterior.xy
            plt.plot(xs, xy)
        plt.show()
    
    def plotPolygonsAndPoints(self, points, polygons):
        plt.figure()
        x, y = points.T
        plt.scatter(x, y)
        for poly in polygons:
            xs, xy = poly.exterior.xy
            plt.plot(xs, xy)
        plt.show()