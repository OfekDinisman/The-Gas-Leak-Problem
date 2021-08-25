import json
from pykml import parser

def getPolygonsFromJson(jsonfile):
    file = open(jsonfile,)
    data = json.load(file)
    polygons = []
    for d in data:
        polygon = {}
        polygon["_id"] = d["Id"]
        polygon["name"] = d["Name"]        
        kml = d['FSL__KML__c'].encode('utf-8')
        root = parser.fromstring(kml)
        coordinates = root.Placemark.Polygon.outerBoundaryIs.LinearRing.coordinates
        polygon["coordinates"] = coordinates
        polygons.append(polygon)
    return polygons


def getTasksFromJson(jsonfile):
    file = open(jsonfile,)
    data = json.load(file)
    tasks = []
    for d in data:
        task = {}
        task["_id"]                 = d["Id"]
        task["lat"]                 = d["Longitude"]
        task["lng"]                 = d["Latitude"]
        task["startTime"]           = d["EarliestStartTime"]
        task["workType"]            = d["WorkType"]["Name"]
        task["serviceTerritory"]    = d["ServiceTerritoryId"]
        task["startTime"]           = d["SchedStartTime"]
        task["endTime"]             = d["SchedEndTime"]
        task["serviceResource"]     = d["Assigned_Service_Resource__c"]
        tasks.append(task)
    return tasks


# def getStandardTaskCoordinates(tasks):
#     coordinates = []
#     for task in tasks:
#         if task["workType"] == "Standard":
#             coordinate = [task["lat"],task["lng"]]
#             coordinates.append(coordinate)
#     return coordinates


# tasks = getTasksFromJson("src\input\serviceAppointment.json")
# coordinates = getStandardTaskCoordinates(tasks)
# print(coordinates)