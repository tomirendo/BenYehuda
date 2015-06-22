from urllib.request import quote

class url(str):
    def add_path(self,addition):
        """
            Taking care of trailing '/' of the elastic url path
        """
        if self[-1] != '/':
            addition = '/' + addition
        return url(self + str(addition) + '/')

    def add_query(query):
        return url(self + '?q={}'.format(query))

    def to_url(self):
        """
            Quotes url in the RIGHT WAY!
        """
        begin,*end = self.split('?')
        end_str = '?'.join(urllib.request.quote(p) for p in end)
        final = begin +'?'+ end_str
        return final

index_url = url('http://localhost:9200/benyehuda/')
