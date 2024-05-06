import uuid
from django.db import models
from artist_app.models.baseModel import BaseModel
from artist_app.models.userModel import UserModel

class ChatSessionModel(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4)
    client = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="client_user")
    talent = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="talent_user")

    class Meta:
        db_table = "Chat Sessions"