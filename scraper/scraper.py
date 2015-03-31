import sys
import urllib3
import json
import os
from bs4 import BeautifulSoup

####################################################################
# A command line util to scrape Ben Yehuda content pages into JSON #
####################################################################


def benyehuda_scraper(url,creator,is_content_page):
    """
    :param url: a url string to a BY content page
    :param is_content_page: bool - True if this is a creator's map of links, False for content page
    :return: True on success, False on an error
    """

    if is_content_page:
        print("got {}, which is a {}".format(url, "content page" if is_content_page else "links page"))

    
    benyehuda_creators = []
    benyehuda_creators.append(url)
    
    parsed_dict = {}

    #TODO: initialize by reading the config file, not url, later, and extract all the creater pages into a URL list
    #For now, assume we have only one creator and one file

    try:

        http = urllib3.PoolManager()

        parsed_dict['creator']=creator
        chapters = []

        for i,item in enumerate(benyehuda_creators):

            
            lines = []

            r = http.request('GET', item)
            print("request for {} from author: {} returned code {}\n".format(item, creator,r.status))

            if r.status != 200:
                raise Exception("Status code: %s" % r.status_code)

            soup = BeautifulSoup(r.data)
            
            for link in soup.find_all("p", "a2"):
                    lines.append({"text_line":link.text})
                    #print("{}".format(link.text))

            chapter = {}
            chapter["chapter_index"]=(str)(i+1)
            chapter["full_text"]=lines

            chapters.append(chapter)

        parsed_dict['chapters']=chapters

        with open(_url_to_json_filename(benyehuda_creators[0]), 'w') as f:
            json.dump(parsed_dict,f)

        

    except Exception as e:
        print("ERROR: %s" % e)
        exit()

    with open(_url_to_json_filename(benyehuda_creators[0])) as g:
        a = json.load(g)
        print(a)

def _url_to_json_filename(url):
    return "{}.json".format(os.path.basename(url))



if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(
            "usage: scraper.py <path> <creator>\ncreates a JSON file represnting one, or more, BenYehuda Project Pieces\
            \nexample: python3 scraper.py http://benyehuda.org/bialik/bia001.html bialik")
        exit()

    benyehuda_scraper(sys.argv[1],sys.argv[2],True)
