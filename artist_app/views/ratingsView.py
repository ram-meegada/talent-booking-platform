from rest_framework.views import APIView
from rest_framework.response import Response
from artist_app.services.ratingsService import RatingService

ratings_obj = RatingService()

class AddRatingView(APIView):
    def post(self, request, talent_id):
        result = ratings_obj.add_rating(request, talent_id)
        return Response(result, status=result["status"])

class GetUserRatingView(APIView):
    def get(self, request, talent_id):
        result = ratings_obj.get_talent_ratings(request, talent_id)
        return Response(result, status=result["status"])