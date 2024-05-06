from threading import Thread

from artist_app.utils import messages
from artist_app.serializers import talentSerializer, adminSerializer
from artist_app.models.userModel import UserModel
from artist_app.models.talentDetailsModel import TalentDetailsModel
from artist_app.models.talentSubCategoryModel import TalentSubCategoryModel
from artist_app.utils.sendOtp import make_otp, send_otp_via_mail, generate_encoded_id
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from artist_app.models.bookingTalentModel import BookingTalentModel

class TalentService:
    def sign_up(self, request):
        ENCODED_ID = request.data["encoded_id"]
        try:
            user = UserModel.objects.get(encoded_id=ENCODED_ID)
            if user.otp_email_verification is False:
                return {"data": "", "message": messages.EMAIL_NOT_VERIFIED, "status": 400}
            elif user.otp_phone_no_verification is False:
                return {"data": "", "message": messages.MOBILE_NOT_VERIFIED, "status": 400}
        except UserModel.DoesNotExist:
            return {"data": "", "message": messages.EMAIL_OR_MOBILE_NOT_VERIFIED, "status": 400}
        serializer = talentSerializer.CreateUpdateTalentUserSerializer(user, data=request.data)
        if serializer.is_valid():
            HASHED_PASSWORD = make_password(request.data["password"])
            serializer.save(password=HASHED_PASSWORD, role=2, profile_status=1)
            return {"data": serializer.data, "message": messages.ACCOUNT_CREATED, "status": 201}
        else:
            first_error_key = list(serializer.errors.keys())[0]
            error = dict(serializer.errors)[first_error_key][0]
        return {"data": None, "message": f"{first_error_key}:- {error}", "status": 400}
    
    def user_login(self, request):
        give_token = True
        if "email" in request.data:
            #payload
            EMAIL = request.data.get("email")
            PASSWORD = request.data.get("password")
            try:
                user = UserModel.objects.get(email=EMAIL)
            except UserModel.DoesNotExist:
                return {"data": None, "message": messages.EMAIL_NOT_FOUND, "status": 400}
            verify_password = check_password(PASSWORD, user.password)
            if verify_password:
                if user.profile_status is None:
                    give_token = False
                serializer = talentSerializer.GetTalentUserSerializer(user, context={"give_token": give_token})
                return {"data": serializer.data, "message": messages.LOGGED_IN, "status": 200}
            else:
                return {"data": "", "message": messages.WRONG_PASSWORD, "status": 400}
        elif "phone_no" in request.data:
            #payload
            PHONE_NO = request.data.get("phone_no")
            COUNTRY_CODE = request.data.get("country_code")
            OTP = make_otp()
            try:
                give_token = False
                user = UserModel.objects.get(phone_no=PHONE_NO, country_code=COUNTRY_CODE)
                user.otp = OTP
                user.save()
            except UserModel.DoesNotExist:
                return {"data": None, "message": messages.MOBILE_NOT_FOUND, "status": 400}
            serializer = talentSerializer.GetTalentUserSerializer(user, context={"give_token": give_token})
            return {"data": serializer.data, "message": messages.OTP_SENT_TO_MOBILE, "status": 200}


    def send_otp_to_email_or_phone(self, request):
        OTP = make_otp()
        if "encoded_id" in request.data and "email" in request.data:
            ENCODED_ID = request.data["encoded_id"]
            EMAIL = request.data["email"]
            user = UserModel.objects.get(encoded_id=ENCODED_ID)
            user.email = EMAIL
            user.otp = OTP
            user.save()
            Thread(target=send_otp_via_mail, args=[EMAIL]).start()
            return {"data": "", "message": messages.OTP_SENT_TO_MAIL, "status": 200}
        elif "encoded_id" in request.data and "phone_no" in request.data:
            ENCODED_ID = request.data["encoded_id"]
            PHONE_NO = request.data["phone_no"]
            user = UserModel.objects.get(encoded_id=ENCODED_ID)
            user.phone_no = PHONE_NO
            user.otp = OTP
            user.save()
            return {"data": "", "message": messages.OTP_SENT_TO_MOBILE, "status": 200}
        elif "email" in request.data:
            ENCODED_ID = generate_encoded_id()
            EMAIL = request.data["email"]
            user = UserModel.objects.filter(email=EMAIL)
            if user.exclude(profile_status=None).first():
                return {"data": "", "message": messages.EMAIL_EXISTS, "status": 400}
            elif user.first():
                user = user.first()
            else:    
                user = UserModel.objects.create(email=EMAIL, encoded_id=ENCODED_ID)
            Thread(target=send_otp_via_mail, args=[EMAIL]).start()
            user.otp = OTP
            user.encoded_id = ENCODED_ID
            user.save()
            return {"data": {"encoded_id": ENCODED_ID}, "message": messages.OTP_SENT_TO_MAIL, "status": 200}
        elif "phone_no" in request.data:
            ENCODED_ID = generate_encoded_id()
            PHONE_NO = request.data["phone_no"]
            user = UserModel.objects.filter(phone_no=PHONE_NO)
            if user.exclude(profile_status=None).first():
                return {"data": "", "message": messages.PHONE_EXISTS, "status": 400}
            elif user.first():
                user = user.first()
            else:        
                user = UserModel.objects.create(phone_no=PHONE_NO, encoded_id=ENCODED_ID)
            user.otp = OTP
            user.encoded_id = ENCODED_ID
            user.save()
            return {"data": {"encoded_id": ENCODED_ID}, "message": messages.OTP_SENT_TO_MOBILE, "status": 200}

    def verify_mail_or_phone(self, request):
        if "email" in request.data:
            EMAIL = request.data["email"]
            user = UserModel.objects.filter(email=EMAIL).first()
            if not user:
                user = UserModel.objects.create(email=EMAIL)
            if user.otp == request.data["otp"]:
                user.otp_email_verification = True
                user.save()
                return {"data": {"encoded_id": user.encoded_id}, "message": messages.OTP_VERIFIED, "status": 200}
        elif "phone_no" in request.data:
            PHONE_NO = request.data["phone_no"]
            user = UserModel.objects.filter(phone_no=PHONE_NO).first()
            if user.profile_status >= 1:
                if user.otp == request.data["otp"]:
                    user.otp_phone_no_verification = True
                    user.save()
                    serializer = talentSerializer.GetTalentUserSerializer(user, context={"give_token": True})
                    return {"data": serializer.data, "message": messages.LOGGED_IN, "status": 200}
            else:
                if user.otp == request.data["otp"]:
                    user.otp_phone_no_verification = True
                    user.save()
                    return {"data": {"encoded_id": user.encoded_id}, "message": messages.OTP_VERIFIED, "status": 200}
            return {"data": "", "message": messages.WRONG_OTP, "status": 400}


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
                user.save()
            if categories_payload:
                talent_details.categories = categories_payload["categories"]
                talent_details.sub_categories = categories_payload["sub_categories"]
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
            return {"data": None, "message": messages.WENT_WRONG, "status": 400}

    def sub_category_listing(self, request):
        """
            Provide all sub categories based on categories selected by user
            Payload:- categories list
        """
        #payload
        categories = request.data["categories"]
        all_sub_categories = TalentSubCategoryModel.objects.filter(category__in=categories)
        serializer = adminSerializer.SubCategorySerializer(all_sub_categories, many=True)
        return {"data": serializer.data, "message": messages.SUB_CATEGORIES_LISTING, "status": 200}

    def log_out(self, request):
        pass

    def resend_otp(self, request):
        OTP = make_otp()
        if "phone_no" in request.data:
            user = UserModel.objects.get(phone_no=request.data["phone_no"])
            user.otp = OTP
            user.save()
            return {"data": "", "message": messages.OTP_SENT_TO_MOBILE, "status": 200}

    def user_details_by_token(self, request):
        user = TalentDetailsModel.objects.select_related("user").get(user_id=request.user.id)
        serializer = talentSerializer.TalentUserDetailsByTokenSerializer(user)
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



