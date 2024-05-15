from django.db import models
from artist_app.models.userModel import UserModel

NOTIFICATION_TYPE = [(1, "email"), (2, "push notification")]
NOTIFICATION_FOR = [(1, "all"), (2, "customer"), (3, "artist")]

class NotificationModel(models.Model):
    title = models.CharField(max_length=254, null=True, blank=True)  
    description = models.TextField(null=True, blank=True)
    for_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, blank=True, related_name="for_user")
    notification_type = models.IntegerField(choices = NOTIFICATION_TYPE, default=1)  
    notification_for = models.IntegerField(choices = NOTIFICATION_FOR, default=1) 
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.id
    
    class Meta:
        db_table = 'notification_model'
