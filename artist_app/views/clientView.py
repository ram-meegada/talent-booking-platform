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
        return Response(result,result["status"])

class VerifyOtpViaMailView(APIView):
    permission_classes = (AllowAny,)
    def post(self , request):
        result = userservice.verify_otp(request)
        return Response(result , result["status"])

class LogInView(APIView):
    permission_classes = (AllowAny,)
    def post(self,request):
        result= userservice.log_in(request)
        return Response(result, result["status"])

class ResendOtpView(APIView):
    permission_classes = (AllowAny,)
    def post(self , request):
        result = userservice.resend_otp(request)
        return Response(result , result["status"])