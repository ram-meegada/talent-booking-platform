from django.db import models
from artist_app.models.baseModel import BaseModel

class TalentCategoryModel(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "Talent Category"