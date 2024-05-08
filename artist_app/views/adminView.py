from sys import api_version
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from artist_app.services.adminService import AdminService

admin_obj = AdminService()

class AddTalentCategoryView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        result = admin_obj.add_category(request)
        return Response(result, status=result["status"])

class AddTalentSubCategoryView(APIView):
    permission_classes = (AllowAny,)
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
    def get(self , request):
        result = admin_obj.get_all_questions_answers(request)
        return Response(result, status=result["status"])

#terms and conditions

class AddTermsAndConditions(APIView):
    def post(self, request):
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

class updateAdminDetailsByTokenView(APIView):
    def put(self, request):
        result = admin_obj.update_admin_details_By_token(request)
        return Response(result, status= result["status"])

class LogOutView(APIView):
    def post(self, request):
        result = admin_obj.logout(request)
        return Response(result, status= result["status"])

#manage customers(clients)

class GetAllCustomerView(APIView):
    def get(self, request):
        result = admin_obj.get_all_customers(request)
        return Response(result, status=result["status"])

class GetAllCustomerDetailsByidView(APIView):
    def get(self, request, id):
        result = admin_obj.get_custome_details_by_id(request, id)
        return Response(result, status=result["status"])

class AddCustomerByAdminView(APIView):
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


#manage categories

class GetAllCategoriesView(APIView):
    def get(self, request):
        result = admin_obj.get_all_categories(request)
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
class UpdateSubcategoryByIdView(APIView):
    def put(self, request, id):
        result = admin_obj.update_subcategory_details(request,id)
        return Response(result, status=result["status"])

class DeleteSubcategoryByIdView(APIView):
    def delete(self, request, id):
        result = admin_obj.delete_subcategory_by_id(request, id)
        return Response(result, status=result["status"])
        







