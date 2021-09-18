from shapely.geometry import Polygon
import logging

from logger import CreateLog
from sfs_manager import SFSManager
from const import QUERY_URL
from queries import QUERY_SA_STD, QUERY_SA_EMG, QUERY_STM_GAS_LEAK_1, QUERY_POLYGON_MAIN
from getInput import getTasksFromJson, getPolygonsFromJson, getResourceFromJson
from generateModel import GenerateModel
from adopt_model import AdoptModel
from params import SIMULATION_DATASET, COMPLIANCE_RATE, DELAY_TIME, RESOURCE_SPEED

CreateLog("Model %s.log" % SIMULATION_DATASET)

sfs_manager = SFSManager()
tasks = sfs_manager.get_query(QUERY_SA_STD % SIMULATION_DATASET)['records']
tasks = getTasksFromJson(tasks)
logging.info("Recieved %d appointments" % len(tasks))
polygon = sfs_manager.get_query(QUERY_POLYGON_MAIN)['records']
territory = Polygon(getPolygonsFromJson(polygon)[0]["coordinates"])
resources = sfs_manager.get_query(QUERY_STM_GAS_LEAK_1)['records']
resources = getResourceFromJson(resources)
logging.info("Recieved %d resources" % len(resources))

# Generate Model...
logging.info("Generating Model...")
model = GenerateModel(tasks, resources, territory, COMPLIANCE_RATE, DELAY_TIME, RESOURCE_SPEED)
polygons = model.run()

# Adopt Model...
logging.info("Adopting Model...")
adopt = AdoptModel(tasks, polygons, resources, SIMULATION_DATASET)
adopt.run()
