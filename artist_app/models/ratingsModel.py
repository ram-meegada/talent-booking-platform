from django.db import models
from artist_app.models.baseModel import BaseModel
from artist_app.models.userModel import UserModel
from artist_app.models.bookingTalentModel import BookingTalentModel
from django.contrib.postgres.fields import ArrayField

BEST_LIKED_CHOICES = [
	(1, "Punctuality"),
	(2, "Clarity"),
	(3, "Helpfulness")
]

GIVEN_CHOICES = [
    (1, "client"),
    (2, "talent"),
]

class ReviewAndRatingsModel(BaseModel):
    talent = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="ratings_talent_user")
    client = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    best_liked = ArrayField(models.CharField(max_length=100), default=list)
    review = models.TextField()
    rating = models.IntegerField()

    booking = models.ForeignKey(BookingTalentModel, on_delete=models.CASCADE, blank=True, null=True)

    given_by = models.IntegerField(choices=GIVEN_CHOICES, blank=True, null=True)
    
    def __str__(self):
        return f"{self.talent} - {self.client}"
    
    class Meta:
        db_table = 'review and ratings'