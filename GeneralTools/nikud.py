#!/usr/bin/python

def remove_nikud(txt,encoding="utf8"):
    """
        Removes nikud from a text
        Returns the texts in the given encoding. 
        If txt is unicode -> returns unicode object. 
        Python2\3 compatible
    """
    alef = 1488 
    min_nikud = 1416 
    max_nikud = 1479
    
    try :
        nikud_chars = [unichr(i) for i in range(min_nikud,alef)]
        test_for = str
    except NameError :#Python3
        nikud_chars = [chr(i) for i in range(min_nikud,alef)]
        test_for = bytes
        
    if not isinstance(txt,test_for):
        was_unicode = True
        unicode_txt = txt
    else :
        was_unicode = False
        unicode_txt = txt.decode(encoding)
    
    for char in nikud_chars:
        unicode_txt = unicode_txt.replace(char,u"")
    
    if not was_unicode:
        return unicode_txt.encode(encoding)
    else :
        return unicode_txt
