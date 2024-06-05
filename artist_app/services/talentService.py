# from tkinter.messagebox import NO
from curses import start_color
import pytz
from threading import Thread
from artist_app.utils import messages
from artist_app.serializers import talentSerializer, adminSerializer, Clientserializer
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
from django.db import IntegrityError
from artist_app.serializers.Clientserializer import ShowBookingDetailsSerializer

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
            check_user_email = UserModel.objects.filter(email=request.data["email"]).first()
            if check_user_email and check_user_email.profile_status >= 1:
                return {"data": None, "message": "User with this email already exists", "status": 400}
            elif check_user_email and check_user_email.profile_status < 1:
                check_user_email.delete()
            user.email = request.data["email"]
            user.otp = otp
            Thread(target=send_otp_via_mail, args=[request.data["email"], otp]).start()
        elif "encoded_id" in request.data and "phone_no" in request.data:
            user = UserModel.objects.get(encoded_id = request.data["encoded_id"])
            check_user_mobile = UserModel.objects.filter(phone_no=request.data["phone_no"], country_code= request.data["country_code"]).first()
            if check_user_mobile and  check_user_mobile.profile_status >= 1:
                return {"data": None, "message": "User with this phone number already exists", "status": 400}
            elif check_user_mobile and check_user_mobile.profile_status < 1:
                check_user_mobile.delete()    
            user.phone_no = request.data["phone_no"]
            user.country_code = request.data["country_code"]
            user.otp = otp
        elif "email" in request.data:
            email = request.data["email"]
            if UserModel.objects.filter(email = email, profile_status__gte=1).first():
                return {"data": None, "message": "Email already taken", "status": 400}
            try:
                user = UserModel.objects.get(email = email, profile_status__lt=1)
            except UserModel.DoesNotExist:
                encoded_id = generate_encoded_id()
                user = UserModel.objects.create(email=email, encoded_id=encoded_id, role=2)
            Thread(target=send_otp_via_mail, args=[email, otp]).start()
            user.otp = otp
        elif "phone_no" in request.data:
            phone_no = request.data["phone_no"]
            if UserModel.objects.filter(phone_no = phone_no, country_code= request.data["country_code"], profile_status__gte=1).first():
                return {"data": None, "message": "Phone number already taken", "status": 400}
            try:
                user = UserModel.objects.get(phone_no=phone_no, country_code= request.data["country_code"])
            except UserModel.DoesNotExist:
                encoded_id = generate_encoded_id()
                user = UserModel.objects.create(phone_no=phone_no, country_code= request.data["country_code"], encoded_id=encoded_id, role=2)
            user.otp = otp
        user.otp_sent_time = datetime.now(tz=pytz.UTC)
        user.save()
        return {"data": "", "message": "Otp resent successfully", "status": 200}
    
    def login(self, request):
        give_token = False
        if "phone_no" in request.data:
            otp = make_otp()
            try:
                user = UserModel.objects.get(phone_no=request.data["phone_no"], country_code= request.data["country_code"])
                if not user.is_active:
                    return {"data":None,"message":messages.BLOCK,"status":400}
                user.otp_sent_time = datetime.now(tz=pytz.UTC)
                user.otp = otp
                user.save()
                return {"data": None, "message": "Otp sent to your phone number", "status": 200}
            except UserModel.DoesNotExist:
                return {"data": None, "message": "User with this phone number not found", "status": 400}
            except Exception as e:
                return {"data": str(e), "message": "Something went wrong", "status": 400}
        elif "email" in request.data:
            try:
                user = UserModel.objects.get(email = request.data["email"])
                if not user.is_active:
                    return {"data":None,"message":messages.BLOCK,"status":400}
            except UserModel.DoesNotExist:
                return {"data": None, "message": messages.EMAIL_NOT_FOUND, "status": 400}
            verify_password = check_password(request.data["password"], user.password)
            if verify_password:
                if user.profile_status >= 1:
                    give_token = True
                serializer = talentSerializer.GetTalentUserSerializer(user, context = {"give_token": give_token})
                return {"data": serializer.data, "message": "Logged In successfully", "status": 200}
            return {"data": None, "message": messages.WRONG_PASSWORD, "status": 400}    
    
    def edit_artist_details_by_token(self, request):
        data = {"user_details": {}, "extra_details": {}}
        data["user_details"]["first_name"] = request.data["first_name"]
        data["user_details"]["last_name"] = request.data["last_name"]
        data["user_details"]["email"] = request.data["email"]
        data["user_details"]["phone_no"] = request.data["phone_no"]
        data["user_details"]["country_code"] = request.data["country_code"]
        data["user_details"]["address"] = request.data["address"]
        data["user_details"]["profile_picture"] = request.data["profile_picture"]

        data["extra_details"]["bust"] = request.data["bust"]
        data["extra_details"]["waist"] = request.data["waist"]
        data["extra_details"]["hips"] = request.data["hips"]
        data["extra_details"]["height_feet"] = request.data["height_feet"]
        data["extra_details"]["height_inches"] = request.data["height_inches"]
        data["extra_details"]["weight"] = request.data["weight"]
        data["extra_details"]["hair_color"] = request.data["hair_color"] 
        data["extra_details"]["eye_color"] = request.data["eye_color"] 
        data["extra_details"]["portfolio"] = request.data["portfolio"]
        data["extra_details"]["cover_photo"] = request.data["cover_photo"]
        data["extra_details"]["categories"] = request.data["categories"]
        data["extra_details"]["sub_categories"] = request.data["sub_categories"]
        data["extra_details"]["services"] = request.data["services"]
        user_obj = UserModel.objects.get(id=request.user.id)
        user = adminSerializer.CreateUpdateTalentUserByAdminSerializer(user_obj, data=data["user_details"])
        NAME = request.data["first_name"] + " " + request.data["last_name"]
        if user.is_valid():
            user_obj = user.save(name=NAME)

        model_obj = TalentDetailsModel.objects.get(user_id=user_obj.id)    
        model_details = adminSerializer.CreateModelStatusSerializer(model_obj, data=data["extra_details"])
        if model_details.is_valid():
            model_details.save(user_id=user_obj.id)
        return {"data":None, "message":"Profile updated successfully" ,"status":200}

    def profile_setup_and_edit(self, request):
        """
            Update profile details like categories, model status, portfolio, booking method
        """
        try:
            print(request.data, '------payload-----')
            #fetch details record and user record
            user = UserModel.objects.get(id=request.user.id)
            talent_details, created = TalentDetailsModel.objects.get_or_create(user_id=request.user.id)
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
                tags = ""
                for i in request.data["category"]:
                    sub_categories += i["subcategory_id"]
                    tags += i["subcategory_text"]    
                tags_list = ["#"+i for i in tags.split(",")]
                talent_details.categories = categories
                talent_details.sub_categories = sub_categories
                talent_details.tags = tags_list
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
                else:
                    return {"data": serializer.errors, "message": "something went wrong", "status": 400}
            if portfolio_payload:
                talent_details.portfolio = portfolio_payload["portfolio"]
                talent_details.cover_photo_id = portfolio_payload["cover_photo"]
                talent_details.save()
                if user.profile_status == 3:
                    user.profile_status = 4
                    user.save()
            if booking_method_payload:
                user_booking_methods = [i["method"] for i in booking_method_payload]
                talent_details.booking_method = user_booking_methods
                talent_details.services = request.data["services"]
                talent_details.save()
                if user.profile_status == 4:
                    user.profile_status = 5
                    user.save()
            return {"data": request.data, "message": messages.DETAILS_UPDATED, "status": 200}
        except IntegrityError:
            return {"data": None, "message": "Category or sub category not found", "status": 400}
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
                response_dict["CategoryId"] = cat_obj.id
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
            upcoming_bookings = BookingTalentModel.objects.filter(date__gte=startdate, talent=request.user.id,status=1, track_booking__in=[1, 2])\
                                                                .exclude(date = startdate,time__lt = time).order_by("-created_at")
            serializer = talentSerializer.BookedClientDetailSerializers(upcoming_bookings, many=True)
            return {"data":serializer.data,"status":200}
        except Exception as e:
            return {"message":messages.WENT_WRONG,"status":400}

    def recent_offers_of_talent(self, request):
        try:
            startdate = datetime.today().date()
            time = datetime.now().time()
            upcoming_bookings = BookingTalentModel.objects.filter(date__gte=startdate, talent=request.user.id, 
                                                                  status=1).exclude(track_booking__in=[3,4,5,6]).exclude(date=startdate, time__lt=time).order_by("-created_at")
            serializer = talentSerializer.BookedClientDetailSerializers(upcoming_bookings, many=True)
            return {"data":serializer.data,"status":200}
        except Exception as e:
            return {"data": str(e), "message": messages.WENT_WRONG, "status": 400}

    def accepted_offers_of_talent(self, request):
        startdate = datetime.today().date()
        try:
            accepted_bookings = BookingTalentModel.objects.filter(date__gte=startdate, talent=request.user.id, 
                                                                  track_booking=3,  status=1).order_by("-created_at")
            serializer = talentSerializer.BookedClientDetailSerializers(accepted_bookings, many=True)
            return {"data":serializer.data,"status":200}
        except Exception as e:
            return {"data": str(e), "message": messages.WENT_WRONG, "status": 400}

    def past_client_booking_listing(self, request):
        try:
            enddate = datetime.today().date()  
            startdate = enddate - timedelta(days=6)
            time = datetime.now().time()
            past_bookings = BookingTalentModel.objects.filter(date__lte = enddate).exclude(date=enddate, time__gt = time).order_by("-created_at")
            serializer = talentSerializer.BookedClientDetailSerializers(past_bookings, many=True)
            return {"data":serializer.data,"status":200}
        except Exception as e:
            return {"message":messages.WENT_WRONG,"status":400}

    def cancelled_bookings(self,request):
        try:
            canceled_bookings = BookingTalentModel.objects.filter(status=3).order_by("-created_at")
            serializer = talentSerializer.BookedClientDetailSerializers(canceled_bookings, many=True)
            return {"data":serializer.data,"status":200}
        except Exception as e:
            return {"message":messages.WENT_WRONG,"status":400}
        
    def counter_offer(self, request):
        booking_id = request.data["booking_id"]
        try:
            booking = BookingTalentModel.objects.get(id=booking_id)
        except BookingTalentModel.DoesNotExist:
            return {"data": None, "message": "Record not found", "status": 400}
        booking.counter_offer_price = request.data["counter_offer_price"]
        booking.track_booking = 2
        booking.save()
        return {"data": None, "message": "Counter offer sent successfully", "status": 200}
    
    def accept_offer(self, request):
        booking_id = request.data["booking_id"]
        try:
            booking = BookingTalentModel.objects.get(id=booking_id)
        except BookingTalentModel.DoesNotExist:
            return {"data": None, "message": "Record not found", "status": 400}
        booking.track_booking = 3
        booking.final_price = booking.offer_price
        booking.save()
        self.add_details_in_slot(booking, request.user.id)
        return {"data": None, "message": "Offer accepted successfully", "status": 200}

    def decline_offer(self, request):
        booking_id = request.data["booking_id"]
        try:
            booking = BookingTalentModel.objects.get(id=booking_id)
        except BookingTalentModel.DoesNotExist:
            return {"data": None, "message": "Record not found", "status": 400}
        booking.track_booking = 4
        booking.status = 3
        booking.save()
        return {"data": None, "message": "Offer declined successfully", "status": 200}

    def add_details_in_slot(self, booking, talent_id):
        user_slots = OperationalSlotsModel.objects.filter(user=talent_id, 
                                                              date=booking.date).first()
        data = user_slots.slots
        check_time = str(booking.time)[:-3]
        check_slot_availability = self.find_time_in_slots(data, check_time)
        serializer = Clientserializer.ShowBookingDetailsSerializer(booking)
        serialized_data = serializer.data
        # print(serialized_data, '-------')
        for i in range(booking.duration):
            data[check_slot_availability]["booking_details"] = serialized_data
            check_slot_availability += 1
        user_slots.slots = data    
        user_slots.save()
        return None

    def find_time_in_slots(self, data, TIME_HOUR):
        for i in range(len(data)):
            if data[i]["slot_time"] == TIME_HOUR:
                return i
        return {}    

    
    def all_categories(self, request):
        categories = TalentCategoryModel.objects.values()
        return {"data": categories, "message": "Categories listing fetched successfully", "status": 200}


################################# slots #################################

    def add_slots(self, request):
        day_representations = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 
                               4: "Friday", 5: "Saturday", 6: "Sunday"}
        try:
            # week_day_num = required_date.weekday()
            # for i in range(week_day_num):
            #     required_date -= timedelta(days=1) 
            for i in range(0, 7):
                find_user_slot = OperationalSlotsModel.objects.filter(
                                                                        user=request.user.id, 
                                                                        date=request.data[i]["date"]
                                                                     ).first()
                payload_data = {
                    "user": request.user.id,
                    "day": day_representations[i],
                    "start" : request.data[i]["start"],
                    "end" : request.data[i]["end"],
                    "date" : request.data[i]["date"],
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
                        serializer.save(slots=slots)
                    else:
                        return {"data": serializer.errors, "message": "Something went wrong", "status": 400}
            return {"data": request.data, "message": "Slots updated successfully for this week", "status": 200}
        except Exception as error:
            return {"data": str(error), "message": "Something went wrong", "status": 400}

    def fetch_weekly_timings(self, request):
        day_representations = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, 
                               "Friday": 4, "Saturday": 5, "Sunday": 6}
        all_user_slot = OperationalSlotsModel.objects.filter(user=request.user.id)[:7]
        serializer = talentSerializer.SlotsSerializer(all_user_slot, many=True)
        slots = list(serializer.data)
        data = []
        for i in day_representations.keys():
            for j in slots:
                if j["day"] == i:
                    data.append(j)
                    break
        return {"data": data, "message": "Weekly timings fetched successfully", "status": 200}
    
    def generate_day_slots(self, start, end):
        data = []
        start_time = datetime.strptime(start, "%H:%M")
        end_time = datetime.strptime(end, "%H:%M")
        while start_time <= end_time:
            stripped_start_time = start_time.strftime("%H:%M")
            obj = {
                    "slot_time": stripped_start_time,
                    "booking_details": {}
                    }
            data.append(obj)
            start_time += timedelta(hours=1)
        return data    
    
    def get_slots_by_date(self, request):
        startdate = (datetime.today() - timedelta(days=1)).date()
        # print(startdate, '-------')
        date = request.data["date"]
        try:
            all_user_slot = OperationalSlotsModel.objects.get(user=request.user.id, date=date)
        except OperationalSlotsModel.DoesNotExist:
            return {"data": None, "message": "No slots found", "status": 400}

        slots = self.format_slots(all_user_slot.slots)
        total_offers = BookingTalentModel.objects.filter(talent=request.user.id)
        total_bookings = total_offers.filter(track_booking=3)
        new_bookings = total_offers.filter(track_booking=3, date__gte=startdate)
        return {"data": slots, "total_offers": total_offers.count(), "total_bookings": total_bookings.count(), "new_bookings": new_bookings.count(), "message": "Day slots fetched successfully", "status": 200}

    def format_slots(self, slots):
        for i in slots:
            if i["booking_details"].get("id"):
                try:
                    booking = BookingTalentModel.objects.get(id=i["booking_details"].get("id"))
                    i["booking_details"] = ShowBookingDetailsSerializer(booking).data
                except:
                    i["booking_details"] = {}
        return slots
                