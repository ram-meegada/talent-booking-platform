from django.db import models
from artist_app.models import userModel, baseModel
from artist_app.utils.choiceFields import ADDRESS_CHOICE

class ManageAddressModel(baseModel.BaseModel):
    user = models.ForeignKey(userModel.UserModel, on_delete=models.CASCADE)
    address_location = models.TextField()
    house_flat_block_no = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    street_no = models.CharField(max_length=255, blank=True, null=True)
    phone_no_manage_address = models.CharField(max_length=255, blank=True, null=True)
    address_type = models.IntegerField(choices=ADDRESS_CHOICE, blank=True, null=True)
    city = models.CharField(max_length = 100, default = "")
    state = models.CharField(max_length = 100, default = "")
    country = models.CharField(max_length = 100, default = "")
    
    is_default = models.BooleanField(default=False)
    class Meta:
        db_table  = "ManageAddress"