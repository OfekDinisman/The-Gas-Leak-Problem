# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 20:38:41 2021

@author: odinisma
"""
import json
import matplotlib.pyplot as plt
import logging
import dateutil.parser
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
#start
CreateLog("TestAlgo.log")
scheduledAppointmentsPath='src\input\scheduledAppointments.json' #get input json
drivingSpeedKM=40 #driving speed in KMs
#*************
file = open(scheduledAppointmentsPath,)
ListAppointments = json.load(file)
ListResourcesNames=GetResourcesNames(ListAppointments)
ListEmergency=GetEmergencyList(ListAppointments)

#**need to create a loop in here
currentEmergency=ListEmergency[2]
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
        print("distance:", distance)
    #result
    print("MinDistance:",minDistance)
    time = (distance / drivingSpeedKM)*60
    print("time(minutes):",time)
    print("Appointment:\n",minAppointment)
else:
    minDistance=None
    minAppointment=None
        
print('\n ')
#print tasks as a graph
plotTitle="Show Appointments in the same time as the Emergency\nstanard in blue,emergency in red color"
plt.title(plotTitle)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
imageFileName="img_"+currentEmergency['Id']+".png"
plt.savefig(imageFileName)
plt.show()




#
print('end')
