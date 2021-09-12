from logging import raiseExceptions
from shapely.geometry import Polygon, Point

from const import SERVICE_TERRITORY
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
        return Point(task['lng'] * 1000000, task['lat'] * 1000000)

    def _get_task_territory_id(self, task):
        point = self._get_point_from_task(task)
        poly_index = self._get_assigned_poly_idx(point)
        return self.ST[poly_index]

    def _get_assigned_poly_idx(self, point):
        for poly in self.polygons:
            if self.polygons[poly].contains(point):
                return poly
        raise "Point not in a Polygon"

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

    def createServiceTerritoryMemebers(self):
        pass

    def run(self):
        # for every Polygon create a Service Territory - get ST ID
        response = self.createServiceTerritories()
        self.ST = [res["body"]["id"] for res in response["compositeResponse"]]
        # self.ST = ['0Hh4L000000TiwSSAS', '0Hh4L000000TiwXSAS', '0Hh4L000000TiwcSAC', '0Hh4L000000TiwTSAS']

        # assign points to polygon and give them Territory ID
        self.updateServiceAppointments()

        # assign resource to polygon
        
        # for every resource
            # create STM and assign Service Resource Id and Service Territory Id

