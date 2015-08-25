from django.shortcuts import render
from django.http import HttpResponse
from .models import Piece
from urllib.request import urlopen
from urllib.parse import quote 

# Create your views here.
def download(request,id):
    p = Piece.objects.get(id = id)
    response = HttpResponse()
    response = HttpResponse(content_type='text/rtf')
    response['Content-Disposition'] = 'attachment; filename="{}.rtf"'.format(p.name.encode("utf8"))
    create_rtf_file(response,dictionary_from_piece(p))
    return response
def create_rtf_file(file_stream, piece):
    """
        Writes an rtf file into the file stream,
        from a piece dictionary:
            piece = {
                'name' : piece_name,
                'parts' :[
                    {
                        'name' : part_name,
                        'text' : part_text
                    },...
                ]
            }
    """
    import PyRTF
    import rtfunicode
    doc = PyRTF.Document(default_language = PyRTF.Languages.Hebrew)
    #Writing The book name:
    par = PyRTF.Paragraph(PyRTF.ParagraphPropertySet(alignment=2))
    par.append(piece["name"].encode('rtfunicode'))
    section = PyRTF.Section()
    section.append(par)
    doc.Sections.append(section)

    for part in piece["parts"]:
        par = PyRTF.Paragraph(PyRTF.ParagraphPropertySet(alignment=2))
        par.append((part["name"] + "\n"*2).encode('rtfunicode'))
        par.append((part["text"] + "\n"*2).encode('rtfunicode'))
        section = PyRTF.Section()
        section.append(par)
        doc.Sections.append(section)

    PyRTF.Renderer().Write(doc,file_stream)

def dictionary_from_piece(piece):
     return {
                 'name' : piece.name,
                 'parts' : [ { "name" : j.name, "text" : j.text } for j in
                           sorted(piece.chapters.all(),key = lambda x:x.index)]
               }
