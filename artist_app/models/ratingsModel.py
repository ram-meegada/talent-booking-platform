from django.db import models
from artist_app.models.baseModel import BaseModel
from artist_app.models.userModel import UserModel

BEST_LIKED_CHOICES = [
	(1, "Punctuality"),
	(2, "Clarity"),
	(3, "Helpfulness")
]

class ReviewAndRatingsModel(BaseModel):
    talent = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="ratings_talent_user")
    client = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    best_liked = models.IntegerField(choices=BEST_LIKED_CHOICES)
    review = models.TextField()
    rating = models.IntegerField()
    
    def __str__(self):
        return f"{self.talent} - {self.client}"
    
    class Meta:
        db_table = 'review and ratings'