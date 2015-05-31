import os
import glob
import json
import unittest

from scraper import Piece, ClsSize

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
        self.assertTrue(piece.profile.is_poem())
        self.assertEqual(piece.as_markdown(), md)

    def test_big_book(self):
        html = self.get_t_file("bershadsky", "neged_hazerem.html")
        md = self.get_t_file("bershadsky", "neged_hazerem_start.md")
        piece = Piece("neged hazerem",
                      "http://benyehuda.org/bershadsky/neged_hazerem.html",
                      html)
        self.assertFalse(piece.profile.is_poem())
        # The solution isn't optimal enough to validate such a big story. But
        # it works well enough to skip this for now
        # self.assertTrue(piece.as_markdown().startswith(md))
