from data.url import url,index_url
import urllib,json

def query_url(obj_type,query):
    return index_url.add_path(obj_type).add_query(query)

def send_query(url):
    result = json.reads(urllib.request.urlopen(url.to_url()).read())
