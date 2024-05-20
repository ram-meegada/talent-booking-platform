from django.db import models
from artist_app.models.baseModel import BaseModel
from artist_app.models.uploadMediaModel import UploadMediaModel

class TalentCategoryModel(BaseModel):
    image = models.ForeignKey(UploadMediaModel, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "Talent Category"