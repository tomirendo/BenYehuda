from main import models
from json import dumps

ps = models.Piece.objects.all()

pieces = [i.to_dict() for i in ps]

print(dumps(pieces))
