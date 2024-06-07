from django.db import models
from artist_app.models import UserModel
from artist_app.utils.choiceFields import MODULE_CHOICES

class PermissionModel(models.Model):
    module = models.IntegerField(choices=MODULE_CHOICES)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    is_add = models.BooleanField(default=False)
    is_view = models.BooleanField(default=False)
    is_edit = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    # can_view = models.BooleanField(default=False)
    # can_be_delete = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=True)

    def __str__(self):
        return str(self.role.role_name + self.user)

    class Meta:
        db_table = 'permissions'
