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
    par.append(piece["name"].decode("utf8").encode('rtfunicode'))
    section = PyRTF.Section()
    section.append(par)
    doc.Sections.append(section)
    
    for part in piece["parts"]:
        par = PyRTF.Paragraph(PyRTF.ParagraphPropertySet(alignment=2))
        par.append((part["name"] + "\n"*2).decode("utf8").encode('rtfunicode'))
        par.append((part["text"] + "\n"*2).decode("utf8").encode('rtfunicode'))
        section = PyRTF.Section()
        section.append(par)
        doc.Sections.append(section)
