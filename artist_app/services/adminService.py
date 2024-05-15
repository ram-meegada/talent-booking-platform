from shutil import ExecError
from artist_app.models.permissionModel import PermissionModel
from artist_app.utils import messages
from artist_app.models.talentCategoryModel import TalentCategoryModel
from artist_app.models.talentSubCategoryModel import TalentSubCategoryModel
from artist_app.serializers import adminSerializer
from artist_app.models.faqModel import FAQModel
from artist_app.models import TermAndConditionModel
from django.contrib.auth.hashers import check_password, make_password
from artist_app.serializers.adminSerializer import TermAndConditionsSerializer
from artist_app.models import UserModel
from rest_framework_simplejwt.tokens import RefreshToken
from artist_app.utils.sendOtp import send_otp_via_mail,make_otp,generate_password,\
                                     send_password_via_mail, generate_encoded_id
from artist_app.models import ManageAddressModel
from artist_app.models.talentDetailsModel import TalentDetailsModel
from artist_app.models.bookingTalentModel import BookingTalentModel
from artist_app.utils.customPagination import CustomPagination
from threading import Thread
from django.utils import timezone

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
                user = serializer.save(otp_email_verification=True, otp_phone_no_verification=True, profile_status=1, role=1)
                password = generate_password()
                user.set_password(password)
                send_password_via_mail(request.data["email"], password)
                user.save()
                address_location = request.data["address"]
                client_address = ManageAddressModel.objects.create(
                    address_location = request.data["address"],
                    user_id=user.id
                )
                client_address.save()
                return {"data": None, "data":serializer.data,"status":200}
            else:
                return {"data": serializer.errors, "message":messages.WENT_WRONG,"status":400}
        except Exception as e:
            return {"data": None, "message":messages.WENT_WRONG,"status":400}
    
    def get_custome_details_by_id(self, request, id):
        try:
            user = UserModel.objects.get(id=id)
        except UserModel.DoesNotExist:
            return {"data": None,"message":messages.WENT_WRONG,"status":400}
        if user:
            serializer = adminSerializer.GetClientByAdminSeriaizer(user)
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
                return {"data": serializer.errors, "message":messages.WENT_WRONG,"status":400}
        else:
            return {"data": None, "message":messages.WENT_WRONG,"status":400}

    def delete_customer_by_admin(self, request, id):
        try:
            user= UserModel.objects.get(id=id)
        except UserModel.DoesNotExist:
            return {"data": None, "message":messages.WENT_WRONG,"status":400}
        user.delete()
        return {"data": None, "message":messages.CUSTOMER_DELETE,"status":200}

    def get_all_customers(self, request):
        try:
            clients = UserModel.objects.filter(role=1)
            pagination_obj = CustomPagination()
            search_keys = ["first_name__icontains", "email__icontains"]
            result = pagination_obj.custom_pagination(request, search_keys, \
                                                      adminSerializer.GetAllClientsDetailsSerializer, clients)
            # serializer = adminSerializer.GetAllClientsDetailsSerializer(clients, many=True)
            return {
                        "data":result["response_object"],
                        "total_records": result["total_records"],
                        "start": result["start"],
                        "length": result["length"], 
                        "message":messages.USER_DETAILS_FETCHED, 
                        "status":200
                    }
        except Exception as e:
            print(e, 'eeeeeeeeeeeeeeee')
            return {"data": None, "message":messages.WENT_WRONG,"status":400}
        
    def bookings_of_customer(self, request, id):
        if request.data["key"] == 1:
            bookings = BookingTalentModel.objects.filter(client=id)
        elif request.data["key"] == 2:
            bookings = BookingTalentModel.objects.filter(client=id, status=2)
        elif request.data["key"] == 3:
            bookings = BookingTalentModel.objects.filter(client=id, status=1)
        elif request.data["key"] == 4:
            bookings = BookingTalentModel.objects.filter(client=id, status=4)
        elif request.data["key"] == 5:
            bookings = BookingTalentModel.objects.filter(client=id, status=3)
        pagination_obj = CustomPagination()
        search_keys = ["talent__email__icontains", "client__email__icontains"]
        result = pagination_obj.custom_pagination(request, search_keys, \
                                                    adminSerializer.BookingsSerializer, bookings)
        return {
                    "data":result["response_object"],
                    "total_records": result["total_records"],
                    "start": result["start"],
                    "length": result["length"], 
                    "message": "Artists fetched successfully", 
                    "status":200
                }    


# manage categories

    def get_all_categories(self, request):
        try:
            categories = TalentCategoryModel.objects.all()
            if request.data["name"]:
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
            if request.data["name"]:
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
        if request.data["verification_status"] == 0:
            users = UserModel.objects.filter(role=2, verification_status=0)
        elif request.data["verification_status"] == 1:
            users = UserModel.objects.filter(role=2, verification_status=1)
        elif request.data["verification_status"] == 2:
            users = UserModel.objects.filter(role=2, verification_status=2)
        users_id = [i.id for i in users]
        try:
            user = TalentDetailsModel.objects.filter(user__in=users_id)
            pagination_obj = CustomPagination()
            search_keys = ["first_name__icontains", "email__icontains"]
            result = pagination_obj.custom_pagination(request, search_keys, \
                                                      adminSerializer.GetArtistDetailsSerializers, user)
            return {
                        "data":result["response_object"],
                        "total_records": result["total_records"],
                        "start": result["start"],
                        "length": result["length"], 
                        "message": "Artists fetched successfully", 
                        "status":200
                    }
            # serializer = adminSerializer.GetArtistDetailsSerializers(user,many = True)
            # return {"data":serializer.data,"messages":messages.USER_DETAILS_FETCHED,"status":200}
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
            user_obj = UserModel.objects.get(id=id)
        except:
            return {"data":None,"messag":"User not found","status":400}
        try:
            user = TalentDetailsModel.objects.get(user_id=user_obj.id)
            serializer = adminSerializer.GetArtistDetailsByIdSerializer(user)
            return {"data":serializer.data,"messag":messages.USER_DETAILS_FETCHED,"status":200}
        except Exception as e:
            print(e)
            return {"data":None,"message":messages.WENT_WRONG,"status":400}

    def Update_artist_details_by_id(self, request, id):
        data = {"user_details": {}, "extra_details": {}}
        data["user_details"]["first_name"] = request.data["first_name"]
        data["user_details"]["last_name"] = request.data["last_name"]
        data["user_details"]["email"] = request.data["email"]
        data["user_details"]["phone_no"] = request.data["phone_no"]
        data["user_details"]["date_of_birth"] = request.data["date_of_birth"]
        data["user_details"]["experience"] = request.data["experience"]
        data["user_details"]["gender"] = request.data["gender"]
        data["user_details"]["country_code"] = request.data["country_code"]
        data["user_details"]["address"] = request.data["address"]
        data["user_details"]["city"] = request.data["city"]
        data["user_details"]["state"] = request.data["state"]
        data["user_details"]["country"] = request.data["country"]
        data["user_details"]["profile_picture"] = request.data["profile_picture"]

        data["extra_details"]["bust"] = request.data["bust"]
        data["extra_details"]["waist"] = request.data["waist"]
        data["extra_details"]["hips"] = request.data["hips"]
        data["extra_details"]["height_feet"] = request.data["height_feet"]
        data["extra_details"]["height_inches"] = request.data["height_inches"]
        data["extra_details"]["weight"] = request.data["weight"]
        data["extra_details"]["hair_color"] = request.data["hair_color"]
        data["extra_details"]["eye_color"] = request.data["eye_color"]
        data["extra_details"]["booking_method"] = request.data["booking_method"]
        data["extra_details"]["portfolio"] = [request.data["portfolio"]]
        data["extra_details"]["cover_photo"] = request.data["cover_photo"]
        data["extra_details"]["categories"] = request.data["categories"]
        data["extra_details"]["sub_categories"] = request.data["sub_categories"]
        user_obj = UserModel.objects.get(id=id)
        user = adminSerializer.CreateUpdateTalentUserByAdminSerializer(user_obj, data=data["user_details"])
        if user.is_valid():
            user_obj = user.save(otp_email_verification=True, otp_phone_no_verification=True, profile_status=1, role=2)

        model_obj = TalentDetailsModel.objects.get(user_id=user_obj.id)    
        model_details = adminSerializer.CreateModelStatusSerializer(model_obj, data=data["extra_details"])
        if model_details.is_valid():
            model_details.save(user_id=user_obj.id)
        return {"data":None, "message":"Artist updated successfully" ,"status":201}
    
    def bookings_of_artist(self, request, id):
        if request.data["key"] == 1:
            bookings = BookingTalentModel.objects.filter(talent=id)
        elif request.data["key"] == 2:
            bookings = BookingTalentModel.objects.filter(talent=id, status=2)
        elif request.data["key"] == 3:
            bookings = BookingTalentModel.objects.filter(talent=id, status=1)
        elif request.data["key"] == 4:
            bookings = BookingTalentModel.objects.filter(talent=id, status=4)
        elif request.data["key"] == 5:
            bookings = BookingTalentModel.objects.filter(talent=id, status=3)
        pagination_obj = CustomPagination()
        search_keys = ["talent__email__icontains", "client__email__icontains"]
        result = pagination_obj.custom_pagination(request, search_keys, \
                                                    adminSerializer.BookingsSerializer, bookings)
        return {
                    "data":result["response_object"],
                    "total_records": result["total_records"],
                    "start": result["start"],
                    "length": result["length"], 
                    "message": "Artists fetched successfully", 
                    "status":200
                }

    def add_artist_through_admin(self, request):
        data = {"user_details": {}, "extra_details": {}}
        data["user_details"]["name"] = request.data["name"]
        data["user_details"]["email"] = request.data["email"]
        data["user_details"]["phone_no"] = request.data["phone_no"]
        data["user_details"]["date_of_birth"] = request.data["date_of_birth"]
        data["user_details"]["experience"] = request.data["experience"]
        data["user_details"]["gender"] = request.data["gender"]
        data["user_details"]["country_code"] = request.data["country_code"]
        data["user_details"]["address"] = request.data["address"]
        data["user_details"]["city"] = request.data["city"]
        data["user_details"]["state"] = request.data["state"]
        data["user_details"]["country"] = request.data["country"]
        data["user_details"]["profile_picture"] = request.data["profile_picture"]

        data["extra_details"]["bust"] = request.data["bust"]
        data["extra_details"]["waist"] = request.data["waist"]
        data["extra_details"]["hips"] = request.data["hips"]
        data["extra_details"]["height_feet"] = request.data["height_feet"]
        data["extra_details"]["height_inches"] = request.data["height_inches"]
        data["extra_details"]["weight"] = request.data["weight"]
        data["extra_details"]["hair_color"] = request.data["hair_color"]
        data["extra_details"]["eye_color"] = request.data["eye_color"]
        data["extra_details"]["booking_method"] = request.data["booking_method"]
        data["extra_details"]["portfolio"] = [request.data["portfolio"]]
        data["extra_details"]["cover_photo"] = request.data["cover_photo"]
        data["extra_details"]["categories"] = request.data["categories"]
        data["extra_details"]["sub_categories"] = request.data["sub_categories"]

        user = adminSerializer.CreateUpdateTalentUserByAdminSerializer(data=data["user_details"])
        if user.is_valid():
            user_obj = user.save(otp_email_verification=True, otp_phone_no_verification=True, profile_status=1, role=2)
            password = generate_password()
            user_obj.set_password(password)
            Thread(target=send_password_via_mail, args=(data["user_details"]["email"], password)).start()
            user_obj.save()
        else:
            return {"data":user.errors, "message":"Something went wrong while adding artist" ,"status":400}

        model_details = adminSerializer.CreateModelStatusSerializer(data=data["extra_details"])
        if model_details.is_valid():
            model_details.save(user_id=user_obj.id)
        else:
            return {"data":model_details.errors, "message":"Something went wrong while adding artist" ,"status":400}
        return {"data":None, "message":"Artist added successfully" ,"status":201}

    # def  booking_details_listing(self, request):
    #     try:
    #         print("came here")
    #         if not request.data.get("status"):
    #             book = BookingTalentModel.objects.all()
    #             serializer = adminSerializer.BookingDetailsModuleSerializer(book)
    #         # elif request.data["status"]:
    #         book = BookingTalentModel.objects.filter(status=request.data["status"])
    #         serializer = adminSerializer.BookingDetailsModuleSerializer(book)

    #         return {"data":serializer.data,"messag":messages.USER_DETAILS_FETCHED,"status":200}
    #     except Exception as e:
    #         print(e)
    #         return {"data":None,"message":messages.WENT_WRONG,"status":400}

    def add_sub_admin(self, request):
        try:
            data = request.data
            user_serializer = adminSerializer.CreateSubAdminSerializer(data=data)
            if user_serializer.is_valid():
                user_data = user_serializer.save(profile_status=1)
                password=generate_password()
                user_data.set_password(password)
                user_data.save()
                password = generate_password()
                user_data.set_password(password)
                send_password_via_mail(request.data["email"], password)
                user_data.save()
                for i in request.data['permissions']:
                    role_serializer = adminSerializer.CreateRolePermissionSubAdminSerializer(data=i)
                    if role_serializer.is_valid():
                        save_role_permission = role_serializer.save(user_id = user_serializer.data['id'])
                        save_role_permission.save()
                    else:
                        return {'data':role_serializer.errors, 'status':400}    
                return {'data':request.data, 'message': "Sub admin created",'status':201}
            return {'data':user_serializer.errors,"message": "Something went wrong",'status':400}
        except Exception as e:
            return {"error": str(e),"message":"Something went wrong", "status": 400}
        
    def update_sub_admin_by_id(self, request, id):
        user = UserModel.objects.filter(id = id).first()
        if not user:
            return {'data':None, "message":"User not found", 'status':400}
        try:
            data = {**request.data}
            role_permission_data = data.pop("permissions")
            user_serializer = adminSerializer.CreateSubAdminSerializer(user, data=data)
            if user_serializer.is_valid():
                user_data = user_serializer.save()
                for i in role_permission_data:
                    try:
                        get_permission = PermissionModel.objects.get(id = i["id"])
                        role_serializer = adminSerializer.CreateRolePermissionSubAdminSerializer(get_permission, data=i)
                    except:
                        role_serializer = adminSerializer.CreateRolePermissionSubAdminSerializer(data=i)
                    if role_serializer.is_valid():
                        save_role_permission = role_serializer.save(user_id = user.id)
                    else:
                        return {'data':role_serializer.errors, 'status':400}    
                return {'data':request.data, 'message': "Sub admin updated successfully",'status':201}
            return {'data':user_serializer.errors,"message":"Something went wrong",'status':400}
        except Exception as e:
            return {"error": str(e),"message":"Internal server error", "status": 500}



    def get_all_sub_admin(self, request):
        sub_obj = UserModel.objects.filter(role=4).order_by("created_at")
        pagination_obj = CustomPagination()
        search_keys = ["email__icontains"]
        result = pagination_obj.custom_pagination(request, search_keys, adminSerializer.GetSubAdminSerializer, sub_obj)
        return{'data': result,'message': "Sub admins fetched successfully", 'status': 200}
    

    def get_sub_admin_by_id(self,request, id):
        try:
            sub_obj = UserModel.objects.get(pk=id)
        except UserModel.DoesNotExist:
            return {"data":None,"message":"User not found", "status": 400}
        serializer = adminSerializer.GetSubAdminSerializer(sub_obj)
        return {"data": serializer.data,"message": "Sub admin details fetched successfully", "status": 200}

    def delete_sub_admin_by_id(self,request, id):
        try:
            sub_obj = UserModel.objects.get(pk=id)
        except UserModel.DoesNotExist:
            return {"data":None,"message":"User not found", "status": 400}
        sub_obj.delete()
        return {"data": None, "message": "Sub admin deleted successfully", "status": 200}

    # def edit_sub_admin_status_by_id(self,request, sub_admin_id):
    #     try:
    #         sub_obj = User.objects.get(pk=sub_admin_id)
    #     except User.DoesNotExist:
    #         return {"data":None,"message":get_message(request, 'NOT_FOUND'), "status": status.HTTP_404_NOT_FOUND}
    #     serializer = adminSerializer.GeteditSubAdminSerializer(sub_obj,request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #     return {"data": serializer.data,"message":get_message(request, 'FETCH'), "status": status.HTTP_200_OK}
    
    def change_status_of_customer_by_admin(self, request, id):
        try:
            customer = UserModel.objects.get(pk=id)
            customer.is_active = request.data["is_active"]
            customer.save()
            return {"data":None,"message": "status updated successfully", "status": 200}
        except UserModel.DoesNotExist:
            return {"data":None,"message": "User not found", "status": 400}

    def verify_artist(self, request, id):
        VERIFICATION_STATUS = request.data["verification_status"]
        try:
            user = UserModel.objects.get(id=id)
            user.verification_status = request.data["verification_status"]
            user.save()
            if VERIFICATION_STATUS == 1:
                var = "approved"
            else:
                var = "rejected"    
            return {"data":None, "message": f"Artist {var} successfully", "status": 200}
        except UserModel.DoesNotExist:
            return {"data":None,"message": "User not found", "status": 400}
        
    def all_bookings(self, request):
        if request.data["key"] == 1:
            bookings = BookingTalentModel.objects.all()
        elif request.data["key"] == 2:
            bookings = BookingTalentModel.objects.filter(status=2)
        elif request.data["key"] == 3:
            bookings = BookingTalentModel.objects.filter(status=1)
        elif request.data["key"] == 4:
            bookings = BookingTalentModel.objects.filter(status=4)
        elif request.data["key"] == 5:
            bookings = BookingTalentModel.objects.filter(status=3)
        pagination_obj = CustomPagination()
        search_keys = ["talent__email__icontains", "client__email__icontains"]
        result = pagination_obj.custom_pagination(request, search_keys, \
                                                    adminSerializer.BookingsSerializer, bookings)
        return {
                    "data":result["response_object"],
                    "total_records": result["total_records"],
                    "start": result["start"],
                    "length": result["length"], 
                    "message": "Artists fetched successfully", 
                    "status":200
                }
    
    def booking_details_by_id(self, request, id):
        try:
            booking = BookingTalentModel.objects.get(id=id)
        except BookingTalentModel.DoesNotExist:
            return {"data": None, "message": "Record not found", "status": 400}
        serializer = adminSerializer.BookingsSerializer(booking)
        return {"data": serializer.data, "message": "Booking details fetched successfully", "status": 400}

###### Dashboard Module


    def kpi(self, request):
        kpi_s ={}
        kpi_s["Total_customers"]=UserModel.objects.filter(role=1, is_deleted=False).count()
        kpi_s["Total_booking"]=0
        kpi_s["Total_Artist"]=UserModel.objects.filter(role=2).count()
        return {"data":kpi_s,"message":messages.FETCH,"status":200}


    def client_chart(self, request):
        interval = request.data.get("interval")
        now = timezone.now()

        filtered_users = UserModel.objects.filter(role=1)
        if not interval:
            current_year = now.year
            start_date = timezone.datetime(current_year, 1, 1).date()
            end_date = now.date()
            date_counts = {}

            current_date = start_date
            while current_date <= end_date:
                count = filtered_users.filter(created_at__year=current_year, created_at__month=current_date.month).count()
                date_counts[current_date.strftime("%Y-%m")] = count
                current_date = current_date.replace(month=current_date.month + 1)
            
            # Organize data into label and value arrays
            labels = list(date_counts.keys())
            values = list(date_counts.values())
            
            return {"labels": labels, "values": values, 'message': messages.FETCH,"status": 200}


        if interval == "daily":
            start_date = timezone.datetime(now.year, now.month, 1).date()
            end_date = now.date()
            delta = timezone.timedelta(days=1)
            date_counts = {}

            current_date = start_date
            while current_date <= end_date:
                count = filtered_users.filter(created_at__date=current_date).count()
                date_counts[current_date.strftime("%Y-%m-%d")] = count
                current_date += delta
            
            # Organize data into label and value arrays
            labels = list(date_counts.keys())
            values = list(date_counts.values())

        elif interval == "weekly":
            last_4_weeks = now - timezone.timedelta(weeks=4)
            start_date = last_4_weeks.date()
            end_date = now.date()
            delta = timezone.timedelta(weeks=1)
            date_counts = {}

            current_date = start_date
            while current_date <= end_date:
                count = filtered_users.filter(created_at__date__range=[current_date, current_date + delta]).count()
                date_counts[current_date.strftime("%Y-%m-%d")] = count
                current_date += delta
            
            # Organize data into label and value arrays
            labels = list(date_counts.keys())
            values = list(date_counts.values())

        elif interval == "monthly":
            current_year = now.year
            start_date = timezone.datetime(current_year, 1, 1).date()
            end_date = now.date()
            date_counts = {}

            current_date = start_date
            while current_date <= end_date:
                count = filtered_users.filter(created_at__year=current_year, created_at__month=current_date.month).count()
                date_counts[current_date.strftime("%Y-%m")] = count
                current_date = current_date.replace(month=current_date.month + 1)
            
            # Organize data into label and value arrays
            labels = list(date_counts.keys())
            values = list(date_counts.values())

        else:
            return {"data":None,'message': messages.WENT_WRONG, "status":400}
        
        return {"labels": labels, "values": values, 'message': messages.FETCH,"status": 200}

    def artist_chart(self, request):
        interval = request.data.get("interval")
        now = timezone.now()

        filtered_users = UserModel.objects.filter(role=2)
        if not interval:
            current_year = now.year
            start_date = timezone.datetime(current_year, 1, 1).date()
            end_date = now.date()
            date_counts = {}

            current_date = start_date
            while current_date <= end_date:
                count = filtered_users.filter(created_at__year=current_year, created_at__month=current_date.month).count()
                date_counts[current_date.strftime("%Y-%m")] = count
                current_date = current_date.replace(month=current_date.month + 1)
            
            # Organize data into label and value arrays
            labels = list(date_counts.keys())
            values = list(date_counts.values())
            
            return {"labels": labels, "values": values, 'message': messages.FETCH,"status": 200}


        if interval == "daily":
            start_date = timezone.datetime(now.year, now.month, 1).date()
            end_date = now.date()
            delta = timezone.timedelta(days=1)
            date_counts = {}

            current_date = start_date
            while current_date <= end_date:
                count = filtered_users.filter(created_at__date=current_date).count()
                date_counts[current_date.strftime("%Y-%m-%d")] = count
                current_date += delta
            
            # Organize data into label and value arrays
            labels = list(date_counts.keys())
            values = list(date_counts.values())

        elif interval == "weekly":
            last_4_weeks = now - timezone.timedelta(weeks=4)
            start_date = last_4_weeks.date()
            end_date = now.date()
            delta = timezone.timedelta(weeks=1)
            date_counts = {}

            current_date = start_date
            while current_date <= end_date:
                count = filtered_users.filter(created_at__date__range=[current_date, current_date + delta]).count()
                date_counts[current_date.strftime("%Y-%m-%d")] = count
                current_date += delta
            
            # Organize data into label and value arrays
            labels = list(date_counts.keys())
            values = list(date_counts.values())

        elif interval == "monthly":
            current_year = now.year
            start_date = timezone.datetime(current_year, 1, 1).date()
            end_date = now.date()
            date_counts = {}

            current_date = start_date
            while current_date <= end_date:
                count = filtered_users.filter(created_at__year=current_year, created_at__month=current_date.month).count()
                date_counts[current_date.strftime("%Y-%m")] = count
                current_date = current_date.replace(month=current_date.month + 1)
            
            # Organize data into label and value arrays
            labels = list(date_counts.keys())
            values = list(date_counts.values())

        else:
            return {"data":None,'message': messages.WENT_WRONG, "status":400}
        
        return {"labels": labels, "values": values, 'message': messages.FETCH,"status": 200}

    def revenue_chart(self, request):
        pass

    def booking_chart(self, request):
        interval = request.data.get("interval")
        now = timezone.now()

        filtered_users = BookingTalentModel.objects.all()
        if not interval:
            current_year = now.year
            start_date = timezone.datetime(current_year, 1, 1).date()
            end_date = now.date()
            date_counts = {}

            current_date = start_date
            while current_date <= end_date:
                count = filtered_users.filter(created_at__year=current_year, created_at__month=current_date.month).count()
                date_counts[current_date.strftime("%Y-%m")] = count
                current_date = current_date.replace(month=current_date.month + 1)
            
            # Organize data into label and value arrays
            labels = list(date_counts.keys())
            values = list(date_counts.values())
            
            return {"labels": labels, "values": values, 'message': messages.FETCH,"status": 200}


        if interval == "daily":
            start_date = timezone.datetime(now.year, now.month, 1).date()
            end_date = now.date()
            delta = timezone.timedelta(days=1)
            date_counts = {}

            current_date = start_date
            while current_date <= end_date:
                count = filtered_users.filter(created_at__date=current_date).count()
                date_counts[current_date.strftime("%Y-%m-%d")] = count
                current_date += delta
            
            # Organize data into label and value arrays
            labels = list(date_counts.keys())
            values = list(date_counts.values())

        elif interval == "weekly":
            last_4_weeks = now - timezone.timedelta(weeks=4)
            start_date = last_4_weeks.date()
            end_date = now.date()
            delta = timezone.timedelta(weeks=1)
            date_counts = {}

            current_date = start_date
            while current_date <= end_date:
                count = filtered_users.filter(created_at__date__range=[current_date, current_date + delta]).count()
                date_counts[current_date.strftime("%Y-%m-%d")] = count
                current_date += delta
            
            # Organize data into label and value arrays
            labels = list(date_counts.keys())
            values = list(date_counts.values())

        elif interval == "monthly":
            current_year = now.year
            start_date = timezone.datetime(current_year, 1, 1).date()
            end_date = now.date()
            date_counts = {}

            current_date = start_date
            while current_date <= end_date:
                count = filtered_users.filter(created_at__year=current_year, created_at__month=current_date.month).count()
                date_counts[current_date.strftime("%Y-%m")] = count
                current_date = current_date.replace(month=current_date.month + 1)
            
            # Organize data into label and value arrays
            labels = list(date_counts.keys())
            values = list(date_counts.values())

        else:
            return {"data":None,'message': messages.WENT_WRONG, "status":400}
        
        return {"labels": labels, "values": values, 'message': messages.FETCH,"status": 200}

## Manage CMs

    # def add_privacy_poicy(self, request):
    #     try:
    #         serializer = adminSerializer.TermAndConditionsSerializer(data = request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return {"data":serializer.data,"message":messages.ADD,"status":200}
    #         else:
    #             return {"data":None,"message":messages.WENT_WRONG,"status":400}
    #     except Exception as e:
    #         return {"data":None,"message":messages.WENT_WRONG,"status":400}

    # def get_privacy_policy(self, request):
    #     pass

    # def add_customer_support(self, request):
    #     try:
    #         serializer = adminSerializer.CustomerSupport(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return {"data":serializer.data,"message":messages.ADD,"status":200}
    #         else:
    #             return {"data":None,"message":messages.WENT_WRONG,"status":400}
    #     except Exception as e:
    #         return {"data":None,"message":messages.WENT_WRONG,"status":400}


    # def get_customer_support(self, request):
    #     try:
    #         data = CustomerSupportModel.objects.all()
    #         serializer = adminSerializer.CustomerSupport(data,many = True)
    #         return {"data":serializer.data,"message":messages.ADD,"status":200}
    #     except Exception as e:
    #         return {"data":None,"message":messages.WENT_WRONG,"status":400}