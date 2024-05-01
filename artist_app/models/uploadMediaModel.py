from django.db import models
from artist_app.models.baseModel import BaseModel

class UploadMediaModel(BaseModel):
    media_file_url = models.TextField()
    media_file_name = models.CharField(max_length=100)
    media_file_type = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        db_table = "Media"