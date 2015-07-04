"""
Class for parsing the main Ben Yehuda site page
"""
from urllib import request
from urllib import parse as urlparse

from bs4 import BeautifulSoup

from .helpers import NamedLink, clean_text

class MainPage(object):
    """
    Parses and gets information from the main index page. Mostly used to get
    links for all of the artist pages
    """
    def __init__(self, url="http://benyehuda.org"):
        self.main_url = url
        self.soup = BeautifulSoup(request.urlopen(url))

    @staticmethod
    def artist_a_filter(tag):
        """
        Finds all the links in the index page that points to an artist's page
        """
        if tag.name != "a":
            return False

        href = tag.get("href").lower()
        # Artist links are supposed to be internal
        if href.startswith("http"):
            return False

        # Remove unrelated crap
        if href.startswith("javascript"):
            return False

        # Artist pages are one branch below the main page and their links
        # usually end with / - Need to verify
        if href.count("/") == 1 and href[-1] == "/":
            return True

        return False

    def get_artist_links(self):
        """
        :return: A set of unique artist page urls and names
        :rtype: set[NamedLink]
        """
        anchors = self.soup.find_all(self.artist_a_filter)
        links = set()
        for anchor in anchors:
            url = urlparse.urljoin(self.main_url, anchor.get("href").lower())
            links.add(NamedLink(url, clean_text(anchor)))
        return links
