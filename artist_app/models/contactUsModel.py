from django.db import models
from artist_app.models.baseModel import BaseModel
from django.utils import timezone

class ContactUsModel(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    phone_no = models.CharField(max_length=20, blank=True, null=True)

    #terms and conditions
    data = models.TextField(default="")
    privacy_policy = models.TextField(default="")

    service_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    class Meta:
        db_table = "ContactUsModel"
