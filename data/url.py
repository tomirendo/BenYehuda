"""
A simple url object for elasticsearch url's
Python 3 only  
"""
from urllib.request import quote

class url(str):
    def add_path(self,addition):
        """
        Taking care of trailing '/' of the elastic url path
        """
        if self[-1] != '/':
            addition = '/' + addition
        return url(self + str(addition) + '/')

    def add_query(self,query):
        return url(self + '?q={}'.format(query))

    def to_url(self):
        begin,*end = self.split('?q=')
        end_str = quote('?q='.join(end))
        final = begin +'?q='+ end_str
        return final

index_url = url('http://localhost:9200/benyehuda/')
