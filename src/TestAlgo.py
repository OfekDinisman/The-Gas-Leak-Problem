# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 20:38:41 2021

@author: odinisma
"""
import json
import matplotlib.pyplot as plt
import logging
def GetResourcesNames(ListAppointments):
    my_set=set()
    for item in ListAppointments:
        my_set.add(item['Assigned_Service_Resource__c'])
    ListResourcesNames = list(set(my_set))
    return ListResourcesNames
def GetDistanceTwoPoints(lon1,lat1,lon2,lat2):

#Inputs:
    from math import sin, cos, sqrt, atan2, radians

    # approximate radius of earth in km
    R = 6373.0
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    
    return distance
def CreateLog(fileName):

    # Set up logging
    log = fileName
    logging.basicConfig(filename=log,level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    logging.info('Start:')
def GetEmergencyList(ListAppointments):
    ListEmergency=list()
    for appoint in ListAppointments:
        #get Emergency info
        if  appoint['WorkType']['Name']=="Emergency":
            ListEmergency.append(appoint)
    return ListEmergency
def IsAppointmentDuringEmergency(appoint,emergen):#get appointment and emercency and check if they are happening at the same time
    if(appoint['SchedStartTime']<=emergen['SchedStartTime']) and appoint['SchedEndTime']>=emergen['SchedEndTime']:
        return True
    return False

#app 6<=7 - 8>7
# 7
#start
CreateLog("TestAlgo.log")
scheduledAppointmentsPath='input\scheduledAppointments.json' #get input json
drivingSpeedKM=40 #driving speed in KMs
#*************
file = open(scheduledAppointmentsPath,)
ListAppointments = json.load(file)
ListResourcesNames=GetResourcesNames(ListAppointments)
ListEmergency=GetEmergencyList(ListAppointments)

for resourceName in ListResourcesNames:
    emergencyLong=0
    emergencyLat=0
    ListResources=list()
    print(resourceName)
    print('\n ')
    for appoint in ListAppointments:
        #get standard tasks info
        if appoint['Assigned_Service_Resource__c']==resourceName and appoint['WorkType']['Name']=="Standard":
            plt.scatter(appoint['Longitude'], appoint['Latitude'], c='blue')
            ListResources.append(appoint)
    
    #calculate distance between emergncy and standard tasks
    for resource in ListResources:       
        distance=GetDistanceTwoPoints(resource['Longitude'],resource['Latitude'],emergencyLong,emergencyLat)
        time = (distance / drivingSpeedKM)*60
        print("distance:", distance)
        print("time(minutes):",time)
        
    print('\n ')
    #print tasks as a graph
    plotTitle="Show Appointments for resource:"+resourceName+"\nstanard in blue,emergency in red color"
    plt.title(plotTitle)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    imageFileName="img_"+resourceName+".png"
    plt.savefig(imageFileName)
    plt.show()




#
print('end')
