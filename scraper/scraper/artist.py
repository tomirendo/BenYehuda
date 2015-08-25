"""
Class for parsing an artist page
"""
import os
import re
import json
import logging
from hashlib import md5
from urllib import request
from urllib.parse import urlparse, urljoin
from urllib.error import URLError


from bs4 import BeautifulSoup

from . import Piece
from .helpers import NamedLink

class ArtistPage(object):
    """
    Handles parsing and fetching of an artist page
    """
    YEARS_RE = re.compile("\((\d+).(\d+)\)")

    def __init__(self, url, name, html=None):
        # log using the artists' page name but remove the trailing `/`
        self.page_name = os.path.basename(urlparse(url).path[:-1])
        self.log = logging.getLogger(self.page_name)
        self.url = url
        self.name = name
        if html is None:
            html = request.urlopen(self.url)
        self.soup = BeautifulSoup(html)
        # hash is done after soup so it will be different from the raw page
        self.md5 = md5(self.soup.encode()).hexdigest()

    def get_years(self):
        """
        @return: The artist's years as string of "birth-death". If the year is
                 not available - returns an empty string.
        @rtype: str
        """
        years_text = self.soup.find(text=self.YEARS_RE)
        if not years_text:
            return None
        # Convert the two years to ints and sorts them from small to large
        year1, year2 = sorted(map(int, self.YEARS_RE.findall(years_text)[0]))
        return "{}-{}".format(year1, year2)

    def get_piece_links(self):
        """
        Finds all the links to pieces in the given page
        :return: Set of the piece links
        :rtype: set[NamedLink]
        """
        piece_links = set()
        for anchor in self.soup.find_all("a"):
            href = urlparse(anchor.get("href")).path
            if not href:
                continue

            if href in piece_links:
                continue

            if "/" in href:
                continue

            if "@" in href:
                continue

            piece_links.add(NamedLink(href, anchor.text))
        self.log.debug("Found {}%d pieces", len(piece_links))
        return piece_links

    def as_dict(self):
        """
        :return: The artist as an easy to json dict
        :rtype: dict
        """
        #TODO: Add copyright parsing - example page: http://benyehuda.org/cohen_yisrael/
        return {
            "name": self.name,
            "url": self.url,
            "md5": self.md5,
            "years": self.get_years()
        }

    def fetch_to_folder(self, main_folder):
        """
        Downloads, parses and saves all the pieces from the given artist
        :param main_folder: The parent dir in which we'll place a directory with
                            the artist's name
        :type main_folder: str
        """
        artist_dir = os.path.join(main_folder, self.page_name)
        self.log.info("Fetching artist details to: %s", artist_dir)
        os.mkdir(artist_dir)
        # Create JSON file with basic details about the artist
        with open(os.path.join(artist_dir, 'artist.json'), 'w',
                  encoding='utf-8') as details_f:
            json.dump(self.as_dict(), details_f, ensure_ascii=False, indent=4)

        piece_links = self.get_piece_links()
        for link in piece_links:
            try:
                piece = Piece(urljoin(self.url, link.url))
            except URLError as err:
                self.log.error("Got url-error on piece: %s", link.name)
                self.log.exception(err)
                continue

            piece.fetch_to_folder(artist_dir)
        self.log.info("Finished fetching artist")
