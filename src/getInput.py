import json
from pykml import parser

def getPolygonsFromJson(json_data):
    try:
        file = open(json_data,)
        data = json.load(file)
    except:
        data = json_data
    polygons = []
    for d in data:
        polygon = {}
        polygon["_id"] = d["Id"]
        polygon["name"] = d["Name"]        
        kml = d['FSL__KML__c'].encode('utf-8')
        root = parser.fromstring(kml)
        coordinates= root.Placemark.Polygon.outerBoundaryIs.LinearRing.coordinates.text
        coordinates = coordinates.rstrip().replace("\n", ",").split(",")
        points = []
        for i in range(0, len(coordinates), 3):
            x, y, z = float(coordinates[i])*1000000, float(coordinates[i+1])*1000000, float(coordinates[i+2])
            points.append((x,y))
        polygon["coordinates"] = points
        polygons.append(polygon)
    return polygons


def getTasksFromJson(json_data):
    try:
        file = open(json_data,)
        data = json.load(file)
    except:
        data = json_data
    tasks = []
    for d in data:
        task = {}
        task["_id"]                 = d["Id"]
        task["lat"]                 = d["Latitude"]
        task["lng"]                 = d["Longitude"]
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

def getResourceFromJson(json_data):
    try:
        file = open(json_data,)
        data = json.load(file)
    except:
        data = json_data
    resources = []
    for d in data:
        resource = {}
        resource["stm_id"]          = d["Id"]
        resource["resource_id"]     = d["ServiceResourceId"]
        resource["lat"]             = d["FSL__Internal_SLR_HomeAddress_Geolocation__Latitude__s"]
        resource["lng"]             = d["FSL__Internal_SLR_HomeAddress_Geolocation__Longitude__s"]
        resources.append(resource)
    return resources