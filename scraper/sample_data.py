import os
import json 

from scraper import Creator
creator = Creator('חיים נחמן ביאליק','http://benyehuda.org/bialik/',verbos = True)

def hebrew_to_english(text):
    translate = {chr(ord('א')+heb):eng for heb,eng in zip(range(27),"abgdhwzhtycclmmnnseppzzkkrst")} 
    translate[' '] = '-'
    return "".join(translate[i] for i in text if i in translate)

sample_dir = 'samples'

def write_creator_files(creator):
    try :
        os.mkdir(sample_dir)
    except:
        pass
    try:
        os.mkdir(os.path.join(sample_dir,hebrew_to_english(creator.name)))
    except :
        pass
    for piece in creator.pieces:
        with open(os.path.join(sample_dir,hebrew_to_english(creator.name),hebrew_to_english(piece.name)+'.json'),"wb") as f:
            f.write(json.dumps(piece.as_dict()).encode('utf8'))

write_creator_files(creator)
