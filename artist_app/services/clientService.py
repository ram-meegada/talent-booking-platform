from artist_app.serializers.Clientserializer import CreateClientSerializers,AddAddressDetailsSerializer,SubCategories,\
    TalentBasedOnSubcategories,TalentDetailsBasedOnSubcategories,BookingDetailsSerializer,ShowBookingDetailsSerializer,\
    GetUserSerializer, TalentBasicDetails, TalentListingDetailsSerializer,TalentDetailsBasedOnIOSSubcategories,GetClientDetails
from django.contrib.auth.hashers import check_password
from artist_app.utils.sendOtp import send_otp_via_mail
from rest_framework import status
from artist_app.models.userModel import UserModel
from rest_framework_simplejwt.tokens import RefreshToken
from artist_app.models.manageAddressModel import ManageAddressModel
from artist_app.utils import messages
from artist_app.models.talentCategoryModel import TalentCategoryModel
from artist_app.serializers.talentSerializer import TalentListingSerializer
from artist_app.models.talentDetailsModel import TalentDetailsModel
from artist_app.models.talentSubCategoryModel import TalentSubCategoryModel
from artist_app.models import TalentDetailsModel,BookingTalentModel
from django.db.models import Q
from threading import Thread
from datetime import datetime
import pytz
from artist_app.utils.sendOtp import make_otp, send_otp_via_mail, generate_encoded_id,generate_access_token
from artist_app.models.operationalSlotsModel import OperationalSlotsModel
from artist_app.serializers import adminSerializer, talentSerializer
from artist_app.models.uploadMediaModel import UploadMediaModel
from artist_app.serializers.uploadMediaSerializer import CreateUpdateUploadMediaSerializer
from artist_app.utils.choiceFields import FILTER_KEYS
from artist_app.serializers.Clientserializer import TalentBasicDetailsIOS

class ClientService():
    def user_signup(self, request):
        if "encoded_id" in request.data:
            user = UserModel.objects.get(encoded_id=request.data["encoded_id"])
            serializer = CreateClientSerializers(user, data=request.data)
        else:
            try:
                user = UserModel.objects.get(email=request.data["email"], profile_status__gte=1)
                return {"data": None, "message": "Email already taken", "status": 400}
            except:
                pass
            try:
                user = UserModel.objects.get(phone_no=request.data["phone_no"], profile_status__gte=1)
                return {"data": None, "message": "Phone number already taken", "status": 400}
            except:
                pass
            check_user = UserModel.objects.filter(Q(email=request.data["email"], profile_status__lt=1) | \
                                     Q(phone_no=request.data["phone_no"], profile_status__lt=1))
            if check_user:
                check_user.delete()    
            encoded_id = generate_encoded_id()
            request.data["encoded_id"] = encoded_id
            serializer = CreateClientSerializers(data=request.data)
        if serializer.is_valid():
            otp = make_otp()
            name = request.data["first_name"] + " " + request.data["last_name"]
            user_obj = serializer.save(role = 1, name=name)
            user_obj.set_password(request.data["password"])
            user_obj.save()
            if user_obj.otp_email_verification and user_obj.otp_phone_no_verification:
                user_obj.profile_status = 1
                user_obj.save()
                media_url = UploadMediaModel.objects.filter(id=serializer.data["profile_picture"]).first()
                data = {**serializer.data}
                data["profile_picture"] = CreateUpdateUploadMediaSerializer(media_url).data
                return {"data": data, "message": "Account created successfully", "status": 201}
            if not user_obj.otp_email_verification and user_obj.otp_phone_no_verification:
                user_obj.otp = otp
                user_obj.otp_sent_time = datetime.now(tz=pytz.UTC)
                Thread(target=send_otp_via_mail, args=[request.data["email"], otp]).start()
                return {"data": None, "message": "Please verify your email", "status": 200}
            if user_obj.otp_email_verification and not user_obj.otp_phone_no_verification:
                user_obj.otp = otp
                user_obj.otp_sent_time = datetime.now(tz=pytz.UTC)
                user_obj.save()
                return {"data": None, "message": "Please verify your phone number", "status": 200}
            if not user_obj.otp_email_verification and not user_obj.otp_phone_no_verification:
                user_obj.otp = otp
                user_obj.otp_sent_time = datetime.now(tz=pytz.UTC)
                user_obj.save()
                return {"data": None, "message": "Please verify your phone number and email", "status": 200}
        else:
            print(serializer.error_messages, '=----=======-=-=-=-')
            keys = list(serializer.errors.keys())
            return {"data": None, "message": f"{keys[0]}: {serializer.errors[keys[0]][0]}", "status": 400}
        
    def verify_otp(self, request):
        give_token = False
        now = datetime.now(tz=pytz.UTC)
        var = ""
        if "encoded_id" in request.data and "email" in request.data:
            var = "email"
            user = UserModel.objects.get(encoded_id=request.data["encoded_id"])
            if user.otp == request.data["otp"]:
                user.otp_email_verification = True
            else:
                return {"data": None, "message": messages.WRONG_OTP, "status": 400}
        if "encoded_id" in request.data and "phone_no" in request.data:
            var = "Phone number"
            user = UserModel.objects.get(encoded_id=request.data["encoded_id"])
            if user.otp == request.data["otp"]:
                user.otp_phone_no_verification = True
            else:
                return {"data": None, "message": messages.WRONG_OTP, "status": 400}
        if "phone_no" in request.data:
            try:
                user = UserModel.objects.get(phone_no=request.data["phone_no"])
            except UserModel.DoesNotExist:
                return {"data": None, "message": messages.MOBILE_NOT_FOUND, "status": 400}
            var = "Phone number"
            if int((now - user.otp_sent_time).total_seconds()) > 60:
                return {"data": None, "message": "Otp expired", "status": 400}
            if user.otp == request.data["otp"]:
                user.otp_phone_no_verification = True
                if user.otp_email_verification is False:
                    otp = make_otp()
                    Thread(target=send_otp_via_mail, args=[user.email, otp]).start()
                    user.otp = otp
                    user.otp_sent_time = datetime.now(tz=pytz.UTC)
            else:
                return {"data": None, "message": messages.WRONG_OTP, "status": 400}
        if "email" in request.data:
            email = request.data["email"]
            try:
                user = UserModel.objects.get(email = email)
            except UserModel.DoesNotExist:
                return {"data": None, "message": messages.EMAIL_NOT_FOUND, "status": 400}
            var = "Email"
            if user.otp == request.data["otp"]:
                user.otp_email_verification = True
                if user.otp_phone_no_verification is False:
                    otp = make_otp()
                    user.otp = otp
                    user.otp_sent_time = datetime.now(tz=pytz.UTC)
            else:
                return {"data": None, "message": messages.WRONG_OTP, "status": 400}
        user.save()
        if user.profile_status == 0 and user.otp_email_verification and user.otp_phone_no_verification:
            user.profile_status = 1
            user.save()
        serializer = GetUserSerializer(user, context = {"give_token": give_token})
        return {"data": serializer.data, "message": f"{var} verified successfully", "status": 200}    

    def resend_otp(self, request):
        encoded_id = ""
        otp = make_otp()
        if "encoded_id" in request.data and "email" in request.data:
            user = UserModel.objects.get(encoded_id = request.data["encoded_id"])
            if UserModel.objects.filter(email=request.data["email"]).first():
                return {"data": None, "message": "User with this email already exists", "status": 400}
            user.email = request.data["email"]
            user.otp = otp
            Thread(target=send_otp_via_mail, args=[request.data["email"], otp]).start()
        elif "encoded_id" in request.data and "phone_no" in request.data:
            user = UserModel.objects.get(encoded_id = request.data["encoded_id"])
            if UserModel.objects.filter(phone_no=request.data["phone_no"]).first():
                return {"data": None, "message": "User with this phone number already exists", "status": 400}
            user.phone_no = request.data["phone_no"]
            user.otp = otp
        elif "email" in request.data:
            email = request.data["email"]
            try:
                user = UserModel.objects.get(email = email)
            except UserModel.DoesNotExist:
                encoded_id = generate_encoded_id()
                user = UserModel.objects.create(email=email, encoded_id=encoded_id, role=1)
            Thread(target=send_otp_via_mail, args=[email, otp]).start()
            user.otp = otp
        elif "phone_no" in request.data:
            phone_no = request.data["phone_no"]
            try:
                user = UserModel.objects.get(phone_no=phone_no)
            except UserModel.DoesNotExist:
                encoded_id = generate_encoded_id()
                user = UserModel.objects.create(phone_no=phone_no, encoded_id=encoded_id, role=1)
            user.otp = otp
        user.otp_sent_time = datetime.now(tz=pytz.UTC)
        user.save()
        return {"data": {"encoded_id": user.encoded_id}, "message": "Otp resent successfully", "status": 200}
    
    def login(self, request):
        give_token = False
        if "phone_no" in request.data:
            otp = make_otp()
            try:
                user = UserModel.objects.get(phone_no=request.data["phone_no"])
                user.otp_sent_time = datetime.now(tz=pytz.UTC)
                user.otp = otp
                user.save()
                return {"data": None, "message": "Otp sent to your phone number", "status": 200}
            except UserModel.DoesNotExist:
                return {"data": None, "message": "User with this phone number not found", "status": 400}
        elif "email" in request.data:
            try:
                user = UserModel.objects.get(email = request.data["email"])
            except UserModel.DoesNotExist:
                return {"data": None, "message": messages.EMAIL_NOT_FOUND, "status": 400}
            verify_password = check_password(request.data["password"], user.password)
            if verify_password:
                if user.profile_status >= 1:
                    give_token = True
                serializer = GetUserSerializer(user, context = {"give_token": give_token})
                return {"data": serializer.data, "message": "Logged In successfully", "status": 200}
            return {"data": None, "message": messages.WRONG_PASSWORD, "status": 400}

    def edit_client_details_by_token(self, request):
        try:
            user_obj = UserModel.objects.get(id=request.user.id)
        except UserModel.DoesNotExist:
            return {"data":None, "message":"User not found" ,"status": 400}
        user_obj.first_name = request.data["first_name"]
        user_obj.last_name = request.data["last_name"]
        user_obj.profile_picture_id = request.data["profile_picture"]
        user_obj.city = request.data["city"]
        user_obj.address = request.data["address"]
        user_obj.state = request.data["state"]
        user_obj.country = request.data["country"]
        # user = adminSerializer.CreateUpdateTalentUserByAdminSerializer(user_obj, data=data["user_details"])
        NAME = request.data["first_name"] + " " + request.data["last_name"]
        user_obj.name = NAME
        user_obj.save()
        # if user.is_valid():
        #     user_obj = user.save(name=NAME)
        return {"data":None, "message":"Profile updated successfully" ,"status":200}


    def client_details_by_token(self, request):
        # user = TalentDetailsModel.objects.select_related("user").get(user_id=request.user.id)
        # serializer = talentSerializer.TalentUserDetailsByTokenSerializer(user)
        user = UserModel.objects.get(id=request.user.id)
        serializer = GetClientDetails(user)
        return {"data": serializer.data, "message": messages.USER_DETAILS_FETCHED, "status": 200}


############################################################################################################

    def create_username(self , email):
        s = ""
        for i in email:
            if i=='@':
                break
            else:
                s+=i 
        return s
    def signup(self , request):
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


    def verify_otp_service(self , request):
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
                print(all_obj,"akjhsdflkjahsdflkjh")
                return {"data": all_obj, 'message': "LOGIN_SUCCESSFULLY", "status": status.HTTP_200_OK}
            else:
                return {"message": "Invalid credentials", "status": status.HTTP_400_BAD_REQUEST}
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



    def resend_otp_service(self ,request):
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

#################################ADDRESS MANAGER##########################

    def show_all_address_with_token(self, request):
        data = ManageAddressModel.objects.filter(user_id = request.user.id)
        home_address = data.filter(address_type=1)
        print("home_address",home_address)
        home = AddAddressDetailsSerializer(home_address, many=True)

        work_address = data.filter(address_type=2)
        work=AddAddressDetailsSerializer(work_address, many=True)
        other_address = data.filter(address_type=3)
        other = AddAddressDetailsSerializer(other_address, many=True)
        req_data={}
        req_data["home"]=home.data
        req_data["work"]=work.data
        req_data["other"]=other.data
        return {"data":req_data, "status":status.HTTP_200_OK}

    def add_address_using_token(self, request):
        try:
            admin = UserModel.objects.get(id = request.user.id)
        except:
            return {"data": None, "message": "RECORD_NOT_FOUND", "status": status.HTTP_404_NOT_FOUND}
        try:
            serializer = AddAddressDetailsSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(user_id = admin.id)
                return {"data":serializer.data,"status":status.HTTP_200_OK}
            else:
                return {"message":messages.WENT_WRONG,"status":status.HTTP_400_BAD_REQUEST}
        except Exception as e:
            return {"message":str(e),"status":status.HTTP_400_BAD_REQUEST}
        
    def edit_address_details(self, request, id):
        try:
            address = ManageAddressModel.objects.get(id = id)
        except Exception as e:
            return {"message":str(e),"status":status.HTTP_400_BAD_REQUEST}
        try:
            serializer = AddAddressDetailsSerializer(address, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data":serializer.data ,"message":messages.UPDATE,"status":status.HTTP_200_OK}
            else:
                return {"message":messages.WENT_WRONG,"status":status.HTTP_400_BAD_REQUEST}
        except Exception as e:
            return {"message":str(e),"status":status.HTTP_400_BAD_REQUEST}

    def delete_address_details_by_id(self, request, id):
        try:
            address = ManageAddressModel.objects.get(id = id)
            address.delete()
            return {"message":messages.DELETE,"status":status.HTTP_200_OK}
        except Exception as e:
            return {"message":messages.WENT_WRONG,"status":status.HTTP_400_BAD_REQUEST}
    def get_addres_details_by_id(self, request, id):
        try:
            address = ManageAddressModel.objects.get(id = id)
            address_data = AddAddressDetailsSerializer(address)
            return {"data":address_data.data,"message":messages.DELETE,"status":status.HTTP_200_OK}
        except Exception as e:
            return {"message":messages.WENT_WRONG,"status":status.HTTP_400_BAD_REQUEST}



#--------------------------booking talent -----------------------------------

# listing all talent categories
    def All_categories(self, request):
        try:
            category = TalentCategoryModel.objects.all()
            serializer = TalentListingSerializer(category, many=True)
            return {"data":serializer.data,"status":200}
        except Exception as e:
            return {"message":messages.WENT_WRONG,"status":400}


    def all_sub_categories(self, request):
        try:
            sub_category = TalentSubCategoryModel.objects.filter(category=request.data["category"])
            serializer = SubCategories(sub_category, many=True)
            return {"data":serializer.data,"status":200}
        except Exception as e:
            return {"message":messages.WENT_WRONG,"status":400}


    def talents_details(self , request):
        try:
            val = request.data.get("sub_category")
            talent_details_ids = []
            for pk in val:
                talent = TalentDetailsModel.objects.filter(sub_categories__contains=[pk]).values("user")
                talent_details_ids += [i["user"] for i in talent]
            users = UserModel.objects.filter(id__in=talent_details_ids)
            serializer = TalentListingDetailsSerializer(users, many = True)
            return {"data":serializer.data, "message": "Artists fetched successfully", "status":200}
        except Exception as e:
            return {"data": str(e), "message": messages.WENT_WRONG,"status":400}

    def talents_details_for_booking(self , request, talent_id):
        try:
            user = UserModel.objects.get(id=talent_id)
            serializer = TalentListingDetailsSerializer(user)
            return {"data":serializer.data, "message": "Artist details fetched successfully", "status":200}
        except UserModel.DoesNotExist:
            return {"data": None, "message": "User not found","status": 200}
        except Exception as e:
            return {"data": str(e), "message": messages.WENT_WRONG,"status":400}

    def filter_talent(self, request):
        filters = Q()
        talent_details_ids = []
        if "search" in request.data:
            filters = Q(user__name__icontains=request.data["search"]["search_value"])
        if "filters" in request.data:
            for key, value in request.data["filters"].items():
                if key in FILTER_KEYS:
                    filters &= Q(**{FILTER_KEYS[key]: value})
        filtered_talent = TalentDetailsModel.objects.filter(filters)    
        talent_details_ids += [i.user_id for i in filtered_talent]
        users = UserModel.objects.filter(id__in=talent_details_ids)
        serializer = TalentListingDetailsSerializer(users, many = True)
        return {"data":serializer.data, "message": "Artists fetched based on filters", "status":200}

    def view_talent_all_details_by_id(self, request,id):
        try:
            talent = UserModel.objects.get(id=id)
            serializer = TalentBasicDetailsIOS(talent)
            other_details= TalentDetailsModel.objects.get(user_id=id)
            details = TalentDetailsBasedOnIOSSubcategories(other_details)
            dict={}
            l = []
            for i in details.data.values():
                l.append(str(i))

            dict["detials"]=serializer.data
            dict["other_detials"]=l

            return {"data": dict, "message": "Talent details fetched successfully", "status":200}
        except Exception as e:
            print(e)
            return {"message": messages.WENT_WRONG, "status":400}


#----------------------------booking proposal -------------------------------
    def book_talent(self , request):
        try:
            TIME_HOUR = request.data["time"]
            user_slots = OperationalSlotsModel.objects.filter(user=request.data["talent"], 
                                                              date=request.data["date"]).first()
            if not user_slots:
                return {"data": None, "message": "No slots found", "status": 400}
            # check_slot_availability = self.find_time_in_slots(user_slots.slots, TIME_HOUR)
            # if check_slot_availability == {}:
            #     return {"data": None, "message": "Desired slot not found", "status": 400}
            # elif check_slot_availability != {}:    
            #     slots = user_slots.slots
                # iteration = []
                # for i in range(request.data["duration"]):
                #     iteration += [TIME_HOUR]
                #     temp = int(TIME_HOUR) + 1
                #     TIME_HOUR = str(temp)
            serializer = BookingDetailsSerializer(data = request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save(status=1, track_booking=1)
                # for i in range(request.data["duration"]):
                #     slots[check_slot_availability]["booking_details"] = serializer.data
                #     check_slot_availability += 1
                # user_slots.slots = slots
                # user_slots.save()    
                return {"data": serializer.data, "message": "Booking request sent to artist successfully", "status":200}
            else:
                return{"message": serializer.errors, "status": 400}
        except Exception as e:
            return {"data": str(e), "message":messages.WENT_WRONG,"status":400}
        
    def find_time_in_slots(self, data, TIME_HOUR):
        for i in range(len(data)):
            if data[i]["slot_time"] == TIME_HOUR:
                return i
        return {}    
        
    def accept_reject_counter_offer(self, request, id):
        pass    

    def get_booking_details_by_id(self, request, id):
        try:
            talent_details = BookingTalentModel.objects.select_related("talent").get(id=id)
            serializer = ShowBookingDetailsSerializer(talent_details)
            return {"data":serializer.data,"status":200}
        except Exception as e:
            print(e)
            return {"message": str(e),"status":400}

    # def get_talent_based_on_filters(self, request):
    #     try:
    #         all_talent = UserModel.objects.filter(role=2, country=request.data["country"])
    #     except Exception as e:
    #         return {"messgae":messages.WENT_WRONG,"status":400}
            

    def talent_services(self, request, id):
        try:
            talent_obj = TalentDetailsModel.objects.get(user_id=id)
        except TalentDetailsModel.DoesNotExist:
            return {"data": None, "message": "Data not found", "status":400}
        return {"data": talent_obj.services, "message": "Services fetched successfully", "status": 200}

    def get_slots_by_date(self, request):
        date = request.data["date"]
        user = request.data["user"]
        try:
            all_user_slot = OperationalSlotsModel.objects.get(user=user, date=date)
        except OperationalSlotsModel.DoesNotExist:
            return {"data": [], "message": "No slots found", "status": 200}
        all_slots = all_user_slot.slots    
        for i in all_slots:
            if i["booking_details"] == {}:
                i["booking_details"]["is_available"] = True
            else:
                i["booking_details"]["is_available"] = False
        return {"data": all_slots, "message": "Day slots fetched successfully", "status": 200}

    def ongoing_bookings(self, request):
        try:
            ongoing_bookings = BookingTalentModel.objects.filter(client=request.user.id, status=1)
            serializer = talentSerializer.BookedClientDetailSerializers(ongoing_bookings, many=True)
            return {"data":serializer.data,"status":200}
        except Exception as e:
            return {"data": str(e), "message": messages.WENT_WRONG, "status": 400}

    def completed_bookings(self, request):
        try:
            completed_bookings = BookingTalentModel.objects.filter(client=request.user.id).\
                                                            filter(Q(status=2) | Q(track_booking=4))
            serializer = talentSerializer.BookedClientDetailSerializers(completed_bookings, many=True)
            return {"data": serializer.data, "message": "Completed bookings fetched successfully", "status": 200}
        except Exception as e:
            return {"data": str(e), "message": messages.WENT_WRONG, "status": 400}
        
    def mark_booking_completed(self, request, booking_id):
        try:
            booking = BookingTalentModel.objects.get(id=booking_id)
        except BookingTalentModel.DoesNotExist:
            return {"data": None, "message": "Record not found", "status": 400}
        booking.status = 2
        booking.save()
        return {"data": None, "message": "Booking marked as completed successfully", "status": 200}

    def cancelled_bookings(self, request):
        try:
            cancelled_bookings = BookingTalentModel.objects.filter(client=request.user.id, status=3, track_booking=4)
            serializer = talentSerializer.BookedClientDetailSerializers(cancelled_bookings, many=True)
            return {"data": serializer.data, "message": "Cancelled bookings fetched successfully", "status": 200}
        except Exception as e:
            return {"data": str(e), "message": messages.WENT_WRONG, "status": 400}
        
    def accept_or_reject_counter_offer(self, request, booking_id):
        try:
            booking = BookingTalentModel.objects.get(id=booking_id)
        except BookingTalentModel.DoesNotExist:
            return {"data": None, "message": "Record not found", "status": 400}
        if request.data["accept"] is True:
            booking.track_booking = 3
            booking.save()
            return {"data": "", "message": "Payment for booking successfully done.", "status": 200}
        else:
            booking.track_booking = 5
            booking.cancellation_reason = request.data["cancellation_reason"]
            booking.status = 3
            booking.save()
            return {"data": "", "message": "Booking declined successfully", "status": 200}