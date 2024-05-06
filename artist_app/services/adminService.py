from artist_app.utils import messages
from artist_app.models.talentCategoryModel import TalentCategoryModel
from artist_app.models.talentSubCategoryModel import TalentSubCategoryModel
from artist_app.serializers import adminSerializer
from artist_app.models.faqModel import FAQModel
from artist_app.models import TermAndConditionModel
from django.contrib.auth.hashers import check_password
from artist_app.serializers.adminSerializer import TermAndConditionsSerializer,AdminLoginserializer
from artist_app.models import UserModel
from rest_framework_simplejwt.tokens import RefreshToken

from artist_app.utils.sendOtp import send_otp_via_mail,make_otp,make_password,send_password_via_mail

class AdminService:
    def add_category(self, request):
        name = request.data["name"]
        talent_obj = TalentCategoryModel.objects.create(name=name)
        return {"data": request.data, "message": messages.CATEGORY_ADDED, "status": 201}
    
    def add_sub_category(self, request):
        name = request.data["name"]
        category_id = request.data["category"]
        talent_sub_category = TalentSubCategoryModel.objects.create(
            name=name,
            category_id=category_id
        )
        return {"data": request.data, "message": messages.SUB_CATEGORY_ADDED, "status": 201}
    
    def subcategory_listing_by_category_id(self, request):
        sub_categories = TalentSubCategoryModel.objects.filter(category = request.data["category"])
        serializer = adminSerializer.SubCategorySerializer(sub_categories, many=True)
        return {"data": serializer.data, "message": messages.SUB_CATEGORIES_LISTING, "status": 200}
    
    def add_questions_answers(self, request):
        serializers = adminSerializer.FAQSerializer(data=request.data)
        try:
            if serializers.is_valid():
                serializers.save()
            return {"data":serializers.data,"message":messages.ADD,"status":200}
        except Exception as e:
            return {"message":str(e),"status":400}

    def update_questions_answers(self, request, id):
        questions = FAQModel.objects.get(id=id)
        try:
            serializers = adminSerializer.FAQSerializer(questions,data = request.data)
            if serializers.is_valid():
                serializers.save()
                return {"data":serializers.data,"message":messages.UPDATE,"status":200}
            else:
                return {"message":messages.WENT_WRONG,"status":400}
        except Exception as e:
            return {"message":str(e),"status":400}

    def delete_question_answer(self, request, id):
        try:
            question = FAQModel.objects.get(id=id)
            question.delete()
            return {"message":messages.DELETE, "status":200}
        except Exception as e:
            return {"message":str(e), "status":400}
    
    def get_all_questions_answers(self , request):
        try:
            questions = FAQModel.objects.all()
            serializers = adminSerializer.FAQSerializer(questions, many=True)
            return {"data":serializers.data,"status":200}
        except Exception as e:
            return {"message":str(e),"status":400}

    #termsAndConditions
    def add_terms_and_conditions(self, request):
        try:
            serializer = adminSerializer.TermAndConditionsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data":serializer.data, "status":200}
            else:
                return {"message":messages.WENT_WRONG, "status":400}
        except Exception as e:
            return {"message":messages.WENT_WRONG, "status":400}

    def get_terms_and_conditions(self, request):
        try:
            terms = TermAndConditionModel.objects.all()
            serializer = adminSerializer.TermAndConditionsSerializer(terms, many=True)
            return {"data":serializer.data, "status":200}

        except Exception as e:
            return {"message":messages.WENT_WRONG, "status":400}
    
    def update_terms_and_conditions(self, request, id):
        try:
            terms = TermAndConditionModel.objects.get(id=id)
            serializer = adminSerializer.TermAndConditionsSerializer(terms, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data":serializer.data, "status":200}
            else:
                return {"message":messages.WENT_WRONG, "status":400}
        except Exception as e:
            return {"message":messages.WENT_WRONG, "status":400}
# admin onboarding
    def admin_login(self, request):
        try:
            email = request.data["email"]
            password = request.data["password"]
            try:
                user = UserModel.objects.get(email = email)

            except UserModel.DoesNotExist:
                return {"message":messages.WENT_WRONG,"status":400}
            serializer = adminSerializer.AdminLoginserializer(user)
            verify_password = check_password(password,user.password)
            if verify_password:
                token = RefreshToken.for_user(user)
                all_obj = {"data": serializer.data}
                all_obj["access_token"] = str(token.access_token)
                all_obj["refresh_token"] = str(token)
                return {"data": all_obj, 'message': messages.LOGGED_IN, "status": 200}
            else:
                return {"message":messages.WENT_WRONG,"status":400}
        except Exception as e:
            print(e)
            return {"message":messages.WENT_WRONG,"status":400}
    

    def verify_otp(self, request):
        try:
            email = request.data["email"]
            otp = request.data["otp"]
            try:
                user = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist:
                return {"message":messages.EMAIL_NOT_FOUND,"status":400}
            if user.otp == otp:
                user.otp_email_verification = True
                user.save()
                return {"message":messages.OTP_VERIFIED,"status":200}
            else:
                return {"message":messages.WRONG_OTP,"status":400}
        except Exception as e:
            return {"message":messages.WENT_WRONG,"status":400}

    def sent_otp(self, request):
        OTP = make_otp()
        email = request.data["email"]
        try:
            user = UserModel.objects.get(email=email)
            send_otp_via_mail(request.data["email"])
            user.otp = OTP
            user.save()
            return {"message":messages.OTP_SENT_TO_MAIL,"status":200}
        except UserModel.DoesNotExist:
            return{"message":messages.EMAIL_NOT_FOUND,"status":400}
    
    def forgot_password(self, request):
        email = request.data["email"]
        try:
            user = UserModel.objects.get(email=email)
            user.set_password(request.data["password"])
            user.save()
            return {"message":messages.FORGOT_PASSWORD,"status":200}
        except Exception as e:
            return {"message":messages.WENT_WRONG,"status":400}
    
# manage customer module
    def add_new_customer(self, request):
        try:
            serializer = adminSerializer.AddNewClientByAdminSeriaizer(data = request.data)
            print(serializer.is_valid())
            print(serializer.errors)
            if serializer.is_valid():
                print("1234567823456734567")
                user = serializer.save()
                password = make_password()
                print(password)
                user.set_password(password)
                print(user.set_password(password))
                send_password_via_mail(request.data["email"])
                user.save()
                print("hello world")
                serializers = adminSerializer.ManageAddressByAdminSerializer(data= request.data["address"])
                print(serializers.is_valid,"haksdjhfakjshdfalkjsdfhlaksjdf23456783456")
                print(serializers.errors)
                if serializers.is_valid():
                    serializers.save(user=user)
                return {"data":serializer.data,"status":200}
            else:
                return {"message":messages.WENT_WRONG,"status":400}
        except Exception as e:
            print(e)
            return {"message":messages.WENT_WRONG,"status":400}

    def edit_customer_by_admin(self,request,id):
        try:
            user = UserModel.objects.get(id = id)
        except UserModel.DoesNotExist:
            return {"message":messages.WENT_WRONG,"status":400}
        if user:
            serializer = adminSerializer.AddNewClientByAdminSeriaizer(user, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data":serializer.data,"status":200}
            else:
                return {"message":messages.WENT_WRONG,"status":400}
        else:
            return {"message":messages.WENT_WRONG,"status":400}

    def delete_customer_by_admin(self, request, id):
        try:
            user= UserModel.objects.get(id=id)
        except UserModel.DoesNotExist:
            return {"message":messages.WENT_WRONG,"status":400}
        user.delete()
        return {"message":messages.DELETE,"status":200}

    def get_all_customers(self, request):
        try:
            clients = UserModel.objects.filter(role=1)
            print(clients,"dfhakljshdflakjhs")
            serializer = adminSerializer.GetAllClientsDetailsSerializer(clients)
            return {"data":serializer.data,"status":200}
        except Exception as e:
            print(e)
            return {"message":messages.WENT_WRONG,"status":400}

    







