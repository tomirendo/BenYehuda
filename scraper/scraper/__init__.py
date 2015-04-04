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
        Creates the chapters from the page's html.
        Decideds which scraping function to use based on an "algorithm".

        :return: List of chapters (each chapter is a simple dict)
        :rtype: list[dict]
        """
        if len(self._soup.find_all("p", "a1")) == 0:
            return self._scrape_t_p_a2()
        return self._scrape_ch_a1_t_p()

    def _scrape_t_p_a2(self):
        """
        Only one chapter.
        Chapter text is <p class="a2">
        """
        return [{
            "name": "",
            "index": 0,
            "text": "\n".join((e.text for e in self._soup.find_all("p", "a2"))),
        }]

    def _scrape_ch_a1_t_p(self):
        """
        Chapters are marked with <p class="a1">
        Chapter text are just <p> after the chapter name
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
