from django.db import models
from artist_app.models.baseModel import BaseModel

class TermAndConditionModel(BaseModel):
    data = models.TextField(default="")
    privacy_policy = models.TextField(default="")

    class Meta:
        db_table = "Terms_And_condition"