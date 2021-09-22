from logging import raiseExceptions
from shapely.geometry import Polygon, Point
from scipy.optimize import linear_sum_assignment
import pandas as pd, numpy as np, matplotlib.pyplot as plt
import logging

from const import SERVICE_TERRITORY, SERVICE_TERRITORY_MEMBER, MAP_POLYGON, FSL_FILE, MILLION
from sfs_manager import SFSManager
from methods import get_point_for_poly_from_object


class AdoptModel():
    def __init__(self, tasks, polygons, resources, dataset) -> None:
        self.tasks = tasks
        self.polygons = polygons
        self.resources = resources
        self.sfs_manager = SFSManager()
        self.NUM_OF_POLYS = len(self.polygons)
        self.NUM_OF_TASKS = len(self.tasks)
        self.dataset = dataset
        self.territories = []

    def _get_task_territory_id(self, task):
        point = get_point_for_poly_from_object(task)
        poly_index = self._get_assigned_poly_idx(point)
        return self.territories[poly_index]

    def _get_assigned_poly_idx(self, point):
        # type: (Point) -> int
        for i, poly in enumerate(self.polygons):
            if poly.contains(point):
                return i
        raiseExceptions("Point not in a Polygon")

    def _get_resource_territory_id(self, resource):
        return self.territories[self.resource_assignment[resource]]

    def create_cost_array(self):
        cost_array = []
        for resource in self.resources:
            point = get_point_for_poly_from_object(resource)
            cost_array_row = []
            for poly in self.polygons:
                cost_array_row.append(point.distance(poly))
            cost_array.append(cost_array_row)
        return cost_array

    def assign_resource_to_territory(self):
        cost_array = self.create_cost_array()
        row_ind, col_ind = linear_sum_assignment(cost_array)
        self.resource_assignment = col_ind


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
                    "OperatingHoursId": "0OH4L000000Tfp8WAC", # Houston hours
                    "isActive": True
                }
            }
            composite.append(st)
            # create in batches of 25
            if (i+1) % 25 == 0 or i == self.NUM_OF_POLYS - 1:
                response = self.sfs_manager.create_many({"compositeRequest": composite})
                self.territories += [res["body"]["id"] for res in response["compositeResponse"]]
                logging.info("Created %d STs." % len(composite))
                composite = []
 
    def createPolygons(self):
        composite = []
        for i, poly in enumerate(self.polygons):
            params = self.get_params_from_poly(poly)
            territory_id = self.territories[i]
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
            # create in batches of 25
            if (i+1) % 25 == 0 or i == self.NUM_OF_POLYS - 1:
                self.sfs_manager.create_many({"compositeRequest": composite})
                logging.info("Created %d Polygons." % len(composite))
                composite = []

    def updateServiceAppointments(self):
        records = []
        for i, task in enumerate(self.tasks):
            task_territory_id = self._get_task_territory_id(task)
            task_info = {
                "attributes" : {"type" : "ServiceAppointment"},
                "id" : task["_id"],
                "ServiceTerritoryId" : task_territory_id
            }
            records.append(task_info)

            # create in batches of 25
            if (i+1) % 25 == 0 or i == self.NUM_OF_TASKS - 1:
                self.sfs_manager.update_many({"records": records})
                logging.info("Updated %d SAs." % len(records))
                records = []

    def createServiceTerritoryMembers(self):
        composite = []
        stm = []
        for i, resource in enumerate(self.resources):
            resource_territory_id = self._get_resource_territory_id(i)
            sr = {
                "method": "POST",
                "url": SERVICE_TERRITORY_MEMBER,
                "referenceId": "ref" + str(i),
                "body": {
                    "ServiceResourceId": resource["resource_id"],
                    "ServiceTerritoryId": resource_territory_id,
                    "EffectiveStartDate": "2021-01-30T13:27:00.000+0000",
                    "TerritoryType": "S"
                }
            }
            composite.append(sr)
            # create in batches of 25
            if (i+1) % 25 == 0 or i == self.NUM_OF_POLYS - 1:
                response = self.sfs_manager.create_many({"compositeRequest": composite})
                stm += [res["body"]["id"] for res in response["compositeResponse"]]
                logging.info("Created %d STMs." % len(composite))
                composite = []
        return stm


    def run(self):
        # for every Polygon create a Service Territory
        logging.info("Creating service territories...")
        self.createServiceTerritories()

        # create polygons
        logging.info("Creating polygons...")
        self.createPolygons()

        # update SA to new STs
        logging.info("Updating service appointments...")
        self.updateServiceAppointments()

        # create STMs
        logging.info("Assigning resource to territory...")
        self.assign_resource_to_territory()
        logging.info("Creating service territory members...")
        self.createServiceTerritoryMembers()


        df = pd.DataFrame.from_dict(self.resources)
        X = np.array(df[['lng', 'lat']]) * MILLION
        X.astype(int)
        for i in range(self.NUM_OF_POLYS):
            xs, xy = self.polygons[self.resource_assignment[i]].exterior.xy
            plt.plot(xs, xy)
            x, y = X[i].T
            plt.scatter(x, y)
        plt.show()

        return self.territories