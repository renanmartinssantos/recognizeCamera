import json 
from bson import json_util

class utils:
    def toJson(self, dbResult):
        details_dicts = [doc for doc in dbResult]
        details_json_string = json.dumps(details_dicts,default=json_util.default)
        return details_json_string