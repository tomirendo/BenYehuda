import os
import json
from enum import Enum
from urllib import request
from collections import Counter, defaultdict

from bs4 import BeautifulSoup

def text_p_filter(tag):
    """
    Filter used with BeautifulSoup's find method to get all the paragraphs with
    text in them:

    >>> soup = BeautifulSoup('<p></p><p><span>Hello1</span></p>')
    >>> soup.find(text_p_filter)
    <p><span>Hello1</span></p>
    """
    return tag.name == 'p' and tag.text

class ClsSize(Enum):
    """
    Enum for the different class sizes for easy understanding
    """
    plain = 0
    major_title = 1
    chapter_title = 2
    subchapter_title = 3
    highlighted = 4


def _get_curdir_json(filename):
    """
    :param filename: Name of json file to return (.json suffix not assumed)
    :type filename: str
    :return: Parsed json file from the current directory
    :rtype: object
    """
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, 'r') as json_file:
        return json.load(json_file)


class PageProfile(object):
    """
    Collects basic statistics about text, paragraphs and CSS classes in a given
    html page
    """
    # Sorting key used for class_count dictionary
    CLS_SORT_KEY = lambda x: x[1]["total"]

    def __init__(self, soup):
        """
        :param soup: The page data
        :type soup: BeautifulSoup
        """
        self._soup = soup
        self.class_count = self._get_class_count()
        self.class_sizes = self._get_class_sizes()

        self.major_class = None
        self.minor_class = None
        self._set_major_minor()

    def _get_class_sizes(self):
        """
        Goes over the document and calculates the class sizes based on the
        following assumptions (rules are organized by priority):
        1. The first <p> class is the Piece's title
        2. The most common class is the plain text
        3. The second most common is the chapter titles
        4. Third most common is the subchapter titles
        5. Fourth most common is highlited text

        The sizes are mapped to `self._class_sizes`
        """
        class_sizes = {}
        first_p = self._soup.find(text_p_filter)
        class_sizes[tupe(first_p.get("class"))] = ClsSize.major_title
        # used to map the class_sizes len to the appropriate ClsSize
        len_to_size = {
            1: ClsSize.plain,
            2: ClsSize.chapter_title,
            3: ClsSize.subchapter_title,
            4: ClsSize.highlighted
        }

        # Sorts the classes by number of <p> tags - highest to lowest
        sorted_count = sorted(self.class_count.items(), key=self.CLS_SORT_KEY)
        for cls in sorted_count:
            if cls in class_sizes:
                continue

            cls_size_len = len(class_sizes)
            if cls_size_len in len_to_size:
                class_sizes[cls] = len_to_size[cls_size_len]
            else:
                # We already found all the major classes
                break

        return class_sizes

    def _get_class_count(self):
        """
        Goes over the paragraphs in the page and creates basic statistics about
        their classes. For each CSS class for <p> elements there's an object
        with the number of paragraph and number of words in all paragraphs.

        Output dict looks like:
        {
            ("a2",) : {
                "total": 34,
                "words": 40
            },
            ("a3",) : {
                "total": 400,
                "words": 5000
            }
        }

        :return: A dict of class and details
        :rtype: dict
        """
        class_stats = defaultdict(Counter)
        for p in self._soup.find_all("p"):
            # We currently don't handle plain paragraphs
            if not p.get("class"):
                continue
            p_cls = tuple(p.get("class"))

            class_stats[p_cls]["total"] += 1
            class_stats[p_cls]["words"] += len(p.text.split())
        return class_stats

    def _set_major_minor(self):
        class_count = self._get_class_count()
        if not class_count:
            return

        # Sorts the classes by number of <p> tags
        sorted_count = sorted(class_count.items(), key=lambda x: x[1]['total'])
        if len(sorted_count) > 2:
            self.major_class = sorted_count[-1]
            self.minor_class = sorted_count[-2]
        else:
            self.major_class = sorted_count[0]

    def get_class_value(self, name):
        """
        Returns the given CSS class name's relative value in the page acording.
        If the given class name is not recognized it's returned as 'plain'

        :param name: The class name
        :type name: str
        :return: The class value acording to the ClsSize enum
        :rtype: int
        """
        return self._class_sizes.get(name, ClsSize.plain)


class Piece(object):
    """
    Holds the piece's name, url and chapters.
    """
    KNOWN_URLS = _get_curdir_json("known_urls.json")

    def __init__(self, name, url, html=None):
        """
        :param name: Piece name
        :type name: str
        :param url: Piece url
        :type url: str
        :param html: Page raw html
        :type html: bytes
        """
        self.name = name
        self.url = url
        if html is None:
            html = request.urlopen(url).read()
        self._soup = BeautifulSoup(html)
        self.chapters = self.scrape_chapters()


    def scrape_chapters(self):
        """
        Creates the chapters from the page's html.
        Decideds which scraping function to use based on an "algorithm".

        :return: List of chapters (each chapter is a simple dict)
        :rtype: list[dict]
        """
        # Things we already know how to parse
        if self.url in self.KNOWN_URLS:
            func_name = "scrape_" + self.KNOWN_URLS[self.url]
            return getattr(self, func_name)()

        stats = PageProfile(self._soup)

        if stats.minor_class:
            return self.scrape_minor(stats.minor_class)

        if len(self._soup.find_all("p", "a1")) == 0:
            return self.scrape_text_from_p2_a2()
        return self.scrape_chapter_from_a1_text_from_p()

    @staticmethod
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

    def scrape_minor(self, minor):
        """
        Uses the given class to divide the paragraphs in the page to chapters
        and main text
        :param minor: The second most common class in the page
        :type minor: tuple[str]
        """
        chapters = []
        chapter = None
        for p in self._soup.find_all("p"):
            if tuple(p.get("class")) == minor:
                if chapter and not chapter["text"]:
                    chapter["name"].append(self.clean_text(p))
                else:
                    chapter = {
                        "name": [self.clean_text(p)],
                        "index": len(chapters),
                        "text": []
                    }
                    chapters.append(chapter)
                    continue

            if chapter is None:
                continue

            chapter["text"].append(p.text)

        fixed_chapters = []
        for chapter in chapters:
            if not chapter["text"]:
                continue
            chapter["index"] = len(fixed_chapters)
            chapter["text"] = "\n".join(chapter["text"])
            fixed_chapters.append(chapter)

        return fixed_chapters

    def scrape_text_from_p2_a2(self):
        """
        Only one chapter.
        Chapter text is <p class="a2">
        """
        return [{
            "name": "",
            "index": 0,
            "text": "\n".join((self.clean_text(e) for e in self._soup.find_all("p", "a2"))),
        }]

    def scrape_chapter_from_a1_text_from_p(self):
        """
        Chapters are marked with <p class="a1">
        Chapter text are just <p> after the chapter name
        """
        chapters = []
        chapter = None
        for p in self._soup.find_all("p"):
            if p.get("class") == ["a1"]:
                chapter = {
                    "name": self.clean_text(p),
                    "index": len(chapters),
                    "text": [],
                }
                chapters.append(chapter)
                continue

            if chapter is None:
                continue

            chapter["text"].append(p.text)

        fixed_chapters = []
        for chapter in chapters:
            if not chapter["text"]:
                continue
            chapter["index"] = len(fixed_chapters)
            chapter["text"] = "\n".join(chapter["text"])
            fixed_chapters.append(chapter)

        return fixed_chapters


    def as_dict(self):
        """
        :return: The piece as an easily jsonable dict
        :rtype: dict
        """
        return {
            "name": self.name,
            "url": self.url,
            "chapters": self.chapters
        }


class Creator(object):
    """
    Holds the creator's name and url
    """
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def get_pieces(self):
        raise NotImplementedError()

class BenYehuda(object):
    """
    Main class for the BenYehuda project scraper
    """
    def get_news(self):
        return []

    def get_pieces(self):
        return []

    def get_creators(self):
        """
        :return: A list of all the site's creators
        :rtype: list[Creator]
        """
        raise NotImplementedError()
