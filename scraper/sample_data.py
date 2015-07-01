import os
import json 

from scraper import Creator
creator = Creator('חיים נחמן ביאליק','http://benyehuda.org/bialik/',verbos = True)

def hebrew_to_english(text):
    translate = {chr(ord('א')+heb):eng for heb,eng in zip(range(27),"abgdhwzhtycclmmnns@ppzzkkrst")}
    return "".join(translate[i] for i in text if i in translate)

sample_dir = 'sample'
def write_creator_files(creator):
    os.mkdir(os.path.join(sample_dir,hebrew_to_english(creator.name)))
    for piece in creator.pieces:
        with open(os.path.join(sample_dir,hebrew_to_english(creator.name),hebrew_to_english(piece.name),'.json'),"rb") as f:
            f.write(json.dumps(piece.as_dict()))
