from sfs_manager import SFSManager

class Optimize:
    def __init__(self, stms, dataset) -> None:
        self.stms = stms
        self.dataset = dataset

    def create_apexfile(self):
        with open("src\optimize%s.apex" % self.dataset, 'w') as f:
            firstLines = [
                "DateTime start = DateTime.newInstance(2022, 1, 4, 9, 00, 00);\n",
                "DateTime finish = start.addDays(3);\n",
                "LIST<Id> lstServiceTerritories = new List<Id>();\n"
            ]
            f.writelines(firstLines)
            for stm in self.stms:
                f.write("lstServiceTerritories.add('%s');\n" % stm)
            endlines = [
                "FSL.OAASRequest oaasRequest = new FSL.OAASRequest();\n"
                "oaasRequest.allTasksMode = true;\n"
                "oaasRequest.filterFieldAPIName = IsStandardTask__c;\n"
                "oaasRequest.start = start;\n"
                "oaasRequest.finish = finish;\n"
                "oaasRequest.includeServicesWithEmptyLocation = false;\n"
                "oaasRequest.locations = lstServiceTerritories;\n"
                "oaasRequest.schedulingPolicyID = 'a0Z4L0000000o2CUAQ';\n"
                "FSL.OAAS oaas = new FSL.OAAS();\n"
                "id optRequest = oaas.optimize(oaasRequest);\n"
            ]
            f.writelines(endlines)
            self.apexfile = f.name

    def optimize(self):
        sfs = SFSManager()
        sfs.execute_apexfile(self.apexfile)
