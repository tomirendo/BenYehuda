from main import models
from ebooklib import epub

pieces = models.Piece.objects.all()
for index,piece in enumerate(pieces):
    book = epub.EpubBook()

    # set metadata
    book.set_title(piece.name)
    book.set_language('he')

    book.add_author(piece.creator.name)

    # create chapter
    spn = []
    for chapter in sorted(book.chapters.objects.all(),key = lambda x:x.index):
        c = epub.EpubHtml(title=chapter.name, file_name='{}.xhtml'.format(chapter.index), lang='he')
        c.content=chapter.text

        book.add_item(c)
        spn.append(c)

    # # define Table Of Contents
    # book.toc = (epub.Link('chap_01.xhtml', 'Introduction', 'intro'),
    #              (epub.Section('Simple book'),
    #              (c1, ))
    #             )

    # add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # define CSS style
    style = 'BODY {color: white;}'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

    # add CSS file

    book.add_item(*([nav_css] + spn))

    # basic spine

    # write to the file
    epub.write_epub('{}.epub'.format(index), book, {})