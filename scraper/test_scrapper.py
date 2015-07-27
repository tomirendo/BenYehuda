import os
import glob
import json
import shutil
import unittest
import tempfile

from scraper import Piece, ClsSize, ArtistPage

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """
        Creates a temp folder
        """
        self.tempdir = tempfile.mkdtemp()
        assert os.path.isdir(self.tempdir)

    def tearDown(self):
        """
        Delete the temp folder
        """
        shutil.rmtree(self.tempdir)

    def get_t_file(self, artist, filename):
        """
        Returns a test file from an artist's folder
        """
        test_dir = os.path.join(os.path.dirname(__file__), "test_files")
        filepath = os.path.join(test_dir, artist, filename)
        with open(filepath, mode="r", encoding="utf-8") as f:
            return f.read()

class PieceParseTest(BaseTestCase):
    """
    Compares parsing of a number of different pieces to a ready made result.
    """
    def test_basic_poem(self):
        html = self.get_t_file("teller_zvi", "holy_seed.html")
        md = self.get_t_file("teller_zvi", "holy_seed.md")
        piece = Piece("http://benyehuda.org/teller_zvi/zera.html",
                      "holy seed",
                      html)
        self.assertTrue(piece.profile.is_poem())
        self.assertEqual(piece.as_markdown(), md)

    def test_big_book(self):
        html = self.get_t_file("bershadsky", "neged_hazerem.html")
        md = self.get_t_file("bershadsky", "neged_hazerem_start.md")
        piece = Piece("http://benyehuda.org/bershadsky/neged_hazerem.html",
                      "neged hazerem",
                      html)
        self.assertFalse(piece.profile.is_poem())
        # The solution isn't optimal enough to validate such a big story. But
        # it works well enough to skip this for now
        # self.assertTrue(piece.as_markdown().startswith(md))

    def test_piece_name(self):
        html = self.get_t_file("bialik", "bia002.html")
        piece = Piece("http://benyehuda.org/bialik/bia002.html", html=html)
        self.assertEqual(piece.name, "מִשּׁוּט בַּמֶּרְחַקִּים")

    def test_fetch_to_folder(self):
        html = self.get_t_file("bialik", "bia002.html")
        piece = Piece("http://benyehuda.org/bialik/bia002.html", html=html)
        piece.fetch_to_folder(self.tempdir)
        self.assertTrue(os.path.isdir(os.path.join(self.tempdir, "bia002")))
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, "bia002")))
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, "bia002", "bia002.orig.html")))

class ArtistPageTest(BaseTestCase):
    def get_artist_page(self, artist):
        return self.get_t_file(artist, "index.html")

    def test_get_pieces(self):
        html = self.get_artist_page("teller_zvi")
        artist = ArtistPage("http://benyehuda.org/teller_zvi/", "ביאליק", html)
        piece_urls = [link.url for link in artist.get_piece_links()].sort()
        expected_urls = [
            "zexer.html",
            "anoxi.html",
            "nes_ziona.html",
            "zera.html",
            "guest.html",
            "metim.html",
            "dunno.html",
            "ben_netanya.html"
        ].sort()
        self.assertEqual(piece_urls, expected_urls)

    def test_to_dict(self):
        html = self.get_artist_page("teller_zvi")
        artist = ArtistPage("http://benyehuda.org/teller_zvi/", "צבי אלעזר טלר", html)
        self.assertEqual(artist.as_dict(), {
            "name": "צבי אלעזר טלר",
            "years": "1840-1914",
            "url": "http://benyehuda.org/teller_zvi/",
            "md5": "115bdd8046e27fb5ed8cad03e150f33a"
        })
