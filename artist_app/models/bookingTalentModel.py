from django.db import models
from artist_app.models.baseModel import BaseModel
from artist_app.models import TalentDetailsModel,ManageAddressModel, UserModel
# from artist_app.models.
from artist_app.utils.choiceFields import BOOKING_STATUS, TRACK_BOOKING

class BookingTalentModel(BaseModel):
    talent = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="talent_booking_user")
    address = models.ForeignKey(ManageAddressModel, on_delete=models.CASCADE)
    client = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, help_text="in hours")

    status = models.IntegerField(choices=BOOKING_STATUS, blank=True, null=True)
    track_booking = models.IntegerField(choices=TRACK_BOOKING, blank=True, null=True)

    offer_price = models.IntegerField(default=0)
    counter_offer_price = models.IntegerField(blank=True, null=True)
    comment = models.TextField(default="")
    currency = models.CharField(max_length=10, null=True, blank=True)
    services = models.JSONField(default=list)


    class Meta:
        db_table = "bookingDetails"

    @property
    def test(self):
        return str(self.date) + str(self.time)    