import json
from const import SERVICE_TERRITORY_MEMBER, PREFIX_URL
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


# stm_creator = SFSManager(PREFIX_URL + '/composite')
# r = stm_creator.create_many(STM_BATCH)
stm_creator = SFSManager(SERVICE_TERRITORY_MEMBER)
# r = stm_creator.get_all()
r = stm_creator.delete_one('0Hu4L000000TiyRSAS')
r = stm_creator.create_one(STM)


# params = {"ids": "0Hu4L000000TfNFSA0,0Hu4L000000TgawSAC"}
# r = stm_creator.delete_many(params)

print(json.dumps(r, indent=2))

# with open('file.json', 'w') as f:
#     json.dumps(r, f, indent=2)
