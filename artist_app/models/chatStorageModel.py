from django.db import models
from artist_app.models.baseModel import BaseModel
from artist_app.models import ChatSessionModel, UserModel
from datetime import datetime

class ChatStorageModel(BaseModel):
    session = models.ForeignKey(ChatSessionModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="user")
    message = models.TextField(default="")
    timestamp = models.DateTimeField(default=datetime.now())

    class Meta:
        db_table = "Chat Storage"
