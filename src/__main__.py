from shapely.geometry import Polygon

from sfs_manager import SFSManager
from const import QUERY_URL
from queries import QUERY_SA_STD, QUERY_SA_EMG, QUERY_SR
from getInput import getTasksFromJson, getPolygonsFromJson
from generateModel import GenerateModel
from adopt_model import AdoptModel


SIMULATION_DATASET = 1
COMPLIANCE_RATE = 0.9
DELAY_TIME = 30

sfs_manager = SFSManager()

standard_tasks = sfs_manager.get_query(QUERY_SA_STD % SIMULATION_DATASET)['records']
tasks = getTasksFromJson(standard_tasks)
# tasks = getTasksFromJson("src\input\serviceAppointment3.json")
territory = Polygon(getPolygonsFromJson("src\input\polygonInput.json")[2]["coordinates"])
resources = sfs_manager.get_query(QUERY_SR)['records']

# Generate Model...
model = GenerateModel(tasks, resources, territory, COMPLIANCE_RATE, DELAY_TIME)
polygons = model.run()

# Adopt Model...
adopt = AdoptModel(tasks, polygons, resources, SIMULATION_DATASET)
stms = adopt.run()

# Optimize...

# Test...
# double MinLat  = 29.56388233493162;
# double MaxLat  = 29.820414777342126;
# double MinLong = -95.0920235039353;
# double MaxLong = -95.9933880169435;