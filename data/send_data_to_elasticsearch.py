from main import models
import urllib
import json
from itertools import count
url = 'http://localhost:9200/benyehuda/piece/'
for piece,idx in zip(models.Piece.objects.all(),count(1)):
    data = json.dumps(piece.to_dict()).encode('utf8') 
    print(data)
    req = urllib.request.Request(url +str(idx)+'/',data,method='PUT')
    print(urllib.request.urlopen(req).read())

