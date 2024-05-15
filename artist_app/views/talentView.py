from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from artist_app.services.talentService import TalentService

talent_service = TalentService()

class TalentSignUpView(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        result = talent_service.user_signup(request)
        return Response(result, status=result["status"])

class TalentLoginView(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        result = talent_service.login(request)
        return Response(result, status=result["status"])
    
class SendEmailOrPhoneView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        result = talent_service.resend_otp(request)
        return Response(result, status=result["status"])

class VerifyMailOrPhoneView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        result = talent_service.verify_otp(request)
        return Response(result, status=result["status"])

class SubCategoryListingView(APIView):
    def post(self, request):
        result = talent_service.sub_category_listing(request)
        return Response(result, status=result["status"])

class ProfileSetUpAndUpdateView(APIView):
    def put(self, request):
        result = talent_service.profile_setup_and_edit(request)
        return Response(result, status=result["status"])

class ResendOtpView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        result = talent_service.resend_otp(request)
        return Response(result, status=result["status"])

class TalentUserDetailsView(APIView):
    def get(self, request):
        result = talent_service.user_details_by_token(request)
        return Response(result, status=result["status"])

#clientBookinglisting

class ClientUpcomingBookingListing(APIView):
    def get(self, request):
        result = talent_service.upcoming_clients_booking_listing(request)
        return Response(result, status=result["status"])

class ClientPastBookingListing(APIView):
    def get(self, request):
        result = talent_service.past_client_booking_listing(request)
        return Response(result, status=result["status"])

class ClientdeclineParamenterListing(APIView):
    def get(self, request):
        result= talent_service.cancel_client_booking_list(request)
        return Response(result, status=result["status"])

class AllCategoriesView(APIView):
    def get(self, request):
        result= talent_service.all_categories(request)
        return Response(result, status=result["status"])


############# slots ###############
class GenerateSlotsView(APIView):
    def post(self, request):
        result = talent_service.add_slots(request)
        return Response(result, status=result["status"])

class FetchWeeklyTimingsView(APIView):
    def get(self, request):
        result = talent_service.fetch_weekly_timings(request)
        return Response(result, status=result["status"])
