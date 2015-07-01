import os
import json 

from scraper import Creator

creator = Creator('חיים נחמן ביאליק','http://benyehuda.org/bialik/',verbos = True)

def write_creator_files(creator):
    os.mkdir(creator.name)
    for piece in creator.pieces:
        with open(os.path.join(creator.name,piece.name,'.json'),"rb") as f:
            f.write(json.dumps(piece.as_dict()))
