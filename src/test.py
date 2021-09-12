import json
from const import SERVICE_TERRITORY_MEMBER, PREFIX_URL, SERVICE_TERRITORY
from sfs_manager import SFSManager


STM_BATCH = {
"compositeRequest" : [{
  "method" : "POST",
  "url" : "/services/data/v52.0/sobjects/ServiceTerritoryMember",
  "referenceId" : "ref1",
  "body" : {
    "ServiceResourceId": "0Hn4L0000000RVVSA2",
    "FSL__Internal_SLR_HomeAddress_Geolocation__Longitude__s": "-95.437886",
    "FSL__Internal_SLR_HomeAddress_Geolocation__Latitude__s": "29.827403",
    "ServiceTerritoryId": "0Hh4L000000TivFSAS",
    "EffectiveStartDate": "2021-10-30T13:27:00.000+0000",
    "TerritoryType": "S"
   }
  },{
  "method" : "POST",
  "url" : "/services/data/v52.0/sobjects/ServiceTerritoryMember",
  "referenceId" : "ref2",
  "body" : { 
    "ServiceResourceId": "0Hn4L0000000RVVSA2",
    "FSL__Internal_SLR_HomeAddress_Geolocation__Longitude__s": "-95.437886",
    "FSL__Internal_SLR_HomeAddress_Geolocation__Latitude__s": "29.827403",
    "ServiceTerritoryId": "0Hh4L000000TivYSAS",
    "EffectiveStartDate": "2021-08-30T13:27:00.000+0000",
    "TerritoryType": "S"
    }
  }]
}

STM = {
    "ServiceResourceId":"0Hn4L0000000SM2SAM",
    "FSL__Internal_SLR_HomeAddress_Geolocation__Longitude__s": "-95.437886",
    "FSL__Internal_SLR_HomeAddress_Geolocation__Latitude__s": "29.825403",
    "ServiceTerritoryId": "0Hh4L000000TivYSAS",
    "EffectiveStartDate": "2021-08-30T13:27:00.000+0000",
    "TerritoryType": "S" 
}

SA_UPDATE = {
  "records" : [{
      "attributes" : {"type" : "ServiceAppointment"},
      "id" : "08p4L000000h80vQAA",
      "ServiceTerritoryId" : "0Hh4L000000TivYSAS"
   },{
      "attributes" : {"type" : "ServiceAppointment"},
      "id" : "08p4L000000h80wQAA",
      "ServiceTerritoryId" : "0Hh4L000000TivYSAS"
   }]
}

sfs_manager = SFSManager()
# r = sfs_manager.create_many(STM_BATCH)
# r = sfs_manager.get_all(SERVICE_TERRITORY)
# r = sfs_manager.delete_one(SERVICE_TERRITORY_MEMBER, '0Hu4L000000TiyRSAS')
# r = sfs_manager.create_one(SERVICE_TERRITORY_MEMBER, STM)
r = sfs_manager.update_many(SA_UPDATE)

# params = {"ids": "0Hh4L000000TivfSAC,0Hh4L000000TivhSAC,0Hh4L000000TivkSAC,0Hh4L000000TivpSAC,0Hh4L000000TivjSAC,0Hh4L000000TiveSAC,0Hh4L000000TivoSAC"}
# r = sfs_manager.delete_many(params)

print(json.dumps(r, indent=2))

# with open('file.json', 'w') as f:
#     json.dumps(r, f, indent=2)
