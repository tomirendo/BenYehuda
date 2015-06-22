from main import models
import urllib,json
from itertools import count
from data.url import url,index_url

def encoded_json_for_object(obj):
    return json.dumps(obj.to_dict()).encode('utf8')

def send_collection(collection,object_name):
    url  = index_url.add_path(object_name)
    for obj,idx in zip(collection,count(1)):
        data = encoded_json_for_object(obj)
        req =  urllib.request.Request( url.add_path(idx).to_url(),data,method='PUT')
        print(urllib.request.urlopen(req).read())

def collection_from_model(model):
    return model.objects.all()
if __name__ == '__main__':
    send_collection(collection_from_model(models.Creator),'creator')
    send_collection(collection_from_model(models.Piece),'piece')
