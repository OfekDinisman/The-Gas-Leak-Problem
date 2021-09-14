import json
from const import SERVICE_TERRITORY_MEMBER, PREFIX_URL, SERVICE_TERRITORY, MAP_POLYGON, FSL_FILE
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
# double MinLat  = 29.56388233493162;
# double MaxLat  = 29.820414777342126;
# double MinLong = -95.0920235039353;
# double MaxLong = -95.9933880169435;
coords = "-95.9933880169435,29.820414777342126,0\n-95.9933880169435,29.56388233493162,0\n-95.0920235039353,29.56388233493162,0\n-95.0920235039353,29.820414777342126,0\n-95.9933880169435,29.820414777342126,0\n"
CREATE_POLY = {
  "Name": "Houston_Main",
  "FSL__Ma_La__c": 29.820414777342126,
  "FSL__Ma_Lo__c": -95.9933880169435,
  "FSL__Mi_La__c": 29.56388233493162,
  "FSL__Mi_Lo__c": -95.0920235039353,
  "FSL__KML__c": FSL_FILE % coords,
  "FSL__Service_Territory__c": "0Hh4L000000TfLBSA0"
}

MANY_POLYS = {
"compositeRequest" : [{
  "method" : "POST",
  "url" : "/services/data/v51.0/sobjects/FSL__Polygon__c",
  "referenceId" : "ref1",
  "body" : {
    "Name": "example5",
    "FSL__Ma_La__c": 29.7456539367767,
    "FSL__Ma_Lo__c": -95.00400669833253,
    "FSL__Mi_La__c": 29.533192882060835,
    "FSL__Mi_Lo__c": -95.33908970614503,
    "FSL__KML__c": "<?xml version=\"1.0\" encoding=\"UTF-8\"?> \n                            <kml xmlns=\"http://www.opengis.net/kml/2.2\">\n                                <Style id=\"example2Style\"> \n                                    <LineStyle> \n                                        <width>1</width> \n                                    </LineStyle> \n                                    <PolyStyle> \n                                        <color>80c0f09d</color> \n                                    </PolyStyle> \n                                </Style> \n                                <Placemark> \n                                    <name>example2</name> \n                                    <styleUrl>#example2Style</styleUrl> \n                                    <Polygon>\n                    <outerBoundaryIs>\n                                    <LinearRing>\n                                        <coordinates>-95.0081265713794,29.736114752522607,0\n-95.00400669833253,29.533192882060835,0\n-95.27591831942628,29.533192882060835,0\n-95.29789097567628,29.641866618837206,0\n-95.33908970614503,29.705106138609562,0\n-95.30887730380128,29.7456539367767,0\n-95.26218540927003,29.737307200175735,0\n-95.21549351473878,29.711070077572373,0\n-95.0081265713794,29.736114752522607,0\n</coordinates>\n                                    </LinearRing>\n                                 </outerBoundaryIs>\n                    \n                </Polygon>\n                                </Placemark> \n                            </kml>",
    "FSL__Service_Territory__c": "0Hh4L000000TivYSAS"
    }
  },{
  "method" : "POST",
  "url" : "/services/data/v51.0/sobjects/FSL__Polygon__c",
  "referenceId" : "ref2",
  "body" : {
    "Name": "example6",
    "FSL__Ma_La__c": 29.7456539367767,
    "FSL__Ma_Lo__c": -95.00400669833253,
    "FSL__Mi_La__c": 29.533192882060835,
    "FSL__Mi_Lo__c": -95.33908970614503,
    "FSL__KML__c": "<?xml version=\"1.0\" encoding=\"UTF-8\"?> \n                            <kml xmlns=\"http://www.opengis.net/kml/2.2\">\n                                <Style id=\"example2Style\"> \n                                    <LineStyle> \n                                        <width>1</width> \n                                    </LineStyle> \n                                    <PolyStyle> \n                                        <color>80c0f09d</color> \n                                    </PolyStyle> \n                                </Style> \n                                <Placemark> \n                                    <name>example2</name> \n                                    <styleUrl>#example2Style</styleUrl> \n                                    <Polygon>\n                    <outerBoundaryIs>\n                                    <LinearRing>\n                                        <coordinates>-95.0081265713794,29.736114752522607,0\n-95.00400669833253,29.533192882060835,0\n-95.27591831942628,29.533192882060835,0\n-95.29789097567628,29.641866618837206,0\n-95.33908970614503,29.705106138609562,0\n-95.30887730380128,29.7456539367767,0\n-95.26218540927003,29.737307200175735,0\n-95.21549351473878,29.711070077572373,0\n-95.0081265713794,29.736114752522607,0\n</coordinates>\n                                    </LinearRing>\n                                 </outerBoundaryIs>\n                    \n                </Polygon>\n                                </Placemark> \n                            </kml>",
    "FSL__Service_Territory__c": "0Hh4L000000TivYSAS"
    }
  }]
}

sfs_manager = SFSManager()
# r = sfs_manager.create_many(STM_BATCH)
# r = sfs_manager.get_all(SERVICE_TERRITORY)
# r = sfs_manager.delete_one(SERVICE_TERRITORY_MEMBER, '0Hu4L000000TiyRSAS')
# r = sfs_manager.create_one(SERVICE_TERRITORY_MEMBER, STM)
# r = sfs_manager.update_many(SA_UPDATE)
r = sfs_manager.create_one(MAP_POLYGON, CREATE_POLY)
# r = sfs_manager.create_many(MANY_POLYS)

# params = {"ids": "0Hh4L000000TivfSAC,0Hh4L000000TivhSAC,0Hh4L000000TivkSAC,0Hh4L000000TivpSAC,0Hh4L000000TivjSAC,0Hh4L000000TiveSAC,0Hh4L000000TivoSAC"}
# r = sfs_manager.delete_many(params)

print(json.dumps(r, indent=2))

# with open('file.json', 'w') as f:
#     json.dumps(r, f, indent=2)
