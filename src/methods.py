

def assignPointsToPolygons(points, polygons):
    result = {}
    for poly in polygons:
        poly_points = []
        for point in points:
            if poly.contains(point):
                poly_points.append(point)
        result[poly] = poly_points
    return result