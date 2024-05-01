from re import I
from rest_framework.response import Response
from artist_app.serializers.Clientserializer import CreateClientSerializers
from django.contrib.auth.hashers import check_password
from artist_app.utils.sendOtp import send_otp_via_mail
from rest_framework import status
from artist_app.models.userModel import UserModel
from rest_framework_simplejwt.tokens import RefreshToken

class ClientService():
    def create_username(self , email):
        s = ""
        for i in email:
            if i=='@':
                break
            else:
                s+=i 
        return s
    def user_signup(self , request):
        serializers = CreateClientSerializers(data = request.data)
        try :
            if serializers.is_valid():
                otp_val = send_otp_via_mail(request.data["email"],request.data["first_name"])
                user = serializers.save()
                user.set_password(request.data["password"])
                user.username = self.create_username(request.data["email"])
                user.otp = otp_val
                user.save()
                return {"data":serializers.data,"status":status.HTTP_200_OK}
        except Exception as e:
            return {"Error":str(e),"status":status.HTTP_400_BAD_REQUEST}


    def verify_otp(self , request):
        if "email" in request.data:
            user = UserModel.objects.get(email = request.data["email"])
            enter_otp = request.data.get("otp")
            try:
                if user.otp == enter_otp:
                    user.otp_email_verification = True
                    user.save()
                    return {"message":"otp in verified","status":status.HTTP_200_OK}
                else:
                    return {"message":"otp is not valid","status":status.HTTP_400_BAD_REQUEST}
            except Exception as e :
                return {"message":"otp is verified","status":status.HTTP_400_BAD_REQUEST}
        elif "phone_no" in request.data:
            user = UserModel.objects.get(phone_no = request.data["phone_no"])
            enter_otp = request.data.get("otp")
            try:
                if user.otp == enter_otp:
                    user.otp_phone_no_verification = True
                    user.save()
                    return {"message":"otp in verified","status":status.HTTP_200_OK}
                else:
                    return {"message":"otp is not valid","status":status.HTTP_400_BAD_REQUEST}
            except Exception as e :
                return {"message":"otp is verified","status":status.HTTP_400_BAD_REQUEST}

    def log_in(self , request):
        
        if "email" in request.data:
            try:
                user_obj = UserModel.objects.get(email = request.data["email"])
                password = request.data.get("password")

                serializer = CreateClientSerializers(user_obj)
            
            except UserModel.DoesNotExist:    
                return {"message": "EMAIL_NOT_EXIST", "status": status.HTTP_400_BAD_REQUEST}

            if user_obj.role not in [1, 3]:
                return {"message": "NOT_ALLOWED", "status": status.HTTP_403_FORBIDDEN}

            check_pwd = check_password(password, user_obj.password) 
            if check_pwd:
                token = RefreshToken.for_user(user_obj)
                all_obj = {"data": serializer.data}
                all_obj["access_token"] = str(token.access_token)
                all_obj["refresh_token"] = str(token)
                return {"data": all_obj, 'message': "LOGIN_SUCCESSFULLY", "status": status.HTTP_200_OK}
            else:
                return {"message": "INVALID_CREDENTIAL", "status": status.HTTP_400_BAD_REQUEST}
        elif "phone_no" in request.data:
            try:
                user_obj = UserModel.objects.get(phone_no = request.data["phone_no"])    
                user_obj.otp = "123456"
                user_obj.save()
            except UserModel.DoesNotExist:
                return {"message":"Phone_No_Is_Not_Exist","status":status.HTTP_400_BAD_REQUEST}
            check_otp = request.data["otp"]
            if check_otp == user_obj.otp:
                serializer = CreateClientSerializers(user_obj)
                token = RefreshToken.for_user(user_obj)
                all_obj = {"data": serializer.data}
                all_obj["access_token"] = str(token.access_token)
                all_obj["refresh_token"] = str(token)
                return {"data": all_obj, 'message': "LOGIN_SUCCESSFULLY", "status": status.HTTP_200_OK}



    def resend_otp(self ,request):
        if "email" in request.data:
            try:
                User_obj = UserModel.objects.get(email = request.data["email"])
                otp_val = send_otp_via_mail(request.data["email"],self.create_username(request.data["email"]))
                User_obj.otp = otp_val
                User_obj.otp_verification = False
                User_obj.save()
                return {"message":"Otp Resend","status":status.HTTP_200_OK}
            except Exception as e:
                return {"message":str(e),"status":status.HTTP_400_BAD_REQUEST}
        elif "phone_in" in request.data:
            pass

            