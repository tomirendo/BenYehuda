from data.url import url,index_url
import urllib,json

def query_url(obj_type,query):
    return index_url.add_path(obj_type).add_query(query)

def query(url):
    result = json.reads(urllib.request.urlopen(url.to_url()).read())

nitshe = b'\xd7\xa0\xd7\x99\xd7\x98\xd7\xa9\xd7\x94'.decode('utf8')
print(query(query_url('creator',nitshe)))

