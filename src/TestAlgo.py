# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 20:38:41 2021

@author: odinisma
"""
import json
import matplotlib.pyplot as plt
import logging
import dateutil.parser

from logger import CreateLog

def GetResourcesNames(ListAppointments):
    my_set=set()
    for item in ListAppointments:
        my_set.add(item['Assigned_Service_Resource__c'])
    ListResourcesNames = list(set(my_set))
    return ListResourcesNames

def GetDistanceTwoPoints(lon1,lat1,lon2,lat2):
    from math import sin, cos, sqrt, atan2, radians

    # approximate radius of earth in km
    R = 6373.0
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

def GetEmergencyList(ListAppointments):
    ListEmergency=list()
    for appoint in ListAppointments:
        #get Emergency info
        if  appoint['WorkType']['Name']=="Emergency":
            ListEmergency.append(appoint)
    return ListEmergency

def GetDateTime(date):
    if not date:
        return None
    dt=dateutil.parser.parse((date.split("+")[0])+'Z')
    return dt

def IsAppointmentDuringEmergency(appoint,emergen):#get appointment and emercency and check if they are happening at the same time
    appointds  = GetDateTime(appoint['SchedStartTime'])#start time   
    emergends = GetDateTime(emergen['SchedStartTime'])#""
    appointes = GetDateTime(appoint['SchedEndTime'])#end time   
    emergenes = GetDateTime(emergen['SchedEndTime'])#""
    if(appointds==emergends or appointes==emergenes):
        return True
    if(appointds<emergends and appointes>emergends):
        return True
    if(appointds<emergenes and appointes>emergenes):
        return True
    return False

def get_json_data(ListEmergencyOutput):
    '''
    Convert string array to json array
    '''
    result = []
    for item in ListEmergencyOutput:
        result.append(json.loads(item.toJSON()))
    return json.dumps(result)

def GetSucceedCount(ListEmergencyOutput):
    count=0
    for item in ListEmergencyOutput:
        if item.isSucceed==True:
            count=count+1
    return count

def GetSuccessRate(ListEmergencyOutput):
    count=GetSucceedCount(ListEmergencyOutput)
    presentage= (count / len(ListEmergencyOutput)) *100 
    return presentage



class EmergencyOutput():
    def __init__(self, distance,isSucceed,resource,appointment,emergency):
        self.distance = distance  # distance between the nearst appointment and emergency
        self.isSucceed = isSucceed  # is succeed=True or failed=False
        self.resource = resource  # resource name
        self.appointment = appointment  # appointment ID
        self.emergency = emergency  # emergency ID
        
    def toJSON(self):
           return json.dumps(self, default=lambda o: o.__dict__, 
               sort_keys=True, indent=4)
#start
CreateLog("TestAlgo.log")
scheduledAppointmentsPath='src\input\scheduledAppointments.json' #get input json
drivingSpeedKM=40 #driving speed in KMs
arrivalTimeToEmergency=60 #max time to get to the emergnecy in minutes
#*************
file = open(scheduledAppointmentsPath,)
ListAppointments = json.load(file)
ListResourcesNames=GetResourcesNames(ListAppointments)
ListEmergency=GetEmergencyList(ListAppointments)
#output
ListEmergencyOutput=[]

#**need to create a loop in here
for currentEmergency in ListEmergency:
    plt.scatter(currentEmergency['Longitude'], currentEmergency['Latitude'], c='red')
    ListAppInSameTime=list()#reset List
    for resourceName in ListResourcesNames:
        for appoint in ListAppointments:
            #get standard tasks info
            if appoint['Assigned_Service_Resource__c']==resourceName and appoint['WorkType']['Name']=="Standard":
                if IsAppointmentDuringEmergency(appoint,ListEmergency[2])==True:
                    ListAppInSameTime.append(appoint)
                    plt.scatter(appoint['Longitude'], appoint['Latitude'], c='blue')
                    
    #calculate distance between emergncy and standard tasks
    if len(ListAppInSameTime) > 0:
        #init value
        minDistance=GetDistanceTwoPoints(ListAppInSameTime[0]['Longitude'],ListAppInSameTime[0]['Latitude'],currentEmergency['Longitude'],currentEmergency['Latitude'])
        minAppointment=ListAppInSameTime[0]
        for appInSameTime in ListAppInSameTime:       
            distance=GetDistanceTwoPoints(appInSameTime['Longitude'],appInSameTime['Latitude'],currentEmergency['Longitude'],currentEmergency['Latitude'])#calculate distance between appointment point and emergncy
            if distance<minDistance:#save min distance
                minDistance=distance
                minAppointment=appInSameTime
            #print("distance:", distance)
            
        #result
        #save result to object
        time = (distance / drivingSpeedKM)*60#calculate time to get to emergency
        eo=EmergencyOutput(minDistance,time<=arrivalTimeToEmergency,minAppointment['Assigned_Service_Resource__c'],minAppointment['Id'],currentEmergency['Id'])
        ListEmergencyOutput.append(eo)#add it to the list of all results
        logging.info("MinDistance:"+str(eo.distance))
        
        if eo.isSucceed==True:
            logging.info('Success')
        else:
            logging.info('Fail')
            
        logging.info("Appointment:"+str(eo.appointment))
        logging.info("Resource:"+str(eo.resource))
        logging.info("Emergency:"+str(eo.emergency))
        #mark the chosen appointment on the plot
        plt.scatter(minAppointment['Longitude'], minAppointment['Latitude'], c='green')
         
    else:
        minDistance=None
        minAppointment=None
        logging.info('Fail to get to emergency')
        eo=EmergencyOutput(None,False,None,None,currentEmergency['Id'])#didn't find a match to the emergency
        ListEmergencyOutput.append(eo)#add it to the list of all results

    logging.info('\n ')
    #print tasks as a graph
    plotTitle="Show Appointments in the same time as the Emergency\nstandard in blue,nearest in green,emergency in red color"
    plt.title(plotTitle)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    imageFileName="img_"+currentEmergency['Id']+".png"
    plt.savefig(imageFileName)
    plt.show()

#output
presentage=GetSuccessRate(ListEmergencyOutput)
jsonOutput=get_json_data(ListEmergencyOutput)
#write json to file
with open('ListEmergencyOutput.json', 'w') as f:
   f.write(jsonOutput)
#
print("SuccessRate:"+str(presentage))
logging.info("SuccessRate:"+str(presentage))
logging.info('end')
print('end')
