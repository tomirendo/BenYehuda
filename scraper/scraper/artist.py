import os
import json
import logging
from urllib import request
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from . import Piece
from .helpers import NamedLink

class ArtistPage(object):
    """
    Handles parsing and fetching of an artist page
    """
    def __init__(self, url, name, html=None):
        # log using the artists' page name but remove the trailing `/`
        self.page_name = urlparse(url).path[:-1]
        self.log = logging.getLogger(self.page_name)
        self.url = url
        self.name = name
        if html is None:
            html = request.urlopen(self.url)
        self.soup = BeautifulSoup(html)

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

    def fetch_to_folder(self, main_folder):
        """
        Downloads, parses and saves all the pieces from the given artist
        """
        artist_dir = os.path.join(main_folder, self.page_name)
        self.log.info("Fetching artist details to: %s", artist_dir)
        os.mkdir(artist_dir)
        # Create JSON file with basic details about the artist
        with open(os.path.join(artist_dir, 'artist.json'), 'w',
                  encoding='utf-8') as details_f:
            json.dump({ "name": self.name, "url": self.url }, details_f,
                      ensure_ascii=False, indent=4)

        piece_links = self.get_piece_links()
        for link in piece_links:
            try:
                piece = Piece(piece_url)
            except URLError as err:
                log.error("Got url-error on piece: %s", piece_name)
                log.exception(err)
                continue

            piece.fetch_to_folder(artist_dir)
        self.log.info("Finished fetching artist")
