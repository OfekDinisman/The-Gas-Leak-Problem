from logging import raiseExceptions
from shapely.geometry import Polygon, Point

from const import SERVICE_TERRITORY, SERVICE_TERRITORY_MEMBER, MAP_POLYGON, FSL_FILE, MILLION
from sfs_manager import SFSManager


class AdoptModel():
    def __init__(self, tasks, polygons, resources, dataset) -> None:
        self.tasks = tasks
        self.polygons = polygons
        self.resources = resources
        self.sfs_manager = SFSManager()
        self.NUM_OF_POLYS = len(self.polygons)
        self.dataset = dataset

    def _get_point_from_task(self, task):
        return Point(task['lng'] * MILLION, task['lat'] * MILLION)

    def _get_task_territory_id(self, task):
        point = self._get_point_from_task(task)
        poly_index = self._get_assigned_poly_idx(point)
        return self.ST[poly_index]

    def _get_assigned_poly_idx(self, point):
        for i, poly in enumerate(self.polygons):
            if poly.contains(point):
                return i
        raiseExceptions("Point not in a Polygon")

    # TODO:
    def _get_resource_territory_id(resource):
        pass

    @staticmethod
    def get_params_from_poly(polygon):
        params = {}
        minx, miny, maxx, maxy = polygon.bounds
        params["minLng"] = minx
        params["minLat"] = miny
        params["maxLng"] = maxx
        params["maxLat"] = maxy
        coords = list(polygon.exterior.coords)
        coords_str = ""
        for coord in coords:
            lng = coord[0] / MILLION
            lat = coord[1] / MILLION
            coords_str += "%s,%s,0\n" % (str(lng), str(lat))
        params["coordinate_string"] = coords_str
        return params

    def createServiceTerritories(self):
        composite = []
        for i in range(self.NUM_OF_POLYS):
            st = {
                "method": "POST",
                "url": SERVICE_TERRITORY,
                "referenceId": "ref" + str(i),
                "body": {
                    "Name": "SET" + str(self.dataset) + "ST" + str(i),
                    "OperatingHoursId": "0OH4L000000Tfp8WAC",
                    "isActive": True
                }
            }
            composite.append(st)
        return self.sfs_manager.create_many({"compositeRequest": composite})
 
    def createPolygons(self):
        composite = []
        for i, poly in enumerate(self.polygons):
            params = self.get_params_from_poly(poly)
            territory_id = self.ST[i]
            mp = {
                "method": "POST",
                "url": MAP_POLYGON,
                "referenceId": "ref" + str(i),
                "body": {
                    "Name": "SET" + str(self.dataset) + "POLY" + str(i),
                    "FSL__Ma_La__c": params["maxLat"],
                    "FSL__Ma_Lo__c": params["maxLng"],
                    "FSL__Mi_La__c": params["minLat"],
                    "FSL__Mi_Lo__c": params["minLng"],
                    "FSL__KML__c": FSL_FILE % params["coordinate_string"],
                    "FSL__Service_Territory__c": territory_id
                }
            }
            composite.append(mp)
        return self.sfs_manager.create_many({"compositeRequest": composite})

    def updateServiceAppointments(self):
        records = []
        for task in self.tasks:
            task_territory_id = self._get_task_territory_id(task)
            task_info = {
                "attributes" : {"type" : "ServiceAppointment"},
                "id" : task["_id"],
                "ServiceTerritoryId" : task_territory_id
            }
            records.append(task_info)
        return self.sfs_manager.update_many({"records": records})

    def createServiceTerritoryMembers(self):
        composite = []
        for i, resource in enumerate(self.resources):
            resource_territory_id = self._get_resource_territory_id(resource)
            sr = {
                "method": "POST",
                "url": SERVICE_TERRITORY_MEMBER,
                "referenceId": "ref" + str(i),
                "body": {
                    "ServiceResourceId": resource["resource_id"],
                    # "FSL__Internal_SLR_HomeAddress_Geolocation__Longitude__s": "-95.437886",
                    # "FSL__Internal_SLR_HomeAddress_Geolocation__Latitude__s": "29.827403",
                    "ServiceTerritoryId": resource_territory_id,
                    "EffectiveStartDate": "2021-01-30T13:27:00.000+0000",
                    "TerritoryType": "S"
                }
            }
            composite.append(sr)
        return self.sfs_manager.create_many({"compositeRequest": composite})


    def run(self):
        # for every Polygon create a Service Territory
        response = self.createServiceTerritories()
        self.ST = [res["body"]["id"] for res in response["compositeResponse"]]
        # self.ST = ['0Hh4L000000TiwSSAS', '0Hh4L000000TiwXSAS', '0Hh4L000000TiwcSAC', '0Hh4L000000TiwTSAS']

        # create polygons
        self.createPolygons()

        # update SA to new STs
        self.updateServiceAppointments()

        # create STMs
        # stms = self.createServiceTerritoryMembers()

        return stms