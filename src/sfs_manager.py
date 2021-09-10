from sfsConnect import sf_api_call
from const import COMPOSITE

class SFSManager:
    def __init__(self, URL) -> None:
        self.URL = URL

    def create_one(self, data):
        r = sf_api_call(self.URL, method='post', data=data)
        return r

    def create_many(self, data):
        r = sf_api_call(COMPOSITE, method='post', data=data)
        return r
        
    def update_one(self, id, data):
        r = sf_api_call(self.URL + "/" + id, method='patch', data=data)
        return r

    def get(self, id):
        r = sf_api_call(self.URL + "/" + id, method='get')
        return r
    
    def get_all(self):
        r = sf_api_call(self.URL, method='get')
        return r

    def delete_one(self, id):
        r = sf_api_call(self.URL + "/" + id, method='delete')
        return r

    def delete_many(self, params):
        r = sf_api_call(COMPOSITE + "/sobjects", method='delete', parameters=params)
        return r