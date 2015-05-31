"""
Collects all the pieces from Ben Yehuda Project site and saves them in a
directory structure.
"""
import os
import sys
import time
import logging
import argparse
import threading
import queue
from urllib import request

from bs4 import BeautifulSoup

DONE = 1
artist_q = queue.Queue()

def fetch_artist(output_dir, main_url):
    link = artist_q.get()
    while link != DONE:
        href = link.get('href').lower()
        full_link = main_url + "/" + href
        log = logging.getLogger(href[:-1])
        log.debug("Started fetching artist")
        name = link.text
        artist_dir = os.path.join(output_dir, href)
        soup = BeautifulSoup(request.url_open(full_link))

        log.debug("Finished fetching artist")
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
    if arguments.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.info("using %d threads", arguments.threads)
    for i in range(arguments.threads):
        t = threading.Thread(
            target=fetch_artist,
            args=(arguments.output_dir, arguments.url)
        )
        t.daemon = True
        t.start()

    main_soup = BeautifulSoup(request.urlopen(arguments.url))
    links = main_soup.find_all(artist_a_filter)
    link_urls = []
    clean_links = []
    for link in links:
        if link.get('href') in link_urls:
            continue
        clean_links.append(link)
        link_urls.append(link.get('href'))


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
