from main import models
from json import dumps

ps = models.Piece.objects.all()
cts = models.Creator.objects.all()

pieces = [i.to_dict() for i in ps]

creators = [i.to_dict() for i in cts]

data_file = "data/data_file.json"
with open(data_file,"w") as f:
	f.write(dumps(pieces + creators))

