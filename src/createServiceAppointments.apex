/** HOUSETON  downtown **/

double latitude = 29.737882871554312;
double longitude = -95.46285831417906;
double radius = 0.3;


DateTime StartDate = DateTime.newInstance(2022, 1, 10, 9, 00, 00);
DateTime EndDate = DateTime.newInstance(2022, 1, 10, 18, 00, 00);
String Simulation_Dataset = '2';

double MinLat  = 29.4359136;
double MaxLat  = 30.06543314;
double MinLong = -95.807349900;
double MaxLong = -95.052039;
System.debug('LatScale: ' + (MaxLat - MinLat));
System.debug('LongScale: ' + (MinLong + (-1*MaxLong)));


Integer numOfServices=360;
double ratioEmg = 0.1;

Id territoryGasLeak1 = [SELECT id FROM ServiceTerritory where Name='GasLeak1'].Id;
Id territoryGasLeak2 = [SELECT id FROM ServiceTerritory where Name='GasLeak2'].Id;
Id workTypeNormal = [Select Id from WorkType where Name='Standard'].Id;
Id workTypeEmergency = [Select Id from WorkType where Name='Emergency'].Id;

WorkOrder standardWO = new WorkOrder();
standardWO.ServiceTerritoryId = territoryGasLeak1;
standardWO.WorkTypeId = workTypeNormal;
insert standardWO;

List<ServiceAppointment> serviceAppointments = new List<ServiceAppointment>();

for (Integer i=0; i<numOfServices; i++){
    ServiceAppointment sa = new ServiceAppointment();
    sa.ServiceTerritoryId = territoryGasLeak1;
    sa.ParentRecordId = standardWO.Id;
    sa.Latitude = MinLat + (Math.random() * (MaxLat - MinLat));
    sa.Longitude = MaxLong + (Math.random() * (MinLong + (-1*MaxLong)));
    sa.EarliestStartTime = StartDate;
    sa.DueDate = EndDate;
    sa.Simulation_Dataset__c = Simulation_Dataset;
    serviceAppointments.add(sa);
}


WorkOrder emergencyWO = new WorkOrder();
emergencyWO.ServiceTerritoryId = territoryGasLeak2;
emergencyWO.WorkTypeId = workTypeEmergency;
insert emergencyWO;

for(Integer i=0; i< (numOfServices * ratioEmg); i++){
    ServiceAppointment sa = new ServiceAppointment();
    sa.ServiceTerritoryId = territoryGasLeak2;
    sa.ParentRecordId = emergencyWO.Id;
    sa.Latitude = latitude + (Math.random() -0.5) * radius;
    sa.Longitude = longitude + (Math.random() -0.5) * radius;
    // Emergency Time
    sa.SchedStartTime = StartDate + 3/24 + (Math.random() * (8.0/24)); // + ~8h 
    sa.SchedEndTime = sa.SchedStartTime + (1.0/24) ; // 1h;
    System.debug('StartDate: ' + sa.SchedStartTime);
    System.debug('EndDate: ' + sa.SchedEndTime);
    sa.Simulation_Dataset__c = Simulation_Dataset;
    serviceAppointments.add(sa);
}

insert serviceAppointments;
