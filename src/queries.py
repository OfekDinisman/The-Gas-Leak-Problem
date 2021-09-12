# ServiceAppointment Standard Tasks
QUERY_SA_STD = "SELECT Id, Longitude, Latitude, EarliestStartTime, Simulation_Dataset__c, WorkType.Name, ServiceTerritoryId, SchedStartTime, SchedEndTime, Assigned_Service_Resource__c FROM ServiceAppointment WHERE WorkType.Name='Standard' and Simulation_Dataset__c='%s' ORDER BY Assigned_Service_Resource__c, SchedStartTime"
QUERY_SA_EMG = "SELECT Id, Longitude, Latitude, EarliestStartTime, Simulation_Dataset__c, WorkType.Name, ServiceTerritoryId, SchedStartTime, SchedEndTime, Assigned_Service_Resource__c FROM ServiceAppointment WHERE WorkType.Name='Emergency' and Simulation_Dataset__c='%s' ORDER by Assigned_Service_Resource__c ,SchedStartTime"

# ServiceAppointment Emergency


# ServiceTerritoryMember
QUERY_STM = 'SELECT Id, ServiceResourceId, ServiceTerritoryId, FSL__Internal_SLR_HomeAddress_Geolocation__Latitude__s, FSL__Internal_SLR_HomeAddress_Geolocation__Longitude__s, TerritoryType FROM ServiceTerritoryMember'

# ServiceTerritory
QUERY_ST = 'SELECT Id FROM ServiceTerritory'


# ServiceResource
QUERY_SR = 'SELECT Id FROM ServiceResource'


#MapPolygon
QUERY_POLYGON = 'SELECT Id, Name, FSL__Ma_La__c, FSL__Ma_Lo__c, FSL__Mi_La__c, FSL__Mi_Lo__c, FSL__KML__c, FSL__Service_Territory__c FROM FSL__Polygon__c'
