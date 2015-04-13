import os
import glob
import json
import unittest

from scraper import Piece

class PieceParseTest(unittest.TestCase):
    """
    Compares parsing of a number of different pieces to a ready made result.
    The results are ordered in the following structure:

    test_files/
        <creator>/
            <piece>.html
            <piece>.json

    <piece>.json:
    {
        "url": "http://benyehuda.org/<creator>/<piece>.html",
        "name": "<piece-name>",
        "chapters": [
            {
                "index": <index-num>,
                "name": "<chapter-name>",
                "text": "<chapter-data>"
            }
        ]
    }
    """
    # maxDiff = None
    def test_piece_parsing(self):
        test_dir = os.path.join(os.path.dirname(__file__), "test_files")
        for piece_html in glob.iglob(os.path.join(test_dir, "*", "*.html")):
            html = open(piece_html, 'rb').read()
            piece_json = os.path.splitext(piece_html)[0] + ".json"
            with open(piece_json, 'r', encoding="utf-8") as f:
                details = json.load(f)
            p = Piece(name=details["name"], url=details["url"], html=html)
            self.assertEqual(p.as_dict(), details)



