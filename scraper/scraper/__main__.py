"""
Collect info from BenYehuda site
"""
import json
import argparse

from . import BenYehuda

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content", choices=["news", "pieces"])

    arguments = parser.parse_args()

    scraper = BenYehuda()
    data = []
    if arguments.content == "news":
        data = scraper.get_news()
    elif arguments.content == "pieces":
        data = scraper.get_pieces()

    print json.dumps(data)


if __name__ == '__main__':
    main()
