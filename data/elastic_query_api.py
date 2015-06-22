from url import url,index_url
import urllib,json

def query_url(obj_type,query):
    search_url = '_search'
    return index_url.add_path(obj_type).add_path(search_url).add_query(query)

def query(url):
    return json.loads(urllib.request.urlopen(url.to_url()).read().decode("utf8"))
    
if __name__ == '__main__':
    nitshe = b'\xd7\xa0\xd7\x99\xd7\x98\xd7\xa9\xd7\x94'.decode('utf8')
    search_url = query_url('creator',nitshe)
    print(search_url.to_url())

