from bs4 import BeautifulSoup
from urllib import request

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
        self._soup = BeautifulSoup(html)
        self.chapters = self.scrape_chapters()

    def scrape_chapters(self):
        """
        Creates the chapters from the page's html
        """
        chapters = []
        chapter = None
        for p in self._soup.find_all("p"):
            if p.get("class") == ["a1"]:
                chapter = {
                    "name": p.text,
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
        self.name = nane
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
