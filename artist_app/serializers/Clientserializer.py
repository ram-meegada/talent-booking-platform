from time import timezone
from rest_framework import serializers
from artist_app.models.userModel import UserModel
from artist_app.models.manageAddressModel import ManageAddressModel
from artist_app.models.talentSubCategoryModel import TalentSubCategoryModel
from artist_app.models.talentCategoryModel import TalentCategoryModel
from artist_app.models.talentDetailsModel import TalentDetailsModel
from artist_app.serializers.uploadMediaSerializer import CreateUpdateUploadMediaSerializer
from artist_app.models.uploadMediaModel import UploadMediaModel
from artist_app.models.bookingTalentModel import BookingTalentModel
from artist_app.utils.sendOtp import generate_access_token
from artist_app.models.ratingsModel import ReviewAndRatingsModel
from django.db.models import Avg
from datetime import date

class CreateClientSerializers(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta:
        model = UserModel
        fields = ("id", "profile_picture", "first_name", "email", "last_name", "gender", "country_code", "phone_no",\
                  "date_of_birth", "experience", "address", "city", "state", "country", "encoded_id","token","otp_email_verification","otp_phone_no_verification")
    def get_token(self, obj):
        token = generate_access_token(obj)
        return token 

class GetClientDetails(serializers.ModelSerializer):
    profile_picture = CreateUpdateUploadMediaSerializer()
    class Meta:
        model = UserModel
        fields = ("id", "profile_picture", "first_name", "email", "last_name", "name", "gender", "country_code", "phone_no",\
                  "date_of_birth", "experience", "address", "city", "state", "country", "encoded_id","otp_email_verification","otp_phone_no_verification")
class GetUserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    profile_picture = CreateUpdateUploadMediaSerializer()
    class Meta:
        model = UserModel
        fields = ["id", "profile_picture", "first_name", "email", "last_name", "gender", "country_code", "phone_no",\
                  "date_of_birth", "experience", "address", "city", "state", "country", "otp_email_verification",\
                  "otp_phone_no_verification", "profile_status","encoded_id", "token"]
    def get_token(self, obj):
        if self.context.get("give_token"):
            token = generate_access_token(obj)
            return token
        else:
            return ""


class AddAddressDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManageAddressModel
        fields = ["id","address_location", "house_flat_block_no", "landmark", "street_no", "phone_no_manage_address", "address_type","city","state","country"]
class SubCategories(serializers.ModelSerializer):
    class Meta:
        model = TalentSubCategoryModel
        fields =["id", "name"]

class TalentBasedOnSubcategories(serializers.ModelSerializer):
    profile_picture = CreateUpdateUploadMediaSerializer()
    class Meta:
        model = TalentDetailsModel
        fields = fields = ('id', 'bust', 'waist', 'hips', 'height_feet', 'height_inches', 'weight', 'hair_color', 'eye_color', 'booking_method')

class TalentCategoryListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentCategoryModel
        fields = ["id", "name"]

class TalentDetailsBasedOnSubcategories(serializers.ModelSerializer):
    hair_color = serializers.SerializerMethodField()
    eye_color = serializers.SerializerMethodField()
    booking_method = serializers.SerializerMethodField()
    portfolio = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    sub_categories = serializers.SerializerMethodField()
    cover_photo = CreateUpdateUploadMediaSerializer()
    class Meta:
        model = TalentDetailsModel
        fields =["id","bust","waist","hips","height_feet","height_inches","weight","hair_color","eye_color",\
                 "booking_method","portfolio","cover_photo", "categories", "sub_categories"]
    def get_hair_color(self, obj):
        try:
            return obj.get_hair_color_display()
        except:
            return obj.hair_color
    def get_eye_color(self, obj):
        try:
            return obj.get_eye_color_display()
        except:
            return obj.eye_color
    def get_booking_method(self, obj):
        try:
            return obj.get_booking_method_display()
        except:
            return obj.booking_method
    def get_portfolio(self, obj):
        data = []
        try:
            for i in obj.portfolio:
                media = UploadMediaModel.objects.filter(id=i).first()
                if media:
                    data.append(CreateUpdateUploadMediaSerializer(media).data)
                else:
                    pass
            return data        
        except:
            return obj.portfolio
    def get_categories(self, obj):
        cat = TalentCategoryModel.objects.filter(id__in=obj.categories)
        serializer = TalentCategoryListingSerializer(cat, many=True)
        return serializer.data 
    def get_sub_categories(self, obj):
        sub_categories = TalentSubCategoryModel.objects.filter(id__in=obj.sub_categories)
        serializer = SubCategories(sub_categories, many=True)
        return serializer.data 


class TalentListingDetailsSerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    profile_picture = CreateUpdateUploadMediaSerializer()
    class Meta:
        model = UserModel
        fields = ["id", "first_name","last_name", "profile_picture", "email", \
                  "name", "address",\
                  "rating", "profile_status", "sub_categories", "categories"]
    def get_sub_categories(self, obj):
        details = TalentDetailsModel.objects.filter(user=obj.id).first()
        if details:
            sub_categories = TalentSubCategoryModel.objects.filter(id__in=details.sub_categories)
            serializer = SubCategories(sub_categories, many=True)
            return ", ".join([i["name"] for i in serializer.data])
        else:
            return []    
    def get_categories(self, obj):
        details = TalentDetailsModel.objects.filter(user=obj.id).first()
        if details:
            categories = TalentSubCategoryModel.objects.filter(id__in=details.categories)
            serializer = TalentCategoryListingSerializer(categories, many=True)
            return serializer.data
        else:
            return []    
    def get_rating(self, obj):
        pass    

class TalentDetailsBasedOnIOSOtherDetailsSubcategories(serializers.ModelSerializer):
    booking_method = serializers.SerializerMethodField()
    portfolio = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    sub_categories = serializers.SerializerMethodField()
    cover_photo = CreateUpdateUploadMediaSerializer()
    

    class Meta:
        model = TalentDetailsModel
        fields = ["booking_method","portfolio","cover_photo", "categories", "sub_categories"]
    def get_booking_method(self, obj):
        try:
            return obj.get_booking_method_display()
        except:
            return obj.booking_method
    def get_portfolio(self, obj):
        data = []
        try:
            for i in obj.portfolio:
                media = UploadMediaModel.objects.filter(id=i).first()
                if media:
                    data.append(CreateUpdateUploadMediaSerializer(media).data)
                else:
                    pass
            return data        
        except:
            return obj.portfolio
    def get_categories(self, obj):
        cat = TalentCategoryModel.objects.filter(id__in=obj.categories)
        serializer = TalentCategoryListingSerializer(cat, many=True)
        return serializer.data 
    def get_sub_categories(self, obj):
        sub_categories = TalentSubCategoryModel.objects.filter(id__in=obj.sub_categories)
        serializer = SubCategories(sub_categories, many=True)
        return serializer.data 

   




class TalentDetailsBasedOnIOSSubcategories(serializers.ModelSerializer):
    gender = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    hair_color = serializers.SerializerMethodField()
    eye_color = serializers.SerializerMethodField()
    height = serializers.SerializerMethodField()
    
    class Meta:
        model = TalentDetailsModel
        fields =["gender","age","city","hair_color","eye_color","height","weight","bust","waist","hips"]
    def get_hair_color(self, obj):
        try:
            return obj.get_hair_color_display()
        except:
            return obj.hair_color

    def get_height(self,obj):
        return str(obj.height_feet)+"'"+str(obj.height_inches)
    def get_gender(self, obj):
        try:
            return obj.user.get_gender_display()
        except:
            return obj.user.gender
    def get_age(self, obj):
        current_date =  date.today()
        user_date=obj.user.date_of_birth
        print(current_date,user_date,"aksjdhfalkshjdfk")
        age = (current_date-user_date).days
        age = age/365.25
        print(age,"sdjasjhdfaksh")
        return int(age)

    def get_city(self, obj):
        return obj.user.city

    def get_eye_color(self, obj):
        try:
            return obj.get_eye_color_display()
        except:
            return obj.eye_color
    

class TalentBasicDetailsIOS(serializers.ModelSerializer):
    profile_picture = CreateUpdateUploadMediaSerializer()
    professional_details = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()
    class Meta:
        model = UserModel
        fields = ["id", "first_name","last_name","profile_picture", "email", "experience","phone_no",\
                  "country_code","country", "name", "address",\
                  "state", "profile_status", "professional_details", "services", "average_rating"]
    def get_professional_details(self, obj):
        details = TalentDetailsModel.objects.filter(user=obj.id).first()
        if details:
            serializer = TalentDetailsBasedOnIOSOtherDetailsSubcategories(details)
            return serializer.data
        else:
            return {}    
    def get_services(self, obj):
        details = TalentDetailsModel.objects.filter(user=obj.id).first()
        if details:
            return details.services
        else:
            return []


class TalentBasicDetails(serializers.ModelSerializer):
    profile_picture = CreateUpdateUploadMediaSerializer()
    professional_details = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    class Meta:
        model = UserModel
        fields = ["id", "first_name","last_name","profile_picture", "email", "gender", "experience","phone_no",\
                  "country_code", "city","country", "name", "address",\
                  "state", "profile_status", "professional_details", "services", "average_rating"]
    def get_professional_details(self, obj):
        details = TalentDetailsModel.objects.filter(user=obj.id).first()
        if details:
            serializer = TalentDetailsBasedOnSubcategories(details)
            return serializer.data
        else:
            return {}    
    def get_gender(self, obj):
        try:
            return obj.get_gender_display()
        except:
            return obj.gender
    def get_services(self, obj):
        details = TalentDetailsModel.objects.filter(user=obj.id).first()
        if details:
            return details.services
        else:
            return []


class BookingProposalSerializers(serializers.ModelSerializer):
    pass




class BookingDetailsSerializer(serializers.ModelSerializer):
    client = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = BookingTalentModel
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    profile_picture = CreateUpdateUploadMediaSerializer()
    rating = serializers.SerializerMethodField()
    class Meta:
        model = UserModel
        fields = ["id", "first_name", "last_name", "name", "profile_picture", "rating"]
    def get_rating(self, obj):
        try:
            if obj.role == 2:
                avg_ratings = ReviewAndRatingsModel.objects.filter(talent=obj.id).aggregate(Avg("rating"))
                return avg_ratings["rating__avg"]
            return None    
        except Exception as err:
            return None

class ShowBookingDetailsSerializer(serializers.ModelSerializer):
    talent = UserSerializer()
    client = UserSerializer()
    subcategories = serializers.SerializerMethodField()
    address = AddAddressDetailsSerializer()
    status = serializers.SerializerMethodField()
    track_booking = serializers.SerializerMethodField()
    class Meta:
        model = BookingTalentModel
        fields = ["id", "talent", "client", "subcategories", "address", "date", "time", "duration", \
                  "status", "track_booking", "offer_price", "counter_offer_price", "comment", "services"]
    def get_subcategories(self, obj):
        try:
            user_sub_cat = TalentDetailsModel.objects.filter(user_id=obj.talent_id).first()
            sub_cat = TalentSubCategoryModel.objects.filter(id__in=user_sub_cat.sub_categories).values_list("name")
            result = ", ".join([i[0] for i in sub_cat])
            return result    
        except:
            return None
    def get_status(self, obj):
        try:
            return obj.get_status_display()
        except:
            return None
    def get_track_booking(self, obj):
        try:
            return obj.get_track_booking_display()
        except:
            return None
