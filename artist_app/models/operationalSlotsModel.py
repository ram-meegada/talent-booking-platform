from django.db import models
from artist_app.models.baseModel import BaseModel
from artist_app.models.userModel import UserModel

class OperationalSlotsModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    day = models.CharField(max_length=100)
    start = models.TimeField()
    end = models.TimeField()
    
    class Meta:
        db_table = "Operational slots"