class Chapter(object):
    """
    Chapters in a piece. The main text lives here
    """
    def __init__(self, name, index, data):
        self.name = name
        self.index = index
        self.data = data


class Piece(object):
    """
    Holds the piece's name, url and chapters
    """
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.chapters = []
        self.scrape()

    def scrape(self):
        """
        Loads the page and gets the chapters
        """


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
