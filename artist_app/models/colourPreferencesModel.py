from artist_app.models.baseModel import BaseModel
from django.db import models
from artist_app.utils.choiceFields import PREFERENCE_TYPES

class ColourPreferencesModel(BaseModel):
    name = models.CharField(max_length=100)
    preference_type = models.IntegerField(choices=PREFERENCE_TYPES)

    class Meta:
        db_table = "Colour preferences"
