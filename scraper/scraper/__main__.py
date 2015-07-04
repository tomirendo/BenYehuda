"""
Collects all the pieces from Ben Yehuda Project site and saves them in a
directory structure.
"""
import os
import sys
import time
import json
import logging
import argparse
import threading
import queue
from urllib import request
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from . import Piece, MainPage, ArtistPage

DONE = 1
artist_q = queue.Queue()

def fetch_artist(output_dir):
    """
    Reads artist links
    """
    link = artist_q.get()
    while link != DONE:
        log = logging.getLogger(urlparse(link.url).path[:-1])
        try:
            artist = ArtistPage(link.url, link.name)
            artist.fetch_to_folder(output_dir)
        except (KeyboardInterrupt, SystemExit):
            log.error("Got keyboard interrupt!")
            return
        except Exception as err:
            log.exception(err)
        finally:
            artist_q.task_done()
            link = artist_q.get()

def artist_a_filter(tag):
    """
    Finds all the links in a page that points to an artist's page on the site
    """
    if tag.name != 'a':
        return False

    href = tag.get('href').lower()
    if href.startswith('http'):
        return False

    if href.startswith('javascript'):
        return False

    # Artist pages are one branch below the main page and their links usually
    # end with / - Need to verify
    if href.count('/') == 1 and href[-1] == '/':
        return True

    return False

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-t", "--threads", type=int, default=5,
                        help="Number of threads to use")
    parser.add_argument("--url", default="http://benyehuda.org",
                        help="URL to Ben Yehuda Project site")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("output_dir", help="Where to save the pieces")

    arguments = parser.parse_args()
    log_fmt = "%(asctime)s\t%(levelname)s\t%(thread)s-%(name)s\t%(message)s"
    if arguments.verbose:
        logging.basicConfig(format=log_fmt, level=logging.DEBUG)
    else:
        logging.basicConfig(format=log_fmt, level=logging.INFO)

    logging.info("writing to folder: %s", arguments.output_dir)
    if os.path.exists(arguments.output_dir):
        parser.error("output folder: %s exists" % arguments.output_dir)
    os.mkdir(arguments.output_dir)

    logging.info("using %d threads", arguments.threads)
    for i in range(arguments.threads):
        thread = threading.Thread(
            target=fetch_artist,
            args=(arguments.output_dir,)
        )
        thread.daemon = True
        thread.start()

    main_page = MainPage(arguments.url)
    links = main_page.get_artist_links()
    logging.info("Started going over %d links", len(links))
    for link in links:
        artist_q.put(link)

    for i in range(arguments.threads):
        artist_q.put(DONE)

    # Allows exiting with Ctrl-C
    try:
        while not artist_q.empty():
            time.sleep(1)
    except KeyboardInterrupt:
        logging.error("Got keyboard interrupt!")
        sys.exit(1)

if __name__ == '__main__':
    main()
