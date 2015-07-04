"""
Set of helper classes and methods for the scraper
"""
from urllib import parse as urlparse

def clean_text(element):
    """
    Removes whitespace from an element's text. Linebreaks and other
    whitespaces inside a single tag are meaningless. IE:

    >>> e = BeautifulSoup('''
    ... <p>This whole thing
    ... is just one line.       No need
    ... for breaks!!!
    ... </p>
    ... ''')
    >>> Piece.clean_text(e)
    'This whole thing is just one line No need for breaks!!!'

    :param element: An html element
    :type element: bs4.element
    """
    return " ".join(element.text.split())

class NamedLink(object):
    """
    Holds a url with an additional name attribute. Used when scraping all the
    urls from the main page into a single set of urls.
    """
    def __init__(self, url, name):
        self.url = url
        self.name = name

    def get_path(self):
        """
        Helper function to get the path part of the url (also removes the root
        slash)
        """
        return urlparse.urlparse(self.url).path[1:]

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other):
        """
        We only care about the urls - first name that comes up - wins!
        """
        if isinstance(other, NamedLink):
            return self.url == other.url
        return False
