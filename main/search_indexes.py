import datetime
from haystack import indexes
from main.models import Creator, Translator, Piece, Chapter


class CreatorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    #CharField
    def get_model(self):
        return Creator

class TranslatorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    def get_model(self):
        return Translator


class PieceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    def get_model(self):
        return Piece

"""
    def index_queryset(self, using=None):
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
"""