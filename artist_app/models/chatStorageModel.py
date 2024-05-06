from django.db import models
from artist_app.models.baseModel import BaseModel
from artist_app.models import ChatSessionModel, UserModel

class ChatStorageModel(BaseModel):
    session = models.ForeignKey(ChatSessionModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="user")
    timestamp = models.DateTimeField()

    class Meta:
        db_table = "Chat Storage"