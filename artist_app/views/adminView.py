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