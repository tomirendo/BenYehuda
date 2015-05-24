import os
import glob
import json
import unittest

from scraper import Piece

class PieceParseTest(unittest.TestCase):
    """
    Compares parsing of a number of different pieces to a ready made result.
    """
    def get_t_file(self, artist, filename):
        test_dir = os.path.join(os.path.dirname(__file__), "test_files")
        filepath = os.path.join(test_dir, artist, filename)
        with open(filepath, mode='r', encoding='utf-8') as f:
            return f.read()

    def test_basic_poem(self):
        html = self.get_t_file("teller_zvi", "holy_seed.html")
        md = self.get_t_file("teller_zvi", "holy_seed.md")
        piece = Piece("holy seed",
                      "http://benyehuda.org/teller_zvi/zera.html",
                      html)
        self.assertEqual(piece.as_markdown(), md)


    # # maxDiff = None
    # def test_piece_parsing(self):
    #     for piece_html in glob.iglob(os.path.join(test_dir, "*", "*.html")):
    #         html = open(piece_html, 'r').read()
    #         piece_json = os.path.splitext(piece_html)[0] + ".json"
    #         with open(piece_json, 'r', encoding="utf-8") as f:
    #             details = json.load(f)
    #         p = Piece(name=details["name"], url=details["url"], html=html)
    #         self.assertEqual(p.as_dict(), details)



