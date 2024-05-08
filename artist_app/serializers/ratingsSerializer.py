from rest_framework import serializers
from artist_app.models.ratingsModel import ReviewAndRatingsModel
from artist_app.serializers.chatSerializer import UserDetailsSerializer
from django.db.models import Avg

class AddRatingSerializer(serializers.ModelSerializer):
	client = serializers.HiddenField(default=serializers.CurrentUserDefault())
	class Meta:
		model = ReviewAndRatingsModel
		fields = ["id", "talent", "client", "review", "rating", "best_liked"]
		
class GetRatingSerializer(serializers.ModelSerializer):
	client = UserDetailsSerializer()
	talent = UserDetailsSerializer()
	average_rating = serializers.SerializerMethodField()
	class Meta:
		model = ReviewAndRatingsModel
		fields = ["id", "talent", "client", "review", "rating", "average_rating"]
	def get_average_rating(self, obj):
		average = ReviewAndRatingsModel.objects.filter()