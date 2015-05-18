from django.db import models
from .NikudFunctions import remove_nikud

# Create your models here.
class Creator(models.Model):
    name = models.CharField(max_length = 250)
    birth = models.IntegerField(default = 1900)
    death = models.IntegerField(default = 0)
    description = models.CharField(max_length = 2000)
    wikipedia_link = models.CharField(max_length = 200,null = True)
    def __str__(self):
        return "<creator : {}>".format(self.name.encode("utf8"))

    def to_dict(self):
        return {'name' : self.name,
                'description' : self.description,
                'id' : self.id,
                'object_type' : 'creator'}


class Translator(models.Model):
    name = models.CharField(max_length = 250)
    birth = models.IntegerField(default = 1900)
    death = models.IntegerField(default = 0,null =True,blank = True)
    description = models.CharField(max_length = 2000)
    wikipedia_link = models.CharField(max_length = 200,null = True,blank = True)
    def __str__(self):
        return "<translateor : {} >".format(self.name.encode("utf8"))
 
class Piece(models.Model):
    name = models.CharField(max_length = 250)
    creator = models.ForeignKey(Creator)
    translator = models.ForeignKey(Translator,null = True,blank = True)
    date = models.DateField(null = True,blank = True)
    chapters = models.ManyToManyField("Chapter")
    def __str__(self):
        return "<piece : {}>".format(self.name.encode("utf8"))

    def get_full_text(self):
        return str.join("",(i.text for i in self.chapters.all()))
    def get_full_text_without_nikud(self):
        return remove_nikud(self.get_full_text())
    def to_dict(self):
        return {'name' : self.name,
                'creator_name' : self.creator.name,
                'creator_id' : self.creator.id,
                'text' : self.get_full_text(),
                'text_without_nikud' : self.get_full_text_without_nikud(),
                'id' : self.id,
                'object_type' : 'piece'}


class Chapter(models.Model):
    name = models.CharField(max_length = 250)
    text = models.TextField()
    searchable_text = None
    index = models.IntegerField()
    def __str__(self):
        return "<chapter : {} >".format(self.name.encode("utf8"))

