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
<<<<<<< HEAD
        """
            Quotes url in the RIGHT WAY!
        """
        begin,*end = self.split('?')
        end_str = '?'.join(quote(p) for p in end)
        final = begin +'?'+ end_str
=======
        begin,*end = self.split('?q=')
        end_str = quote('?q='.join(end))
        final = begin +'?q='+ end_str
>>>>>>> ea0a983c8129d48e794575ee92b3e573c0138a88
        return final

index_url = url('http://localhost:9200/benyehuda/')
