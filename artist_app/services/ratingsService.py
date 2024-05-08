from artist_app.models.ratingsModel import ReviewAndRatingsModel
from artist_app.serializers.ratingsSerializer import AddRatingSerializer, GetRatingSerializer
from artist_app.utils import messages

class RatingService():
    def add_rating(self, request, talent_id):
        request.data["talent"] = talent_id
        serializer = AddRatingSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return {"data": serializer.data, "message": messages.ADDED_RATING, "status": 200}
        return {"data": serializer.errors, "message": messages.WENT_WRONG, "status": 400}
    
    def get_talent_ratings(self, request, talent_id):
        ratings = ReviewAndRatingsModel.objects.filter(talent=talent_id)
        serializer = GetRatingSerializer(ratings, many=True)
        return {"data": serializer.data, "message": "Ratings fetched successfully", "status": 200}    