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

    It also removes paragraphs where the text is in <a> tags.
    """
    if not (tag.name == 'p' and tag.text):
        return False
    return not (tag.find_all('a'))

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
    def __init__(self, soup):
        """
        :param soup: The page data
        :type soup: BeautifulSoup
        """
        self._soup = soup
        self.class_count = self._get_class_count()
        self.class_sizes = self._get_class_sizes()
        self.total_words = sum(v["words"] for v in self.class_count.values())

        self.major_class = None
        self.minor_class = None
        self._set_major_minor()

    @staticmethod
    def _cls_sort_key(cls_details):
        """
        Sorting key used for class_count dictionary
        """
        return cls_details[1]["total"]

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
        class_sizes[tuple(first_p.get("class"))] = ClsSize.major_title
        # used to map the class_sizes len to the appropriate ClsSize
        len_to_size = {
            1: ClsSize.plain,
            2: ClsSize.chapter_title,
            3: ClsSize.subchapter_title,
            4: ClsSize.highlighted
        }

        # Sorts the classes by number of <p> tags - highest to lowest
        sorted_count = sorted(self.class_count.items(), key=self._cls_sort_key,
                              reverse=True)
        for cls_details in sorted_count:
            cls = cls_details[0]
            if cls in class_sizes:
                continue

            # Wordless are ignored
            if not cls_details[1]["words"]:
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
        for p in self._soup.find_all(text_p_filter):
            # We currently don't handle plain paragraphs
            if not p.get("class"):
                continue

            p_cls = tuple(p.get("class"))

            class_stats[p_cls]["total"] += 1
            class_stats[p_cls]["words"] += len(p.text.split())
        return class_stats

    def _set_major_minor(self):
        if not self.class_count:
            return

        # Sorts the classes by number of <p> tags
        sorted_count = sorted(self.class_count.items(), key=self._cls_sort_key)
        if len(sorted_count) > 2:
            self.major_class = sorted_count[-1]
            self.minor_class = sorted_count[-2]
        else:
            self.major_class = sorted_count[0]

    def get_class_value(self, name):
        """
        Returns the given CSS class name's relative value in the page acording.
        If the given class name is not recognized it's returned as 'plain'

        :param name: The elements classes
        :type name: tuple[str]
        :return: The class value acording to the ClsSize enum
        :rtype: int
        """
        return self.class_sizes.get(name, ClsSize.plain)

    def is_poem(self):
        """
        Figures out if the piece is a poem based on how many different classes
        it has. Basically if there's only the main title + plain text - it's a
        poem.
        """
        return len(self.class_sizes) <= 2


class Piece(object):
    """
    Holds the piece's name, url and chapters.
    """
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
        self.soup = BeautifulSoup(html)
        self.profile = PageProfile(self.soup)
        self.contents = self._scrape_contents()

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

    def _scrape_contents(self):
        """
        Goes over the <p> elemnts in the piece and creates a list of the
        contents in an internal format of a list of dicts. As json it will look
        like::

            [
                { "text": "The Never Ending Story", "type": 1 },
                { "text": "Chapter 1", "type": 2 },
                { "text": "The End", "type": 0 }
            ]

        The type of each element in the list is a reference to the ClsSize enum

        :return: The main contents of this piece
        :rtype: list[dict]
        """
        contents = []
        for tag in self.soup.find_all(text_p_filter):
            contents.append({
                "text": self.clean_text(tag),
                "type": self.profile.get_class_value(tuple(tag.get("class")))
            })
        return contents

    @staticmethod
    def markdown_map(item):
        """
        :param item: A single element from the internal contents
        :type item: dict
        :return: The item as a markdown string
        :rtype: str
        """
        if item["type"] == ClsSize.plain:
            return item["text"]

        if item["type"] == ClsSize.major_title:
            return "# " + item["text"]

        if item["type"] == ClsSize.chapter_title:
            return "## " + item["text"]

        if item["type"] == ClsSize.subchapter_title:
            return "### " + item["text"]

        if item["type"] == ClsSize.highlighted:
            return "*" + item["text"] + "*"

        # We shouldn't reach this but just in case
        return item["text"]

    @staticmethod
    def poem_markdown_map(item):
        """
        Converts markdown specifically for poems. Uses linebreaks instead of
        paragraphs for most situations

        :param item: A single element from the internal contents
        :type item: dict
        :return: The item as a markdown string
        :rtype: str
        """
        if item["type"] == ClsSize.plain:
            if item["text"]:
                # Two spaces to indicate newline in markdown
                return item["text"] + "  "
            return "\n"

        return Piece.markdown_map(item)

    @staticmethod
    def remove_last_empty_lines(lines):
        """
        :param lines: A list of text lines
        :type lines: list[str]
        :return: A list of lines were the last line has contents
        :rtype: list[str]
        """
        while lines and not lines[-1].split():
            lines.pop()
        return lines

    def as_markdown(self):
        """
        Converts the internal contents format to basic markdown language
        :return: The chapter as markdown
        :rtype: str
        """
        if self.profile.is_poem():
            lines = list(map(self.poem_markdown_map, self.contents))
            return "\n".join(self.remove_last_empty_lines(lines))
        # Two newlines are necessary for new paragraph in markdown
        return "\n\n".join(map(self.markdown_map, self.contents))

    def as_dict(self):
        """
        :return: The piece as an easily jsonable dict
        :rtype: dict[str]
        """
        return {
            "name": self.name,
            "url": self.url,
            "contents": self.contents
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
