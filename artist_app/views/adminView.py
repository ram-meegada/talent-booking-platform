from os import stat
from sys import api_version
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from artist_app.services.adminService import AdminService
import csv
import pandas as pd
from django.http import JsonResponse
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from artist_app.services.uploadMediaService import UploadMediaService
from artist_app.models.userModel import UserModel
from artist_app.serializers.adminSerializer import *
# from artist_python_backend.artist_app.models import talentDetailsModel


admin_obj = AdminService()

class AddTalentCategoryView(APIView):
    def post(self, request):
        result = admin_obj.add_category(request)
        return Response(result, status=result["status"])

class AddTalentSubCategoryView(APIView):
    def post(self, request):
        result = admin_obj.add_sub_category(request)
        return Response(result, status=result["status"])
    
class AddQuestionsAndAnswersView(APIView):
    def post(self , request):
        result = admin_obj.add_questions_answers(request)
        return Response(result,status=result["status"])


class UpdateQuestionsAnswersView(APIView):
    def put(self , request, id):
        result = admin_obj.update_questions_answers(request, id)
        return Response(result, status=result["status"])

class DeleteQuestionAnswerView(APIView):
    def delete(self, request, id):
        result = admin_obj.delete_question_answer(request, id)
        return Response(result, status=result["status"])

class GetAllQuestionsAnswers(APIView):
    def post(self , request):
        result = admin_obj.get_all_questions_answers(request)
        return Response(result, status=result["status"])

class GetQuestionById(APIView):
     def get(self, request, id):
        result = admin_obj.get_question_by_id(request,id)
        return Response(result, status=result["status"]) 

#terms and conditions

class AddTermsAndConditions(APIView):
    def put(self, request):
        result = admin_obj.add_terms_and_conditions(request)
        return Response(result, status=result["status"])

class UpdateTermsAndConditions(APIView):
    def put(self, request,id):
        result = admin_obj.update_terms_and_conditions(request, id)
        return Response(result, status=result["status"])

class GetTermsAndConditions(APIView):
    def get(self,request):
        result = admin_obj.get_terms_and_conditions(request)
        return Response(result, status=result["status"])

# admin onboarding

class AdminLoginView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        result = admin_obj.admin_login(request)
        return Response(result, status=result["status"])

class VerifyOTPViewAdminSide(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        result = admin_obj.verify_otp(request)
        return Response(result, status=result["status"])

class resendOTPView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        result = admin_obj.sent_otp(request)
        return Response(result, status=result["status"])

class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        result = admin_obj.forgot_password(request)
        return Response(result, status=result["status"])

class GetAdminDetailsByTokenView(APIView):
    def get(self, request):
        result = admin_obj.get_admin_details_by_token(request)
        return Response(result, status=result["status"])

class ChangePasswordByTokenView(APIView):
    def post(self, request):
        result = admin_obj.change_password_by_token(request)
        return Response(result, status=result["status"])

class UpdateAdminDetailsByTokenView(APIView):
    def put(self, request):
        result = admin_obj.update_admin_details_By_token(request)
        return Response(result, status= result["status"])

class LogOutView(APIView):
    def post(self, request):
        result = admin_obj.logout(request)
        return Response(result, status= result["status"])

#manage customers(clients)
class CustomerCSV(APIView):
    def get(self, request, * args , **kwargs):
        users = UserModel.objects.filter(role=1)
        serializer = GetAllClientsDetailsSerializer(users, many=True)
        df = pd.DataFrame(serializer.data)
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Users')
        excel_buffer.seek(0)
        excel_file = InMemoryUploadedFile(
            excel_buffer, 
            'media', 
            'users.xlsx', 
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
            excel_buffer.getbuffer().nbytes, 
            None
        )
        upload_media_service = UploadMediaService()
        excel_upload_result = upload_media_service.create_upload_media_xl(request, excel_file)
        url = excel_upload_result['file_url']
        
        # Construct your response data
        response_data = {
            "file_urls": url,
            "messages": "Excel file uploaded successfully.",
            "status": 200
        }

        # Return JSON response
        return JsonResponse(response_data)

class GetAllCustomerView(APIView):
    def post(self, request):
        result = admin_obj.get_all_customers(request)
        return Response(result, status=result["status"])

class BookingsOfCustomerView(APIView):
    def post(self, request, id):
        result = admin_obj.bookings_of_customer(request, id)
        return Response(result, status=result["status"])

class GetAllCustomerDetailsByidView(APIView):
    def get(self, request, id):
        result = admin_obj.get_custome_details_by_id(request, id)
        return Response(result, status=result["status"])

class AddCustomerByAdminView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = admin_obj.add_new_customer(request)
        return Response(result, status=result["status"])

class updateCustomerDetailsByAdminView(APIView):
    def put(self, request, id):
        result = admin_obj.edit_customer_by_admin(request, id)
        return Response(result, status=result["status"])

class DeleteCustomerByAdminView(APIView):
    def delete(self, request, id):
        result = admin_obj.delete_customer_by_admin(request, id)
        return Response(result, status=result["status"])

class DeleteCustomerByIdView(APIView):
    def delete(self, request, id):
        result = admin_obj.delete_subcategory_by_id(request, id)
        return Response(result, status=result["status"])

class UpdateStatusOfCustomerView(APIView):
    def put(self, request, id):
        result = admin_obj.change_status_of_customer_by_admin(request, id)
        return Response(result, status=result["status"])

#manage categories
class CategoryCSVView(APIView):
    def get(self, request, * args , **kwargs):
        users = TalentCategoryModel.objects.all()
        serializer = GetAllCategoriesSerializers(users, many=True)
        df = pd.DataFrame(serializer.data)
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Users')
        excel_buffer.seek(0)
        excel_file = InMemoryUploadedFile(
            excel_buffer, 
            'media', 
            'users.xlsx', 
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
            excel_buffer.getbuffer().nbytes, 
            None
        )
        upload_media_service = UploadMediaService()
        excel_upload_result = upload_media_service.create_upload_media_xl(request, excel_file)
        url = excel_upload_result['file_url']
        
        # Construct your response data
        response_data = {
            "file_urls": url,
            "messages": "Excel file uploaded successfully.",
            "status": 200
        }

        # Return JSON response
        return JsonResponse(response_data)
class GetAllCategoriesView(APIView):
    def post(self, request):
        result = admin_obj.get_all_categories(request)
        return Response(result, status=result["status"])

class AllCategoryView(APIView):
    def get(self, request):
        result = admin_obj.all_category(request)
        return Response(result, status=result["status"])

class GetCategoriesDetailsByIdView(APIView):
    def get(self, request, id):
        result = admin_obj.get_categories_detail_by_id(request, id)
        return Response(result, status=result["status"])

class UpdateCategoriesByIdView(APIView):
    def put(self, request,id):
        result = admin_obj.update_category_by_id(request, id)
        return Response(result, status=result["status"])

class DeleteCategoriesByIdView(APIView):
    def delete(self, request, id):
        result = admin_obj.delete_category_by_id(request, id)
        return Response(result, status=result["status"])

class GetAllSubCategoryBasedOnCategoryView(APIView):
    def post(self, request):
        result= admin_obj.get_all_subCategory(request)
        return Response(result, status=result["status"])

class GetSubCategoryByIdView(APIView):
    def get(self, request, id):
        result = admin_obj.get_subcategory_by_id(request, id)
        return Response(result, status=result["status"])

class UpdateStatusOfCategoryView(APIView):
    def patch(self, request, id):
        result = admin_obj.update_status_of_category(request, id)
        return Response(result, status=result["status"])

class UpdateSubcategoryByIdView(APIView):
    def put(self, request, id):
        result = admin_obj.update_subcategory_details(request,id)
        return Response(result, status=result["status"])

class DeleteSubcategoryByidView(APIView):
    def delete(self, request, id):
        result = admin_obj.delete_subcategory_by_id(request, id)
        return Response(result, status=result["status"])




# manage artist 

class ArtistCSVView(APIView):
    def get(self, request, * args , **kwargs):
        # users = UserModel.objects.filter(role=2)
        users = TalentDetailsModel.objects.filter(user__role=2)
        serializer = GetArtistDetailsSerializers(users, many=True)
        df = pd.DataFrame(serializer.data)
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Users')
        excel_buffer.seek(0)
        excel_file = InMemoryUploadedFile(
            excel_buffer, 
            'media', 
            'users.xlsx', 
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
            excel_buffer.getbuffer().nbytes, 
            None
        )
        upload_media_service = UploadMediaService()
        excel_upload_result = upload_media_service.create_upload_media_xl(request, excel_file)
        url = excel_upload_result['file_url']
        
        # Construct your response data
        response_data = {
            "file_urls": url,
            "messages": "Excel file uploaded successfully.",
            "status": 200
        }

        # Return JSON response
        return JsonResponse(response_data)

class GetAllArtistDetialsView(APIView):
    def post(self, request):
        result=admin_obj.get_all_artist_Details(request)
        return Response(result, status=result["status"])

class DeleteArtistByIdView(APIView):
    def delete(self, request, id):
        result= admin_obj.delete_artist_by_id(request, id)
        return Response(result, status=result["status"])

class GetArtistDetailsByIdView(APIView):
    def get(self, request, id):
        result = admin_obj.get_artist_by_id(request, id)
        return Response(result, status=result["status"])

class UpdateArtistDetailsByIdView(APIView):
    def put(self, request, id):
        result = admin_obj.Update_artist_details_by_id(request, id)
        return Response(result, status=result["status"])

class BookingsOfArtistView(APIView):
    def post(self, request, id):
        result = admin_obj.bookings_of_artist(request, id)
        return Response(result, status=result["status"])

class AddArtistThroughAdminView(APIView):
    def post(self, request):
        result= admin_obj.add_artist_through_admin(request)
        return Response(result, status=result["status"])

class FilterArtistBYnameView(APIView):
    def post(self, request, id):
        result = admin_obj.Search_artist_by_name(request)
        return Response(result, status=result["status"])

class VerifyArtistView(APIView):
    def patch(self, request, id):
        result = admin_obj.verify_artist(request, id)
        return Response(result, status=result["status"])


############## sub admin #####################

class AddSubAdminView(APIView):
    def post(self, request):
        result = admin_obj.add_sub_admin(request)
        return Response(result, status=result["status"])

class UpdateSubAdminView(APIView):
    def put(self, request, id):
        result = admin_obj.update_sub_admin_by_id(request, id)
        return Response(result, status=result["status"])

class SubAdminByIdView(APIView):
    def get(self, request, id):
        result = admin_obj.get_sub_admin_by_id(request, id)
        return Response(result, status=result["status"])

class DeleteSubAdminByIdView(APIView):
    def delete(self, request, id):
        result = admin_obj.delete_sub_admin_by_id(request, id)
        return Response(result, status=result["status"])

class GetAllSubAdminView(APIView):
    def post(self, request):
        result = admin_obj.get_all_sub_admin(request)
        return Response(result, status=result["status"])

####### booking module

class BookingCSVView(APIView):
    def get(self, request, * args , **kwargs):
        users = BookingTalentModel.objects.all()
        serializer = BookingsSerializer(users, many=True)
        df = pd.DataFrame(serializer.data)
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Users')
        excel_buffer.seek(0)
        excel_file = InMemoryUploadedFile(
            excel_buffer, 
            'media', 
            'users.xlsx', 
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
            excel_buffer.getbuffer().nbytes, 
            None
        )
        upload_media_service = UploadMediaService()
        excel_upload_result = upload_media_service.create_upload_media_xl(request, excel_file)
        url = excel_upload_result['file_url']
        
        # Construct your response data
        response_data = {
            "file_urls": url,
            "messages": "Excel file uploaded successfully.",
            "status": 200
        }

        # Return JSON response
        return JsonResponse(response_data)

class AllBookingsView(APIView):
    def post(self, request):
        result = admin_obj.all_bookings(request)
        return Response(result, status=result["status"])

class BookingdetaisByIdView(APIView):
    def get(self, request, id):
        result = admin_obj.booking_details_by_id(request, id)
        return Response(result, status=result["status"])
####Dashboard module

class DashboardKPIView(APIView):
    def get(self, request):
        result = admin_obj.kpi(request)
        return Response(result, status=result["status"])

class CustomerChartView(APIView):
    permission_classes=(AllowAny,)
    def post(self, request):
        result= admin_obj.client_chart(request)
        return Response(result, status= result["status"])

class RevenueChartView(APIView):
    def post(self, request):
        result = admin_obj.revenue_chart(request)
        return Response(result, status=result["status"])

class ArtistChartView(APIView):
    def post(self, request):
        result = admin_obj.artist_chart(request)
        return Response(result, status=result["status"])

class BookingChartView(APIView):
    def post(self, request):
        result = admin_obj.booking_chart(request)
        return Response(result, status=result["status"])

#### Notification Module
class NotificationCSVView(APIView):
    def get(self, request, * args , **kwargs):
        users = NotificationModel.objects.all()
        serializer = NotificationSerializer(users, many=True)
        df = pd.DataFrame(serializer.data)
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Users')
        excel_buffer.seek(0)
        excel_file = InMemoryUploadedFile(
            excel_buffer, 
            'media', 
            'users.xlsx', 
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
            excel_buffer.getbuffer().nbytes, 
            None
        )
        upload_media_service = UploadMediaService()
        excel_upload_result = upload_media_service.create_upload_media_xl(request, excel_file)
        url = excel_upload_result['file_url']
        
        # Construct your response data
        response_data = {
            "file_urls": url,
            "messages": "Excel file uploaded successfully.",
            "status": 200
        }

        # Return JSON response
        return JsonResponse(response_data)

class AddNotificationsView(APIView):
    def post(self, request):
        result = admin_obj.add_notification(request)
        return Response(result, status=result["status"])

class GetNotificationsView(APIView):
    def post(self, request):
        result = admin_obj.get_all_notification_listing(request)
        return Response(result, status=result["status"])

##privacy police

class AddPrivacyPolicy(APIView):
    def put(self, request):
        result = admin_obj.add_privacy_poicy(request)
        return Response(result, status=result["status"])

class GetPrivacyPolicy(APIView):
    def get(self, request):
        result = admin_obj.get_privacy_policy(request)
        return Response(result, status=result["status"])
#customer support

class AddCustomerSupport(APIView):
    def put(self, request):
        result = admin_obj.add_customer_support(request)
        return Response(result, status=result["status"])

class getCustomerSupport(APIView):
    def get(self, request):
        result = admin_obj.get_customer_support(request)
        return Response(result, status=result["status"])

class AddServiceFeesView(APIView):
    permission_classes = [AllowAny]
    def put(self, request):
        result = admin_obj.add_service_fees(request)
        return Response(result, status=result["status"])

class getServiceFeesView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        result = admin_obj.get_service_fees(request)
        return  Response(result, status = result["status"])

## revenue Model

class GetAllRevenueDetails(APIView):
    def post(self, request):
        result = admin_obj.get_all_revenue_details(request)
        return Response(result, status=result["status"])

class ExportRevenueCSVView(APIView):
    def get(self, request, * args , **kwargs):
        users = BookingTalentModel.objects.all()
        serializer = GetRevenueDetails(users, many=True)
        df = pd.DataFrame(serializer.data)
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Users')
        excel_buffer.seek(0)
        excel_file = InMemoryUploadedFile(
            excel_buffer, 
            'media', 
            'users.xlsx', 
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
            excel_buffer.getbuffer().nbytes, 
            None
        )
        upload_media_service = UploadMediaService()
        excel_upload_result = upload_media_service.create_upload_media_xl(request, excel_file)
        url = excel_upload_result['file_url']
        
        # Construct your response data
        response_data = {
            "file_urls": url,
            "messages": "Excel file uploaded successfully.",
            "status": 200
        }

        # Return JSON response
        return JsonResponse(response_data)
#####rating and review module

class GetALLRatingDetials(APIView):
    def post(self, request):
        result = admin_obj.get_all_review_details(request)
        return Response(result, status=result["status"])

class ExportRatingCSVView(APIView):
    def get(self, request, * args , **kwargs):
        users = ReviewAndRatingsModel.objects.all()
        serializer = GetAllRatingDetails(users, many=True)
        df = pd.DataFrame(serializer.data)
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Users')
        excel_buffer.seek(0)
        excel_file = InMemoryUploadedFile(
            excel_buffer, 
            'media', 
            'users.xlsx', 
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
            excel_buffer.getbuffer().nbytes, 
            None
        )
        upload_media_service = UploadMediaService()
        excel_upload_result = upload_media_service.create_upload_media_xl(request, excel_file)
        url = excel_upload_result['file_url']
        
        # Construct your response data
        response_data = {
            "file_urls": url,
            "messages": "Excel file uploaded successfully.",
            "status": 200
        }

        # Return JSON response
        return JsonResponse(response_data)

        







