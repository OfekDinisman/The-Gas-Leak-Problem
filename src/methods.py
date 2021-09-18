from shapely.geometry import Point
from const import MILLION


def get_point_for_poly_from_object(obj):
    return Point(obj['lng'] * MILLION, obj['lat'] * MILLION)

def get_point_from_object(obj):
    return Point(obj['lng'], obj['lat'])