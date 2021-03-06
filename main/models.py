from django.db import models
from .NikudFunctions import remove_nikud
import json

# Create your models here.
class Creator(models.Model):
    name = models.CharField(max_length = 250)
    english_name = models.CharField(max_length = 250)
    birth = models.IntegerField(default = 1900)
    death = models.IntegerField(default = 0)
    description = models.CharField(max_length = 2000)
    wikipedia_link = models.CharField(max_length = 200,null = True)
    def __str__(self):
        return "<creator : {}>".format(self.name.encode("utf8"))

    def to_dict(self):
        return {'name' : self.name,
                'english_name':self.english_name,
                'description' : self.description,
                'id' : self.id,
                'object_type' : 'creator',
                'wikipedia_link' : self.wikipedia_link}




class Translator(models.Model):
    name = models.CharField(max_length = 250)
    birth = models.IntegerField(default = 1900)
    death = models.IntegerField(default = 0,null =True,blank = True)
    description = models.CharField(max_length = 2000)
    wikipedia_link = models.CharField(max_length = 200,null = True,blank = True)
    def __str__(self):
        return "<translateor : {} >".format(self.name.encode("utf8"))
 
    def to_dict(self):
        return {'name' : self.name,
                }

    def to_str(self):
        return json.dumps(self.to_dict())

class Piece(models.Model):
    name = models.CharField(max_length = 250)
    english_name = models.CharField(max_length = 250)
    creator = models.ForeignKey(Creator)
    translator = models.ForeignKey(Translator,null = True,blank = True)
    date = models.DateField(null = True,blank = True)
    chapters = models.ManyToManyField("Chapter")
    def __str__(self):
        return "<piece : {}>".format(self.name.encode("utf8"))

    def get_full_text(self):
        return str.join("",
            (str.join("",[i.name, i.text])
                for i in self.chapters.all()))

    def get_full_text_without_nikud(self):
        return remove_nikud(self.get_full_text())

    def to_dict(self):
        return {'name' : self.name,
                'english_name' : self.english_name,
                'creator_name' : self.creator.name,
                'creator_id' : self.creator.id,
                'text' : self.get_full_text(),
                'text_without_nikud' : self.get_full_text_without_nikud(),
                'id' : self.id,
                'object_type' : 'piece'}


    def to_str(self):
        return json.dumps(self.to_dict())


class Chapter(models.Model):
    name = models.CharField(max_length = 250)
    text = models.TextField()
    searchable_text = None
    index = models.IntegerField()
    def __str__(self):
        return "<chapter : {} >".format(self.name.encode("utf8"))

