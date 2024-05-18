from difflib import restore
from rest_framework.response import Response
from rest_framework.views import APIView
from artist_app.services.clientService import ClientService
from rest_framework.permissions import AllowAny,IsAuthenticated

userservice = ClientService()

class SignUpView(APIView):
    permission_classes = (AllowAny,)
    def post(self,request):
        result = userservice.user_signup(request)
        return Response(result, result["status"])

class VerifyOtpViaMailView(APIView):
    permission_classes = (AllowAny,)
    def post(self , request):
        result = userservice.verify_otp(request)
        return Response(result , result["status"])

class LogInView(APIView):
    permission_classes = (AllowAny,)
    def post(self,request):
        result= userservice.login(request)
        return Response(result, result["status"])

class ResendOtpView(APIView):
    permission_classes = (AllowAny,)
    def post(self , request):
        result = userservice.resend_otp(request)
        return Response(result , result["status"])
    

################################ADDRESS MANAGE ##############################

class AddClientNewAddressDetailsView(APIView):
    def post(self, request):
        result = userservice.add_address_using_token(request)
        return Response(result, result["status"])

class EditClientAddressDetailsView(APIView):
    def put(self, request,id ):
        result = userservice.edit_address_details(request,id)
        return Response(result, result["status"])


class DeleteClientAddressDetailsBYIDView(APIView):
    def delete(self, request, id):
        result = userservice.delete_address_details_by_id(request, id)
        return Response(result, result["status"])

class ShowAllAddressesDetailsView(APIView):
    def get(self, request):
        result = userservice.show_all_address_with_token(request)
        return Response(result, result["status"])


#-------------------------------booking talent -------------------------

class ListingAllCategories(APIView):
    def get(self, request):
        result = userservice.All_categories(request)
        return Response(result, status=result["status"])

class ListingAllSubCategoriesBasedOnCategories(APIView):
    def post(self, request):
        result = userservice.all_sub_categories(request)
        return Response(result, status=result["status"])

class ListingAllTalent(APIView):
    def post(self, request):
        result = userservice.talents_details(request)
        return Response(result, status=result["status"])

class TalentDetailsById(APIView):
    def get(self, request,id):
        result = userservice.view_talent_all_details_by_id(request,id)
        return Response(result, status=result["status"])

class BookTalentView(APIView):
    def post(self,request):
        result = userservice.book_talent(request)
        return Response(result,status=result["status"])

class GetTalentSlotsView(APIView):
    def post(self,request):
        result = userservice.get_slots_by_date(request)
        return Response(result,status=result["status"])

class GetAllBookTalentDetails(APIView):
    def get(self, request, id):
        result = userservice.get_booking_details_by_id(request, id)
        return Response(result,status=result["status"])

class EditClientDetailsByTokenView(APIView):
    def put(self, request):
        result = userservice.edit_client_details_by_token(request)
        return Response(result,status=result["status"])

class FetchAllTalentServicesView(APIView):
    def get(self, request, id):
        result = userservice.talent_services(request, id)
        return Response(result,status=result["status"])
