from django.db import models
from artist_app.models.baseModel import BaseModel
from artist_app.models import TalentDetailsModel,ManageAddressModel, UserModel
# from artist_app.models.
from artist_app.utils.choiceFields import BOOKING_STATUS, TRACK_BOOKING

class BookingTalentModel(BaseModel):
    booking_id = models.IntegerField(blank=True, null=True)

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
    final_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    comment = models.TextField(default="")
    currency = models.CharField(max_length=10, null=True, blank=True)
    services = models.JSONField(default=list)

    rating_by_client = models.BooleanField(default=False)
    rating_by_talent = models.BooleanField(default=False)

    cancellation_reason = models.TextField(blank=True, null=True)

    payment_completed = models.BooleanField(default=False)

    client_marked_completed = models.BooleanField(default=False)
    talent_marked_completed = models.BooleanField(default=False)

    class Meta:
        db_table = "bookingDetails"
