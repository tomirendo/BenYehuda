from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.models import User

from main.models import Creator,Translator,Piece,Chapter
import main

from rest_framework import routers, serializers, viewsets,filters,generics

# Serializers define the API representation.
class CreatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Creator
        fields = ("pk",'name', 'birth', 'death', 'description','wikipedia_link','piece_set')

class TranslatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Translator
        fields = ("pk",'name', 'birth', 'death', 'description','wikipedia_link','piece_set')

class PieceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Piece
        fields = ("pk",'name', 'creator','creator', 'translator', 'chapters')

class ChapterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chapter
        fields = ("pk",'name', 'text', 'index')

# ViewSets define the view behavior.
class CreatorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

class TranslatorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Translator.objects.all()
    serializer_class = TranslatorSerializer 
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

class PieceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Piece.objects.all()
    serializer_class = PieceSerializer
    filter_backends = (filters.SearchFilter,filters.DjangoFilterBackend)
    search_fields = ("name","description")
    filter_fields = ("creator",)

class ChapterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'creator', CreatorViewSet)
router.register(r'translator', TranslatorViewSet)
router.register(r'piece', PieceViewSet)
router.register(r'chapter', ChapterViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BenYehuda.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^download/(?P<id>\d+)/$', 'main.views.download'),
    url(r'^search/', include('haystack.urls')),
    url(r'^search_solr/(?P<search_term>.+)/$','main.views.search'),


    #url(r'^$','main.views.index'),
    #url(r'^script.js$','main.views.script'),
)
