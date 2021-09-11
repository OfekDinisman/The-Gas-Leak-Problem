from shapely.geometry import Polygon

from sfs_manager import SFSManager
from const import QUERY_URL
from queries import QUERY_SA_STD, QUERY_SA_EMG, QUERY_SR
from getInput import getTasksFromJson, getPolygonsFromJson
from generateModel import GenerateModel

SIMULATION_DATASET = None
COMPLIANCE_RATE = 0.9
DELAY_TIME = 30

query_manager = SFSManager(QUERY_URL)

# standard_tasks = query_manager.get_query(QUERY_SA_STD % SIMULATION_DATASET)['records']
tasks = getTasksFromJson("src\input\serviceAppointment3.json")
territory = Polygon(getPolygonsFromJson("src\input\polygonInput.json")[2]["coordinates"])
resources = query_manager.get_query(QUERY_SR)

model = GenerateModel(tasks, resources, territory, COMPLIANCE_RATE, DELAY_TIME)
model.run()
