import uuid
from django.db import models
from artist_app.models.baseModel import BaseModel
from artist_app.models.userModel import UserModel

class ChatSessionModel(BaseModel):
    session_id = models.CharField(max_length=100)
    client = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="client_user")
    talent = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="talent_user")

    class Meta:
        db_table = "Chat Sessions"