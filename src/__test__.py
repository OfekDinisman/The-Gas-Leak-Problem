import logging
from test_model import TestModel
from sfs_manager import SFSManager
from params import SIMULATION_DATASET, COMPLIANCE_RATE, DELAY_TIME, RESOURCE_SPEED
from queries import QUERY_SCHED_SA_STD, QUERY_SA_EMG, QUERY_STM_GAS_LEAK_1, QUERY_ASSIGNED_RESOURCE
from getInput import getTasksFromJson, getResourceFromJson, getAssignedResource
from logger import CreateLog


CreateLog("Test %s.log" % SIMULATION_DATASET)

# API requests from SFS
sfs_manager = SFSManager()
scheduled_tasks = sfs_manager.get_query(QUERY_SCHED_SA_STD % SIMULATION_DATASET)['records']
scheduled_tasks = getTasksFromJson(scheduled_tasks)
logging.info("Recieved %d appointments" % len(scheduled_tasks))
emergencies = sfs_manager.get_query(QUERY_SA_EMG % SIMULATION_DATASET)['records']
emergencies = getTasksFromJson(emergencies)
logging.info("Recieved %d emergencies" % len(emergencies))
resources = sfs_manager.get_query(QUERY_STM_GAS_LEAK_1)['records']
resources = getResourceFromJson(resources)
assigned_resources = sfs_manager.get_query(QUERY_ASSIGNED_RESOURCE)['records']
assigned_resources = getAssignedResource(assigned_resources)

test = TestModel(scheduled_tasks, emergencies, resources, assigned_resources, COMPLIANCE_RATE, DELAY_TIME, RESOURCE_SPEED)
result, total_success_rate = test.run()
logging.info("The overall success rate is %d%%" % total_success_rate)