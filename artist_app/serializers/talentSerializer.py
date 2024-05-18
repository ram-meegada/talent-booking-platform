from rest_framework import serializers
from artist_app.utils.sendOtp import generate_access_token
from artist_app.models.operationalSlotsModel import OperationalSlotsModel
from artist_app.models.userModel import UserModel
from artist_app.models.talentDetailsModel import TalentDetailsModel
from artist_app.models.talentCategoryModel import TalentCategoryModel
from artist_app.models.talentSubCategoryModel import TalentSubCategoryModel
from artist_app.models.bookingTalentModel import BookingTalentModel
from artist_app.serializers.uploadMediaSerializer import CreateUpdateUploadMediaSerializer
from artist_app.serializers.adminSerializer import CategorySerializer, SubCategorySerializer

class TalentListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentCategoryModel
        fields = ["id", "name"]

class CreateUpdateTalentUserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta:
        model = UserModel
        fields = ("id", "profile_picture", "first_name", "email", "last_name", "gender", "country_code", "phone_no",\
                  "date_of_birth", "experience", "address", "city", "state", "country", "token", 'profile_status')
    def get_token(self, obj):
        token = generate_access_token(obj)
        return token    
    
class GetTalentUserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    profile_picture = CreateUpdateUploadMediaSerializer()
    class Meta:
        model = UserModel
        fields = ["id", "profile_picture", "first_name", "email", "last_name", "gender", "country_code", "phone_no",\
                  "date_of_birth", "experience", "address", "city", "state", "country", "otp_email_verification",\
                  "otp_phone_no_verification", "profile_status", "encoded_id", "token"]
    def get_token(self, obj):
        if self.context.get("give_token"):
            token = generate_access_token(obj)
            return token
        else:
            return ""

class CreateModelStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentDetailsModel
        fields = ('id', 'bust', 'waist', 'hips', 'height_feet', 'height_inches', 'weight', 'hair_color',\
                   'eye_color', 'booking_method')
        
class TalentUserDetailsByTokenSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone_no = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()
    hair_color = serializers.SerializerMethodField()
    eye_color = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    sub_categories = serializers.SerializerMethodField()
    class Meta:
        model = TalentDetailsModel
        fields = ('id', 'full_name', 'profile_picture', 'email', 'phone_no', 'address', \
                  'weight', 'hair_color', 'eye_color', 'categories', 'sub_categories')

    def get_full_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name
    def get_profile_picture(self, obj):
        try:
            serializer = CreateUpdateUploadMediaSerializer(obj.user.profile_picture)
            return serializer.data
        except Exception as error:
            return obj.user.profile_picture
    def get_email(self, obj):
        return obj.user.email
    def get_phone_no(self, obj):
        return obj.user.phone_no
    def get_address(self, obj):
        return obj.user.address
    def get_weight(self, obj):
        return f"{obj.weight} Kg"
    def get_hair_color(self, obj):
        return obj.get_hair_color_display()
    def get_eye_color(self, obj):
        return obj.get_eye_color_display()
    def get_categories(self, obj):
        try:
            categories = TalentCategoryModel.objects.filter(id__in=obj.categories)
            cat_serializer = CategorySerializer(categories, many=True)
            return cat_serializer.data
        except:
            return obj.categories
    def get_sub_categories(self, obj):
        try:
            sub_categories = TalentSubCategoryModel.objects.select_related("category").filter(id__in=obj.sub_categories)
            sub_cat_serializer = SubCategorySerializer(sub_categories, many=True)
            return sub_cat_serializer.data
        except:
            return obj.sub_categories

class UserSerializersForClientDetails(serializers.ModelSerializer):
    profile_picture = CreateUpdateUploadMediaSerializer()
    class Meta:
        model = UserModel
        fields = ["id", "name", "profile_picture"]

class BookedClientDetailSerializers(serializers.ModelSerializer):
    client = UserSerializersForClientDetails()
    talent = UserSerializersForClientDetails()
    status = serializers.SerializerMethodField()
    track_booking = serializers.SerializerMethodField()
    class Meta:
        model = BookingTalentModel
        fields = ["id", "client", "talent", "offer_price", "time", "date", "status", "track_booking", \
                  "currency", "services", "created_at"]
    def get_status(self, obj):
        try:
            return obj.get_status_display()    
        except:
            obj.status    
    def get_track_booking(self, obj):
        try:
            return obj.get_track_booking_display()    
        except:
            obj.track_booking    
    
class SlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationalSlotsModel
        fields = ["id", "user", "day", "start", "end", "date", "is_active"]