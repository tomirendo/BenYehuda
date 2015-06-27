import os
import json
from urllib import request
from urllib import parse as urlparse

from bs4 import BeautifulSoup

from helpers import NamedLink

class ArtistPage(object):
    """
    Handles parsing and fetching of an artist page
    """
    def __init__(self, url, name):
        # log using the artists' page name
        self.page_name = urlparse.urlparse(url).path[:-1]
        self.log = logging.getLogger(page_name)
        self.url = url
        self.name = name

    def get_piece_links(self):
        """
        Finds all the links to pieces in the given page
        :return: Set of the piece links
        :rtype: set[NamedLink]
        """
        soup = BeautifulSoup(request.urlopen(self.url))
        piece_links = set()
        for anchor in soup.find_all("a"):
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
        self.log.debug("Found %d pieces", len(piece_links))
        return piece_links

    def fetch_to_folder(self, main_folder):
        """
        Downloads, parses and saves all the pieces from the given artist
        """
        artist_dir = os.path.join(main_folder, self.page_name)
        os.mkdir(artist_dir)
        # Create JSON file with basic details about the artist
        with open(os.path.join(artist_dir, 'artist.json'), 'w',
                  encoding='utf-8') as details_f:
            json.dump({ "name": self.name, "url": self.url }, details_f,
                      ensure_ascii=False, indent=4)

        piece_links = self.get_piece_links()




def fetch_artist(output_dir):
    """
    Reads artist links
    """
    link = artist_q.get()
    while link != DONE:
        href = link.url
        # We use the artist page name to make the logs easier
        log = logging.getLogger(link.get_path()[:-1])
        try:
            log.debug("Started fetching artist")
            name = link.name
            artist_dir = os.path.join(output_dir, link.get_path())
            os.mkdir(artist_dir)
            with open(os.path.join(artist_dir, 'artist.json'), 'w',
                      encoding="utf-8") as f:
                json.dump({ "name": name, "url": link.url }, f,
                          ensure_ascii=False, indent=4)
            soup = BeautifulSoup(request.urlopen(link.url))
            piece_links = []
            for anchor in soup.find_all("a"):
                href = urlparse(anchor.get('href')).path
                if not href:
                    continue

                if href in piece_links:
                    continue

                if '/' in href:
                    continue

                if "@" in href:
                    continue

                piece_links.append(href)

            log.debug("found %d pieces", len(piece_links))
            for piece_url in piece_links:
                piece_name = os.path.splitext(piece_url)[0]
                piece_folder = os.path.join(artist_dir, piece_name)
                log.debug("Creating folder for piece: %s", piece_folder)
                os.mkdir(piece_folder)
                piece_url = link.url + piece_url
                log.debug("Getting piece: %s", piece_url)
                try:
                    piece = Piece(piece_url)
                except URLError as err:
                    log.error("Got url-error on piece: %s", piece_name)
                    log.exception(err)
                    continue
                with open(os.path.join(piece_folder, piece_name + ".md"), 'w',
                          encoding="utf-8") as f:
                    f.write(piece.as_markdown())

                with open(os.path.join(piece_folder, piece_name + ".json"), 'w',
                          encoding="utf-8") as f:
                    json.dump(piece.as_dict(), f, ensure_ascii=False, indent=4)

            log.info("Finished fetching artist")
        except (KeyboardInterrupt, SystemExit):
            log.error("Got keyboard interrupt!")
            return
        except Exception as err:
            log.exception(err)
        finally:
            artist_q.task_done()
            link = artist_q.get()
