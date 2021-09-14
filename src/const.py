#REST API URLs
PREFIX_URL = '/services/data/v52.0'

SERVICE_APPOINTMENT          = PREFIX_URL + '/sobjects/ServiceAppointment'
SERVICE_RESOURCE             = PREFIX_URL + '/sobjects/ServiceResource'
SERVICE_TERRITORY            = PREFIX_URL + '/sobjects/ServiceTerritory'
SERVICE_TERRITORY_MEMBER     = PREFIX_URL + '/sobjects/ServiceTerritoryMember'
MAP_POLYGON                  = '/services/data/v51.0/sobjects/FSL__Polygon__c'
QUERY_URL                    = PREFIX_URL + '/query'
COMPOSITE                    = PREFIX_URL + '/composite'


FSL_FILE = "<?xml version=\"1.0\" encoding=\"UTF-8\"?> \n                            <kml xmlns=\"http://www.opengis.net/kml/2.2\">\n                                <Style id=\"example2Style\"> \n                                    <LineStyle> \n                                        <width>1</width> \n                                    </LineStyle> \n                                    <PolyStyle> \n                                        <color>80c0f09d</color> \n                                    </PolyStyle> \n                                </Style> \n                                <Placemark> \n                                    <name>example2</name> \n                                    <styleUrl>#example2Style</styleUrl> \n                                    <Polygon>\n                    <outerBoundaryIs>\n                                    <LinearRing>\n                                        <coordinates>%s</coordinates>\n                                    </LinearRing>\n                                 </outerBoundaryIs>\n                    \n                </Polygon>\n                                </Placemark> \n                            </kml>"

MILLION = 1000000