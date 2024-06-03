from django.db import models
from artist_app.models.baseModel import BaseModel
from artist_app.models.userModel import UserModel
from artist_app.models.uploadMediaModel import UploadMediaModel
from django.contrib.postgres.fields import ArrayField
from artist_app.utils.choiceFields import HAIR_COLOR_CHOICES, EYE_COLOR_CHOICES, BOOKING_METHOD_CHOICES

class TalentDetailsModel(BaseModel):    
    #foreign keys
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, blank=True, null=True)

    #integer fields
    bust = models.IntegerField(help_text="in inches", blank=True, null=True)
    waist = models.IntegerField(help_text="in inches", blank=True, null=True)
    hips = models.IntegerField(help_text="in inches", blank=True, null=True)
    height_feet = models.IntegerField(help_text="in feet", blank=True, null=True)
    height_inches = models.IntegerField(help_text="in inches", blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    hair_color = models.IntegerField(choices=HAIR_COLOR_CHOICES, default=0, blank=True, null=True)
    eye_color = models.IntegerField(choices=EYE_COLOR_CHOICES, default=0, blank=True, null=True)
    booking_method = models.IntegerField(choices=BOOKING_METHOD_CHOICES, default=0)

    #media
    portfolio = ArrayField(models.IntegerField(), default=list)
    cover_photo = models.ForeignKey(UploadMediaModel, on_delete=models.SET_NULL, blank=True, null=True)

    #others
    categories = ArrayField(models.IntegerField(), default=list)
    sub_categories = ArrayField(models.IntegerField(), default=list)
    services = models.JSONField(default=list)
    tags = models.JSONField(default=list)

    class Meta:
        db_table = "Talent details"