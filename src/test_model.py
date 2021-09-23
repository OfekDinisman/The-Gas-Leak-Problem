from datetime import datetime
import pytz
from dateutil import parser
import logging

from methods import get_point_from_object

class TestModel:
    def __init__(self, scheduled_tasks, emergencies, resources, assigned_resources, COMPLIANCE_RATE, DELAY_TIME, RESOURCE_SPEED) -> None:
        self.scheduled_tasks = scheduled_tasks
        self.emergencies = emergencies
        self.resources = resources
        self.assigned_resources = assigned_resources
        self.COMPLIANCE_RATE = COMPLIANCE_RATE
        self.DELAY_TIME = DELAY_TIME
        self.RESOURCE_SPEED = RESOURCE_SPEED

    def getTasksResourceId(self, assignment_id):
        return self.assigned_resources[assignment_id] # return resource_id

    @staticmethod
    def getDistanceTwoPointsinKM(point1, point2):
        from math import sin, cos, acos, radians
        R = 6371.0  # approximate radius of earth in km
        distance = acos(sin(radians(point1.y))*sin(radians(point2.y))+cos(radians(point1.y))*cos(radians(point2.y))*cos(radians(point2.x)-radians(point1.x)))*R
        return distance

    @staticmethod
    def getDateTime(date):
        if not date:
            return None
        dt = parser.parse((date.split("+")[0])+'Z')
        return dt

    def getResourcesTasks(self):
        ''' Returns a list of tasks for each resource'''
        resource_tasks ={}
        for task in self.scheduled_tasks:
            resource_id = self.getTasksResourceId(task["_id"])
            current_resource_tasks = resource_tasks.get(resource_id) or []
            current_resource_tasks.append(task)
            resource_tasks[resource_id] = current_resource_tasks
        return resource_tasks

    def getResourceTaskBeforeEmg(self, resource, task_list, emergency): 
        ''' Returns resources last task before emergency starts'''
        emergency_start_time = self.getDateTime(emergency['schedStartTime'])
        current_task = None
        current_task_time = datetime.min.replace(tzinfo=pytz.UTC)
        for task in task_list:
            task_start_time  = self.getDateTime(task['schedStartTime'])
            if task_start_time <= emergency_start_time and task_start_time > current_task_time:
                current_task = task
                current_task_time = task_start_time
        return current_task or resource

    def getTasksBeforeEmg(self):
        # type: () -> dict[list]
        ''' Returns a list of tasks in same timeframe as emergency'''
        emergency_tasks ={}
        resource_tasks = self.getResourcesTasks()
        for emergency in self.emergencies:
            tasks_during_emg = []
            for resource in self.resources:
                task = self.getResourceTaskBeforeEmg(resource, resource_tasks[resource["resource_id"]], emergency)
                tasks_during_emg.append(task)
            emergency_tasks[emergency["_id"]] = tasks_during_emg
        return emergency_tasks

    def getNearestTask(self, emergency, task_list):
        closest_task = task_list[0]
        min_distance = self.getDistanceTwoPointsinKM(get_point_from_object(task_list[0]), get_point_from_object(emergency))
        for task in task_list:
            distance = self.getDistanceTwoPointsinKM(get_point_from_object(task), get_point_from_object(emergency))
            if distance < min_distance:
                min_distance = distance
                closest_task = task
        return closest_task, min_distance

    def run(self):
        result = []
        success_count = 0
        total_time = 0
        emergency_tasks = self.getTasksBeforeEmg()
        for emergency in self.emergencies:
            task, distance = self.getNearestTask(emergency, emergency_tasks[emergency["_id"]])
            if len(task) < 6: # task is actually the resources home
                task_id = "Resource Home"
                resource_id = task["resource_id"]
            else:
                task_id = task["_id"]  
                resource_id = self.getTasksResourceId(task["_id"])
            time_to_emg = (distance / self.RESOURCE_SPEED) * 60  # minutes
            total_time += time_to_emg
            successful_emg = time_to_emg <= self.DELAY_TIME
            if successful_emg: success_count += 1

            emergency_result = {
                "Emergency": emergency["_id"],
                "Nearest Task": task_id,
                "Resource": resource_id,
                "Distance": distance,
                "Time to emergency": time_to_emg,
                "Successful": successful_emg,
            }
            logging.info(emergency_result)
            result.append(emergency_result)

        average_time = total_time / len(self.emergencies)
        success_rate = success_count / len(self.emergencies)
        return result, round(success_rate * 100), average_time


