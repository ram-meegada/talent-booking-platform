from django.db import models
from artist_app.models.baseModel import BaseModel
from artist_app.models.talentCategoryModel import TalentCategoryModel

class TalentSubCategoryModel(BaseModel):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(TalentCategoryModel, on_delete=models.CASCADE)

    class Meta:
        db_table = "Talent Sub Category"