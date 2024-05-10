from unicodedata import category
from artist_app.utils import messages
from artist_app.models.talentCategoryModel import TalentCategoryModel
from artist_app.models.talentSubCategoryModel import TalentSubCategoryModel
from artist_app.serializers import adminSerializer
from artist_app.models.faqModel import FAQModel
from artist_app.models import TermAndConditionModel
from django.contrib.auth.hashers import check_password
from artist_app.serializers.adminSerializer import TermAndConditionsSerializer
from artist_app.models import UserModel
from rest_framework_simplejwt.tokens import RefreshToken
from artist_app.utils.sendOtp import send_otp_via_mail,make_otp,make_password,\
                                     send_password_via_mail, generate_encoded_id
from artist_app.models import ManageAddressModel
from artist_app.models.talentDetailsModel import TalentDetailsModel
from artist_app.models.bookingTalentModel import BookingTalentModel

class AdminService:
    def add_category(self, request):
        # name = request.data["name"]
        # talent_obj = TalentCategoryModel.objects.create(name=name)
        try:
            serializer =adminSerializer.CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data": request.data, "message": messages.CATEGORY_ADDED, "status": 201}
            else:
                return {"data": None, "message":messages.WENT_WRONG,"status":400}
        except Exception as e:
            print(e)
            return {"data": None, "message":messages.WENT_WRONG,"status":400}
    
    def add_sub_category(self, request):
        try:
            serializers = adminSerializer.SubCategorySerializer(data=request.data)
            print(serializers.is_valid())
            print(serializers.errors)
            if serializers.is_valid():
                serializers.save()
                return {"data": serializers.data, "message": messages.SUB_CATEGORY_ADDED, "status": 201}
            else:
                return {"data": None, "message":messages.WENT_WRONG,"status":400}
        except Exception as e:
            print(e)
            return {"data": None, "message":messages.WENT_WRONG,"status":400}
        # name = request.data["name"]
        # category_id = request.data["category"]
        # talent_sub_category = TalentSubCategoryModel.objects.create(
        #     name=name,
        #     category_id=category_id
        # )
    
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
            return {"data": None, "message":str(e),"status":400}

    def update_questions_answers(self, request, id):
        questions = FAQModel.objects.get(id=id)
        try:
            serializers = adminSerializer.FAQSerializer(questions,data = request.data)
            if serializers.is_valid():
                serializers.save()
                return {"data":serializers.data,"message":messages.UPDATE,"status":200}
            else:
                return {"data": None, "message":messages.WENT_WRONG,"status":400}
        except Exception as e:
            return {"message":str(e),"status":400}

    def delete_question_answer(self, request, id):
        try:
            question = FAQModel.objects.get(id=id)
            question.delete()
            return {"data": None, "message":messages.DELETE, "status":200}
        except Exception as e:
            return {"data": None, "message":str(e), "status":400}
    
    def get_all_questions_answers(self , request):
        try:
            questions = FAQModel.objects.all()
            serializers = adminSerializer.FAQSerializer(questions, many=True)
            return {"data":serializers.data,"message":messages.QUESTION_FETCHED,"status":200}
        except Exception as e:
            return {"data":None, "message":str(e),"status":400}

    #termsAndConditions
    def add_terms_and_conditions(self, request):
        try:
            serializer = adminSerializer.TermAndConditionsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data":serializer.data,"messages":messages.QUESTION_ADDED, "status":200}
            else:
                return {"data":None, "message":messages.WENT_WRONG, "status":400}
        except Exception as e:
            return {"data":None, "message":messages.WENT_WRONG, "status":400}

    def get_terms_and_conditions(self, request):
        try:
            terms = TermAndConditionModel.objects.all()
            serializer = adminSerializer.TermAndConditionsSerializer(terms, many=True)
            return {"data":serializer.data,"message":messages.TERMSANDCONDTIONS_FETCHED, "status":200}

        except Exception as e:
            return {"data":None,"message":messages.WENT_WRONG, "status":400}
    
    def update_terms_and_conditions(self, request, id):
        try:
            terms = TermAndConditionModel.objects.get(id=id)
            serializer = adminSerializer.TermAndConditionsSerializer(terms, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data":serializer.data,"message":messages.TERMSANDCONDTIONS_UPDATE, "status":200}
            else:
                return {"data":None ,"message":messages.WENT_WRONG, "status":400}
        except Exception as e:
            return {"data":None, "message":messages.WENT_WRONG, "status":400}
# admin onboarding
    def admin_login(self, request):
        try:
            email = request.data["email"]
            password = request.data["password"]
            try:
                user = UserModel.objects.get(email = email)
            except UserModel.DoesNotExist:
                return {"data":None ,"message": "User with this email doesnot exists","status":400}
            serializer = adminSerializer.ShowAdminDetialsByTokenSerializer(user)
            verify_password = check_password(password,user.password)
            if verify_password:
                token = RefreshToken.for_user(user)
                all_obj = dict(serializer.data).copy()
                all_obj["access_token"] = str(token.access_token)
                all_obj["refresh_token"] = str(token)
                return {"data": all_obj, 'message': messages.LOGGED_IN, "status": 200}
            else:
                return {"data":None,"message":"Incorrect password", "status":400}
        except Exception as e:
            return {"data":None,"message":messages.WENT_WRONG,"status":400}
    

    def verify_otp(self, request):
        try:
            email = request.data["email"]
            otp = request.data["otp"]
            try:
                user = UserModel.objects.get(email=email)
                ENCODED_ID = user.encoded_id
            except UserModel.DoesNotExist:
                return {"data":None,"message":messages.EMAIL_NOT_FOUND,"status":400}
            if user.otp == otp:
                user.otp_email_verification = True
                if user.encoded_id == "":
                    ENCODED_ID = generate_encoded_id()
                    user.encoded_id = ENCODED_ID
                user.save()
                return {"data":{"encoded_id": ENCODED_ID}, "message":messages.OTP_VERIFIED,"status":200}
            else:
                return {"data":None,"message":messages.WRONG_OTP,"status":400}
        except Exception as e:
            return {"data":None,"message":messages.WENT_WRONG,"status":400}

    def sent_otp(self, request):
        OTP = make_otp()
        email = request.data["email"]
        try:
            user = UserModel.objects.get(email=email)
            send_otp_via_mail(request.data["email"])
            user.otp = OTP
            user.save()
            return {"data":None,"message":messages.OTP_SENT_TO_MAIL,"status":200}
        except UserModel.DoesNotExist:
            return{"data":None,"message":messages.EMAIL_NOT_FOUND,"status":400}
    
    def forgot_password(self, request):
        encoded_id = request.data["encoded_id"]
        try:
            user = UserModel.objects.get(encoded_id=encoded_id)
            user.set_password(request.data["password"])
            user.save()
            return {"data":None,"message":messages.FORGOT_PASSWORD,"status":200}
        except UserModel.DoesNotExist:
            return {"data":None, "message":"Record not found", "status":400}
    
    def get_admin_details_by_token(self, request):
        try:
            user = UserModel.objects.get(id=request.user.id)
            serializer = adminSerializer.ShowAdminDetialsByTokenSerializer(user)
            return {"data":serializer.data,"message":messages.USER_DETAILS_FETCHED, "status":200}
        except Exception as e:
            return {"data":None,"message":messages.WENT_WRONG, "status":400}

    def update_admin_details_By_token(self, request):
        try:
            user = UserModel.objects.get(id=request.user.id)
            serializer = adminSerializer.updateAdminDetialsByTokenSerializer(user, data=request.data, context ={"profile_picture":request.data["profile_picture"]})
            if serializer.is_valid():
                serializer.save(profile_picture_id = request.data.get("profile_picture"))
                return {"data":serializer.data,"message":messages.UPDATE, "status":200}
            else:
                print(serializer.errors)
                return{"data":None,"message":messages.WENT_WRONG, "status":400}
        except Exception as e:
            print(e)
            return {"data":None,"message":messages.WENT_WRONG, "status":400}

    
    def change_password_by_token(self, request):
        try:
            user = UserModel.objects.get(id = request.user.id)
            old_password = request.data["old_password"]
            new_password = request.data["new_password"]
            verify_password = check_password(old_password,user.password)
            if verify_password:
                user.set_password(new_password)
                user.save()
                return {"data":None,"message":messages.CHANGE_PASSWORD,"status":200}
            else:
                return {"data":None,"message":messages.WENT_WRONG,"status":400}
        except Exception as e:
            return {"data":None,"message":messages.WENT_WRONG,"status":400}

    def logout(self, request):
        # token = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        # print(token, '-----')
        # token_obj = AccessToken(token)
        # BlacklistedToken(token=token_obj).save()
        # # token_obj.blacklist()
        # # jwt_token = JWTAuthentication().get_validated_token(request)
        # # AccessToken(token).blacklist()

        # return {"data": None, "message": messages.USER_LOGGED_OUT, "status": 200}
        # jwt_token = JWTAuthentication().get_validated_token(request)
        # token = str(jwt_token)
        # BlacklistedToken(token=token).save()
        return {"data": None, "message": messages.USER_LOGGED_OUT, "status": 200}
    
# manage customer module
    def add_new_customer(self, request):
        try:
            serializer = adminSerializer.AddNewClientByAdminSeriaizer(data = request.data)
            if serializer.is_valid():
                user = serializer.save()
                password = make_password()
                user.set_password(password)
                send_password_via_mail(request.data["email"])
                user.save()
                address_location = request.data["address"]
                client_address = ManageAddressModel.objects.create(
                    address_location = request.data["address"],
                    user_id=user.id
                )
                client_address.save()
                return {"data": None, "data":serializer.data,"status":200}
            else:
                return {"data": None, "message":messages.WENT_WRONG,"status":400}
        except Exception as e:
            return {"data": None, "message":messages.WENT_WRONG,"status":400}
    
    def get_custome_details_by_id(self, request, id):
        try:
            user = UserModel.objects.get(id=id)
        except UserModel.DoesNotExist:
            return {"data": None,"message":messages.WENT_WRONG,"status":400}
        if user:
            serializer = adminSerializer.AddNewClientByAdminSeriaizer(user)
            return {"data":serializer.data,"message":messages.USER_DETAILS_FETCHED,"status":200}
        else:
            return {"data": None, "message":messages.WENT_WRONG,"status":400}

    def edit_customer_by_admin(self,request,id):
        try:
            user = UserModel.objects.get(id = id)
        except UserModel.DoesNotExist:
            return {"data": None,"message":messages.WENT_WRONG,"status":400}
        if user:
            serializer = adminSerializer.AddNewClientByAdminSeriaizer(user, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data":serializer.data,"message":messages.USER_DETAILS_FETCHED,"status":200}
            else:
                return {"data": None, "message":messages.WENT_WRONG,"status":400}
        else:
            return {"data": None, "message":messages.WENT_WRONG,"status":400}

    def delete_customer_by_admin(self, request, id):
        try:
            user= UserModel.objects.get(id=id)
        except UserModel.DoesNotExist:
            return {"data": None, "message":messages.WENT_WRONG,"status":400}
        user.delete()
        return {"data": None, "message":messages.DELETE,"status":200}

    def get_all_customers(self, request):
        try:
            clients = UserModel.objects.filter(role=1)
            serializer = adminSerializer.GetAllClientsDetailsSerializer(clients, many=True)
            return {"data":serializer.data,"message":messages.USER_DETAILS_FETCHED,"status":200}
        except Exception as e:
            return {"data": None, "message":messages.WENT_WRONG,"status":400}


# manage categories

    def get_all_categories(self, request):
        try:
            categories = TalentCategoryModel.objects.all()
            if not request.data["name"]:
                category = categories.filter(name__icontains=request.data["name"])
                serializers = adminSerializer.GetAllCategoriesSerializers(category, many = True)
            else:
                serializers = adminSerializer.GetAllCategoriesSerializers(categories, many = True)
            return {"data":serializers.data,"message":messages.CATEGORIES_LISTING,"status":200}
        except Exception as e:
            return {"data": None, "message":messages.WENT_WRONG,"status":400}
    
    def get_categories_detail_by_id(self, request,id):
        try:
            category = TalentCategoryModel.objects.get(id=id)
            serializer  = adminSerializer.CategorySerializer(category)
            return {"data":serializer.data,"message":messages.CATEGORIES_LISTING,"status":200}
        except Exception as e:
            return {"data": None, "message":messages.WENT_WRONG,"status":400}
    
    def update_category_by_id(self, request,id):
        try:
            category = TalentCategoryModel.objects.get(id=id)
            serializer = adminSerializer.CategorySerializer(category,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data":serializer.data,"message":messages.UPDATE,"status":200}
            else:
                return {"data": None, "message":messages.WENT_WRONG,"status":400}
        except Exception as e:
            return {"data": None, "message":messages.WENT_WRONG,"status":400}

    def delete_category_by_id(self, request, id):
        try:
            category = TalentCategoryModel.objects.get(id=id)
            category.delete()
            return {"data": None, "message":messages.DELETE,"status":200}
        except Exception as e:
            return {"data": None, "message":messages.WENT_WRONG,"status":400}

    def get_all_subCategory(self, request):
        try:
            subcategory = TalentSubCategoryModel.objects.all()
            if not request.data["name"]:
                sub_category = subcategory.filter(name__icontains = request.data["name"],category = request.data["category"])
                serializer = adminSerializer.SubcategoryDetailsByCategoryIdSerializer(sub_category,many = True)
            else:
                sub_category = subcategory.filter(category = request.data["category"])
                serializer = adminSerializer.SubcategoryDetailsByCategoryIdSerializer(sub_category, many = True)
            return {"data":serializer.data,"message":messages.SUB_CATEGORIES_LISTING,"status":200}
        except Exception as e:
            return {"data": None, "message":messages.WENT_WRONG,"status":400}

        
    def get_subcategory_by_id(self, request, id):
        try:
            subcategory = TalentSubCategoryModel.objects.get(id=id)
            serializer = adminSerializer.SubcategoryDetailsByCategoryIdSerializer(subcategory)
            if serializer.is_valid():
               return {"data":serializer.data,"message":messages.SUB_CATEGORIES_LISTING,"status":200}
            else:
                return {"data":None,"message":messages.WENT_WRONG,"status":400}
            
        except Exception as e:
            return {"data":serializer.data,"message":messages.SUB_CATEGORIES_LISTING,"status":400}

    def update_subcategory_details(self, request, id):
        try:
            subcategory = TalentSubCategoryModel.objects.get(id=id)
            serializer = adminSerializer.SubcategoryDetailsByCategoryIdSerializer(subcategory,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data":serializer.data,"message":messages.UPDATE,"status":200}
            else:
                return {"data":None,"message":messages.WENT_WRONG,"status":400}
        except Exception as e:
            return {"data":None,"message":messages.WENT_WRONG,"status":400}

    def delete_subcategory_by_id(self, request, id):
        try:
            sub_category = TalentSubCategoryModel.objects.get(id=id)
            sub_category.delete()
            return {"data":None,"message":messages.DELETE,"status":200}
        except Exception as e:
            return {"data":None,"message":messages.WENT_WRONG,"status":400}
            
            

# manage Artist

    def get_all_artist_Details(self, request):
        try:
            user = TalentDetailsModel.objects.all()
            serializer = adminSerializer.GetArtistDetailsSerializers(user,many = True)
            return {"data":serializer.data,"messages":messages.USER_DETAILS_FETCHED,"status":200}
        except Exception as e:
            print(e)
            return {"data":None,"message":messages.WENT_WRONG,"status":400}
    

    def delete_artist_by_id(self, request, id):
        try:
            artist = UserModel.objects.get(id=id)
            artist.delete()
            return {"data":None,"message":messages.DELETE,"status":200}
        except Exception as e:
            return{"data":None,"message":messages.WENT_WRONG,"status":400}

    def get_artist_by_id(self, request, id):
        try:
            user = TalentDetailsModel.objects.get(id=id)
            serializer = adminSerializer.GetArtistDetailsByIdSerializer(user)
            return {"data":serializer.data,"messag":messages.USER_DETAILS_FETCHED,"status":200}
        except Exception as e:
            print(e)
            return {"data":None,"message":messages.WENT_WRONG,"status":400}

    def Update_artist_details_by_id(self, request, id):
       pass

    def add_artist_through_admin(self, request):
        pass

    # def  booking_details_listing(self, request):
    #     book = BookingTalentModel.objects.all()
    #     if not request.data["book_status"]:
    #         serializer = adminSerializer.
    #         return {"data":serializer.data,"messag":messages.USER_DETAILS_FETCHED,"status":200}



