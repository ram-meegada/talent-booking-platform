from django.db import models
from artist_app.models.baseModel import BaseModel
from django.contrib.auth.models import AbstractUser
from artist_app.models.uploadMediaModel import UploadMediaModel
from artist_app.utils.choiceFields import GENDER_CHOICES, ROLE_CHOICE, PROFILE_STATUS_CHOICES,\
                                          VERIFICATION_STATUS_CHOICES, EXPERIENCE_CHOICES

class UserModel(AbstractUser):
    #Email field
    email = models.EmailField(unique = True, blank=True, null=True)

    #character fields
    username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, default="")
    last_name = models.CharField(max_length=255, default="")
    country_code = models.CharField(max_length=100, default="")
    phone_no = models.CharField(max_length=100, unique = True, blank=True, null=True)
    city = models.CharField(max_length = 100, default = "")
    state = models.CharField(max_length = 100, default = "")
    country = models.CharField(max_length = 100, default = "")
    otp = models.CharField(max_length = 255, default = "")
    password = models.CharField(max_length=500, default="")
    encoded_id = models.CharField(max_length=500, default="")
    name = models.CharField(max_length=500, default="")

    #Boolean fields
    otp_email_verification = models.BooleanField(default = False)
    otp_phone_no_verification = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_deleted = models.BooleanField(default = False)

    #Integer fields
    role = models.IntegerField(choices=ROLE_CHOICE, blank=True, null=True)
    gender = models.IntegerField(choices = GENDER_CHOICES, blank = True, null = True)
    profile_status = models.IntegerField(choices=PROFILE_STATUS_CHOICES, default=0)
    verification_status = models.IntegerField(choices=VERIFICATION_STATUS_CHOICES, default=0)
    experience = models.IntegerField(choices=EXPERIENCE_CHOICES, blank=True, null=True)

    #foreign keys
    profile_picture = models.ForeignKey(UploadMediaModel, on_delete=models.SET_NULL, null=True)

    #DateTime fields
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    deleted_at = models.DateTimeField(blank = True , null = True)
    otp_sent_time = models.DateTimeField(blank = True , null = True)

    #Date fields
    date_of_birth = models.DateField(blank = True, null = True)

    #Text fields
    # experience = models.TextField(default = "")
    address = models.TextField(default = "")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_no"]

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "User"