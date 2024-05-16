import pytz
from threading import Thread
from artist_app.utils import messages
from artist_app.serializers import talentSerializer, adminSerializer
from artist_app.models.userModel import UserModel
from artist_app.models.uploadMediaModel import UploadMediaModel
from artist_app.models.talentDetailsModel import TalentDetailsModel
from artist_app.models.talentSubCategoryModel import TalentSubCategoryModel
from artist_app.utils.sendOtp import make_otp, send_otp_via_mail, generate_encoded_id
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from artist_app.models.bookingTalentModel import BookingTalentModel
from datetime import datetime, date
from artist_app.models.talentCategoryModel import TalentCategoryModel
from artist_app.models.operationalSlotsModel import OperationalSlotsModel
from artist_app.serializers.uploadMediaSerializer import CreateUpdateUploadMediaSerializer

class TalentService:    
    def user_signup(self, request):
        if "encoded_id" in request.data:
            user = UserModel.objects.get(encoded_id=request.data["encoded_id"])
            serializer = talentSerializer.CreateUpdateTalentUserSerializer(user, data=request.data)
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
            serializer = talentSerializer.CreateUpdateTalentUserSerializer(data=request.data)
        if serializer.is_valid():
            otp = make_otp()
            name = request.data["first_name"] + " " + request.data["last_name"]
            user_obj = serializer.save(role = 2, name=name)
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
            print(int((now - user.otp_sent_time).total_seconds()), '--------------')
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
                    give_token = True    
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
                    give_token = True    
            else:
                return {"data": None, "message": messages.WRONG_OTP, "status": 400}
        user.save()
        if user.profile_status == 0 and user.otp_email_verification and user.otp_phone_no_verification:
            user.profile_status = 1
            user.save()
        serializer = talentSerializer.GetTalentUserSerializer(user, context={"give_token": give_token})
        return {"data": serializer.data, "message": f"{var} verified successfully", "status": 200}

    def resend_otp(self, request):
        encoded_id = ""
        otp = make_otp()
        if "encoded_id" in request.data and "email" in request.data:
            user = UserModel.objects.get(encoded_id = request.data["encoded_id"])
            user.email = request.data["email"]
            user.otp = otp
            Thread(target=send_otp_via_mail, args=[request.data["email"], otp]).start()
        elif "encoded_id" in request.data and "phone_no" in request.data:
            user = UserModel.objects.get(encoded_id = request.data["encoded_id"])
            user.phone_no = request.data["phone_no"]
            user.otp = otp
        elif "email" in request.data:
            email = request.data["email"]
            try:
                user = UserModel.objects.get(email = email)
            except UserModel.DoesNotExist:
                encoded_id = generate_encoded_id()
                user = UserModel.objects.create(email=email, encoded_id=encoded_id, role=2)
            Thread(target=send_otp_via_mail, args=[email, otp]).start()
            user.otp = otp
        elif "phone_no" in request.data:
            phone_no = request.data["phone_no"]
            try:
                user = UserModel.objects.get(phone_no=phone_no)
            except UserModel.DoesNotExist:
                encoded_id = generate_encoded_id()
                user = UserModel.objects.create(phone_no=phone_no, encoded_id=encoded_id, role=2)
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
                serializer = talentSerializer.GetTalentUserSerializer(user, context = {"give_token": give_token})
                return {"data": serializer.data, "message": "Logged In successfully", "status": 200}
            return {"data": None, "message": messages.WRONG_PASSWORD, "status": 400}    
    


    def profile_setup_and_edit(self, request):
        """
            Update profile details like categories, model status, portfolio, booking method
        """
        try:
            #fetch details record and user record
            user = UserModel.objects.get(id=request.user.id)
            talent_details, created = TalentDetailsModel.objects.get_or_create(user_id=request.user.id)
            print(talent_details, '------')
            #payload keys
            user_payload = request.data.get("user")
            categories_payload = request.data.get("category")
            model_status_payload = request.data.get("model_status")
            portfolio_payload = request.data.get("portfolio")
            booking_method_payload = request.data.get("booking_method")
            if user_payload:
                user.profile_picture_id = user_payload["profile_picture"]
                user.first_name = user_payload["first_name"]
                user.last_name = user_payload["last_name"]
                user.address = user_payload["address"]
                user.name = user_payload["first_name"] + " " + user_payload["last_name"]
                user.save()
            if categories_payload:
                categories = [i["category_id"] for i in request.data["category"]]
                sub_categories = []
                for i in request.data["category"]:
                    if i["subcategory_id"]:
                        sub_categories += i["subcategory_id"]
                    else:
                        crt = TalentSubCategoryModel.objects.create(name=i["subcategory_text"], 
                                                                    category_id=i["category_id"])    
                # return
                talent_details.categories = categories
                talent_details.sub_categories = sub_categories
                talent_details.save()
                if user.profile_status == 1:
                    user.profile_status = 2
                    user.save()
            if model_status_payload:
                serializer = talentSerializer.CreateModelStatusSerializer(talent_details, data=model_status_payload)
                if serializer.is_valid():
                    serializer.save()
                    if user.profile_status == 2:
                        user.profile_status = 3
                        user.save()
            if portfolio_payload:
                talent_details.portfolio = portfolio_payload["portfolio"]
                talent_details.cover_photo_id = portfolio_payload["cover_photo"]
                talent_details.save()
                if user.profile_status == 3:
                    user.profile_status = 4
                    user.save()
            if booking_method_payload:
                talent_details.booking_method = booking_method_payload["method"]
                talent_details.save()
                if user.profile_status == 4:
                    user.profile_status = 5
                    user.save()
            return {"data": request.data, "message": messages.DETAILS_UPDATED, "status": 200}
        except Exception as error:
            return {"data": str(error), "message": messages.WENT_WRONG, "status": 400}

    def sub_category_listing(self, request):
        """
            Provide all sub categories based on categories selected by user
            Payload:- categories list
        """
        #payload
        categories = request.data["categories"]
        response = []
        for cat in categories:
            response_dict = {}
            cat_obj = TalentCategoryModel.objects.filter(id=cat).first()
            if cat_obj:
                all_sub_categories = TalentSubCategoryModel.objects.filter(category=cat_obj.id)
                serializer = adminSerializer.SubCategorySerializer(all_sub_categories, many=True)
                response_dict["Categoryname"] = cat_obj.name
                response_dict["CategoryData"] = serializer.data
                response.append(response_dict)
            else:
                pass
        return {"data": response, "message": messages.SUB_CATEGORIES_LISTING, "status": 200}
    
    def sub_category_listing_angular(self, request):
        all_sub_categories = TalentSubCategoryModel.objects.filter(category__in=request.data["categories"])
        serializer = adminSerializer.SubCategorySerializer(all_sub_categories, many=True)
        return {"data": serializer.data, "message": messages.SUB_CATEGORIES_LISTING, "status": 200}

    def log_out(self, request):
        pass

    def user_details_by_token(self, request):
        # user = TalentDetailsModel.objects.select_related("user").get(user_id=request.user.id)
        # serializer = talentSerializer.TalentUserDetailsByTokenSerializer(user)
        user = UserModel.objects.get(id=request.user.id)
        serializer = adminSerializer.TalentBasicDetails(user)
        return {"data": serializer.data, "message": messages.USER_DETAILS_FETCHED, "status": 200}
    # Booking details from talent

    def upcoming_clients_booking_listing(self, request):
        try:
            startdate = datetime.today().date()
            time = datetime.now().time()
            # upcoming_bookings = BookingTalentModel.objects.filter(
            #     Q(date__range=[startdate, enddate]) & Q(time__gt=time)
            # ).select_related('client')
            upcoming_bookings = BookingTalentModel.objects.filter(date__gte = startdate).exclude(date = startdate,time__lt = time)
            serializer = talentSerializer.BookedClientDetailSerializers(upcoming_bookings, many=True)
            return {"data":serializer.data,"status":200}
        except Exception as e:
            print(e)
            return {"message":messages.WENT_WRONG,"status":400}

    def past_client_booking_listing(self, request):
        try:
            enddate = datetime.today().date()  
            print(enddate, '-------')
            startdate = enddate - timedelta(days=6)
            time = datetime.now().time()
            print(datetime.now().time(),"1234567893456781234567812345678")
            past_bookings = BookingTalentModel.objects.filter(date__lte = enddate).exclude(date=enddate, time__gt = time)
            serializer = talentSerializer.BookedClientDetailSerializers(past_bookings, many=True)
            return {"data":serializer.data,"status":200}
        except Exception as e:
            print(e, 'eeeeee')
            return {"message":messages.WENT_WRONG,"status":400}

    def cancel_client_booking_list(self,request):
        try:
            canceled_bookings = BookingTalentModel.objects.filter(status=3)
            serializer = talentSerializer.BookedClientDetailSerializers(canceled_bookings,many = True)
            return {"data":serializer.data,"status":200}
        except Exception as e:
            return {"message":messages.WENT_WRONG,"status":400}
        
    
    def all_categories(self, request):
        categories = TalentCategoryModel.objects.values()
        return {"data": categories, "message": "Categories listing fetched successfully", "status": 200}


################################# slots #################################

    def add_slots(self, request):
        day_representations = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 
                               4: "Friday", 5: "Saturday", 6: "Sunday"}
        try:
            required_date = date.today()
            week_day_num = required_date.weekday()
            for i in range(week_day_num):
                required_date -= timedelta(days=1) 
            for i in range(0, 7):
                find_user_slot = OperationalSlotsModel.objects.filter(
                                                                        user=request.user.id, 
                                                                        date=required_date
                                                                     ).first()
                payload_data = {
                    "user": request.user.id,
                    "day": day_representations[i],
                    "start" : request.data[i]["start"],
                    "end" : request.data[i]["end"],
                    "date" : required_date,
                    "is_active": request.data[i]["is_active"]
                }
                slots = self.generate_day_slots(payload_data["start"], payload_data["end"])
                if find_user_slot:
                    serializer = talentSerializer.SlotsSerializer(find_user_slot, data=payload_data)
                    if serializer.is_valid():
                        serializer.save(slots=slots)
                    else:
                        return {"data": serializer.errors, "message": "Something went wrong", "status": 400}
                elif not find_user_slot:
                    serializer = talentSerializer.SlotsSerializer(data=payload_data)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return {"data": serializer.errors, "message": "Something went wrong", "status": 400}
                required_date += timedelta(days=1)
            return {"data": request.data, "message": "Slots updated successfully for this week", "status": 200}
        except Exception as error:
            return {"data": str(error), "message": "Something went wrong", "status": 400}

    def fetch_weekly_timings(self, request):
        all_user_slot = OperationalSlotsModel.objects.filter(user=request.user.id)
        serializer = talentSerializer.SlotsSerializer(all_user_slot, many=True)
        return {"data": serializer.data, "message": "Weekly timings fetched successfully", "status": 200}
    
    def generate_day_slots(self, start, end):
        data = {}
        start_time = datetime.strptime(start, "%H:%M")
        end_time = datetime.strptime(end, "%H:%M")
        while start_time <= end_time:
            stripped_start_time = start_time.strftime("%H")
            data[stripped_start_time] = {}
            start_time += timedelta(hours=1)
        return data    
    
    def get_slots_by_date(self, request):
        date = request.data["date"]
        try:
            all_user_slot = OperationalSlotsModel.objects.get(user=request.user.id, date=date)
        except OperationalSlotsModel.DoesNotExist:
            return {"data": None, "message": "No slots found", "status": 400}
        return {"data": all_user_slot.slots, "message": "Day slots fetched successfully", "status": 200}
