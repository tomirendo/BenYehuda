import os
import json 

from scraper import Creator
creator = Creator('חיים נחמן ביאליק','http://benyehuda.org/bialik/',verbos = True)

def hebrew_to_english(text):
    translate =  {'ת': 's', 't': 't', 'כ': 'c', 'y': 'y', 'l': 'l', 'c': 'c', 'א': 'a', 'a': 'a', 'מ': 'm', 'ן': 'n', 'q': 'q', 'ר': 'k', 'ד': 'd', 'פ': 'p', 'u': 'u', 'ב': 'b', 'י': 'y', 'h': 'h', 'ס': 's', 'k': 'k', 'w': 'w', 'd': 'd', 'צ': 'z', 'e': 'e', 'ל': 'l', 'm': 'm', 'b': 'b', 'ז': 'z', 'ג': 'g', 'ע': 'e', 'ח': 'h', 'i': 'i', 'ק': 'k', 'n': 'n', 'ט': 't', 'ם': 'm', 's': 's', 'ש': 'r', 'r': 'r', 'z': 'z', 'ף': 'p', 'ה': 'h', 'v': 'v', ' ': ' ', 'x': 'x', 'o': 'o', 'j': 'j', 'p': 'p', 'f': 'f', 'ו': 'w', 'נ': 'n', 'ך': 'c', 'ץ': 'z', 'g': 'g'}
    return "".join(translate.get(i,'') for i in text)

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
