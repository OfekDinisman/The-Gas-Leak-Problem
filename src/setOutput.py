import json


def setTasksToJson(tasks, jsonfile):
    data = []
    for task in tasks:
        d = {}
        d["Id"]                             = task["_id"]
        d["Latitude"]                       = task["lat"]
        d["Longitude"]                      = task["lng"]
        d["EarliestStartTime"]              = task["startTime"]
        d["WorkType"]["Name"]               = task["workType"] 
        d["ServiceTerritoryId"]             = task["serviceTerritory"]
        d["SchedStartTime"]                 = task["startTime"]
        d["SchedEndTime"]                   = task["endTime"]
        d["Assigned_Service_Resource__c"]   = task["serviceResource"] 
        data.append(d)
    json.dump(data, jsonfile)


def setSTM(id, territory, resource):
    pass