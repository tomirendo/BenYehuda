from main import models
import urllib,json
from itertools import count

class url(str):
    def add_path(self,addition):
        if self[-1] != '/':
            addition = '/' + addition
        return url(self + str(addition) + '/')
    def to_url(self):
        return urllib.request.quote(self)

def encoded_json_for_object(obj):
    return obj.to_dict.encode('utf8')

index_url = url('http://localhost:9200/benyehuda/')

def send_collection(collection,object_name):
    url  = index_url.add_path(object_name)
    for obj,idx in zip(colleciton,count(1)):
        data = encoded_json_for_object(obj)
        req =  urllib.request.Request( url.add_path(count).to_url(),data,method='PUT')
        print(urllib.request.urlopen(req).read())

