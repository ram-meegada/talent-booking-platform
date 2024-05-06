from django.db import models
from artist_app.models.baseModel import BaseModel
from artist_app.models import TalentDetailsModel,ManageAddressModel, UserModel
# from artist_app.models.
from artist_app.utils.choiceFields import BOOKING_STATUS

class BookingTalentModel(BaseModel):
    # Foreign Keys
    talent = models.ForeignKey(TalentDetailsModel, on_delete=models.CASCADE)
    address = models.ForeignKey(ManageAddressModel, on_delete=models.CASCADE)
    client = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    # booking details
    # choose service  this field is left. we have to create in this model

    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(choices=BOOKING_STATUS, blank=True, null=True)
    offer_price = models.IntegerField(default=0)
    comment = models.TextField(default="")
    currency = models.CharField(max_length=10, null=True, blank=True)


    class Meta:
        db_table = "bookingDetails"

    @property
    def test(self):
        return str(self.date) + str(self.time)    