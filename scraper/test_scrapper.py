"""
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

import unittest

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
    def test_
        pass



