from sfsConnect import sf_api_call
from const import COMPOSITE, QUERY_URL, EXECUTE_ANONYMOUS

class SFSManager:
    def __init__(self) -> None:
        pass

    def get_query(self, query):
        r = sf_api_call(QUERY_URL, method='get', parameters={'q': query})
        return r

    def create_one(self, URL, data):
        r = sf_api_call(URL, method='post', data=data)
        return r

    def create_many(self, data):
        r = sf_api_call(COMPOSITE, method='post', data=data)
        return r
        
    def update_one(self, URL, id, data):
        r = sf_api_call(URL + "/" + id, method='patch', data=data)
        return r

    def update_many(self, data):
        r = sf_api_call(COMPOSITE + "/sobjects", method='patch', data=data)
        return r

    def get(self, URL, id):
        r = sf_api_call(URL + "/" + id, method='get')
        return r
    
    def get_all(self, URL):
        r = sf_api_call(URL, method='get')
        return r

    def delete_one(self, URL, id):
        r = sf_api_call(URL + "/" + id, method='delete')
        return r

    def delete_many(self, params):
        # params = {"ids": "0Hu4L000000TfNFSA0,0Hu4L000000TgawSAC"}
        r = sf_api_call(COMPOSITE + "/sobjects", method='delete', parameters=params)
        return r

    def execute_apexfile(self, apexfile):
        with open(apexfile) as f:
            body = f.read()
        r = sf_api_call(EXECUTE_ANONYMOUS, method="get", parameters={'anonymousBody': body})
        return r

