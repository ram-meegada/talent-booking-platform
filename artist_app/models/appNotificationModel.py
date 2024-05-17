from artist_app.models.userModel import UserModel
from artist_app.models.baseModel import BaseModel
from django.db import models
from artist_app.utils.choiceFields import NOTIFICATION_TYPE_CHOICES

class AppNotificationModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPE_CHOICES)
    title = models.TextField()

    class Meta:
        db_table = "App Notifications"