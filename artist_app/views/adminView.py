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