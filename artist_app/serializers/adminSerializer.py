from artist_app.models.permissionModel import PermissionModel
from rest_framework import serializers
from artist_app.models.talentCategoryModel import TalentCategoryModel
from artist_app.models.talentSubCategoryModel import TalentSubCategoryModel
from artist_app.models.faqModel import FAQModel
from artist_app.models import TermAndConditionModel
from artist_app.models import UserModel
from artist_app.models.manageAddressModel import ManageAddressModel
from artist_app.serializers.uploadMediaSerializer import CreateUpdateUploadMediaSerializer
from artist_app.models.talentDetailsModel import TalentDetailsModel
from artist_app.models.uploadMediaModel import UploadMediaModel
from artist_app.models.bookingTalentModel import BookingTalentModel
# from artist_python_backend.artist_app.models import manageAddressModel
from artist_app.serializers.Clientserializer import TalentBasicDetails


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentCategoryModel
        fields = ["id", "name"]

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentSubCategoryModel
        fields = ["id", "name", "category"]


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQModel
        fields = ["question","answer"]

class TermAndConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermAndConditionModel
        fields = ["id", "data"]


class AdminVerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id","email","otp","otp_email_verification"]

class AddNewClientByAdminSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id","email","first_name","last_name","phone_no","address","city","state","country", \
                  "profile_picture", "country_code"]

class GetClientByAdminSeriaizer(serializers.ModelSerializer):
    profile_picture = CreateUpdateUploadMediaSerializer()
    profile_picture = CreateUpdateUploadMediaSerializer()
    class Meta:
        model = UserModel
        fields = ["id","email","first_name","last_name","phone_no","address","city","state","country", \
                  "profile_picture", "country_code"]


class ManageAddressByAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManageAddressModel
        fields = ["id","address_location","user"]

class GetAllClientsDetailsSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    profile_picture = CreateUpdateUploadMediaSerializer()
    class Meta:
        model = UserModel
        fields = ["id", "full_name", "email", "country_code", "phone_no", "address", "is_active", \
                  "profile_picture", "city", "state", "country"]

    def get_full_name(self, obj):
        try:
            fullname=obj.first_name +" "+ obj.last_name
            return fullname
        except:
            return None    


class ShowAdminDetialsByTokenSerializer(serializers.ModelSerializer):
    profile_picture = CreateUpdateUploadMediaSerializer()
    class Meta:
        model = UserModel
        fields = ["id","username","country_code","email","phone_no","address","profile_picture"]

    def get_address(self, obj):
        try:
            address = ManageAddressModel.objects.filter(user_id=obj).first
            serializer = ManageAddressByAdminSerializer(address, many=True)
            return serializer.data
        except Exception as e:
            return None

class updateAdminDetialsByTokenSerializer(serializers.ModelSerializer):
    profile_picture =serializers.SerializerMethodField()
    class Meta:
        model = UserModel
        fields = ["id","username","country_code","email","phone_no","address","profile_picture"]
    
    def get_profile_picture(self, obj):
        try:
            get_profile_picture = UploadMediaModel.objects.get(id = self.context.get("profile_picture"))
            serializers = CreateUpdateUploadMediaSerializer(get_profile_picture)
            return serializers.data
        except Exception as e:
            return obj.profile_picture_id

class GetAllCategoriesSerializers(serializers.ModelSerializer):
    update_at = serializers.SerializerMethodField()
    class Meta:
        model = TalentCategoryModel
        fields = ["id","name","update_at","is_active"]

    def get_update_at(self, obj):
       return obj.updated_at.date()

class SubcategoryDetailsByCategoryIdSerializer(serializers.ModelSerializer):
    update_at  = serializers.SerializerMethodField()

    class Meta:
        model = TalentSubCategoryModel
        fields = ["id","name","update_at","is_active"]

    def get_update_at(self, obj):
        return obj.updated_at.date()

#manage artist serializers


class GetArtistDetailsSerializers(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    country_code = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone_no = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    sub_categories = serializers.SerializerMethodField()
    date_of_birth = serializers.SerializerMethodField()
    experience = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    verification_status = serializers.SerializerMethodField()

    class Meta:
        model = TalentDetailsModel
        fields = ["id","name","email","profile_picture","gender","country_code","phone_no","date_of_birth",\
                  "experience",'booking_method',"address","categories","sub_categories", "is_active", "verification_status"]

    def get_date_of_birth(self, obj):
        return obj.user.date_of_birth
    
    def get_id(self, obj):
        return obj.user.id

    def get_experience(self, obj):
        return obj.user.experience
    def get_profile_picture(self, obj):
        p_obj = obj.user.profile_picture
        serializers= CreateUpdateUploadMediaSerializer(p_obj)
        return serializers.data
    def get_name(self, obj):
        return obj.user.first_name+" "+obj.user.last_name
    def get_address(self, obj):
        return obj.user.address
    def get_email(self, obj):
        return obj.user.email
    def get_phone_no(self, obj):
        return obj.user.phone_no
    def get_country_code(self, obj):
        return obj.user.country_code
    def get_gender(self, obj):
        return obj.user.gender
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
    def get_verification_status(self, obj):
        try:
            return obj.user.get_verification_status_display()
        except:
            return obj.user.verification_status

class GetArtistDetailsByIdSerializer(serializers.ModelSerializer):
    country_code = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone_no = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    sub_categories = serializers.SerializerMethodField()
    date_of_birth = serializers.SerializerMethodField()
    experience = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    cover_photo = CreateUpdateUploadMediaSerializer()
    portfolio = serializers.SerializerMethodField()
    booking_method = serializers.SerializerMethodField()
    hair_color = serializers.SerializerMethodField()
    eye_color = serializers.SerializerMethodField()

    class Meta:
        model = TalentDetailsModel
        fields = ["id","name","email","profile_picture","gender","state","city","country","country_code",\
                  "phone_no","date_of_birth","experience",'booking_method',"address", "categories","sub_categories",\
                  "bust","waist","hips","height_feet","height_inches","weight","hair_color","eye_color","portfolio",\
                  "cover_photo"]

    def get_date_of_birth(self, obj):
        return obj.user.date_of_birth
    def get_date_of_birth(self, obj):
        return obj.user.date_of_birth
    def get_hair_color(self, obj):
        return obj.get_hair_color_display()
    def get_eye_color(self, obj):
        return obj.get_eye_color_display()

    def get_experience(self, obj):
        return obj.user.experience
    def get_profile_picture(self, obj):
        p_obj = obj.user.profile_picture
        serializers= CreateUpdateUploadMediaSerializer(p_obj)
        return serializers.data
    def get_country(self, obj):
        return obj.user.country
    def get_booking_method(self, obj):
        return obj.get_booking_method_display()
    def get_city(self, obj):
        return obj.user.city
    def get_state(self, obj):
        return obj.user.state
    def get_cover_photo(self,obj):
        image= obj.cover_photo
        serializer = CreateUpdateUploadMediaSerializer(image)
        return serializer.data
    def get_name(self, obj):
        return obj.user.name
    def get_address(self, obj):
        return obj.user.address
    def get_email(self, obj):
        return obj.user.email
    def get_phone_no(self, obj):
        return obj.user.phone_no
    def get_country_code(self, obj):
        return obj.user.country_code
    def get_gender(self, obj):
        return obj.user.get_gender_display()
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
    def get_portfolio(self, obj):
        try:
            media = UploadMediaModel.objects.filter(id=obj.portfolio[0]).first()
            if media:
                serializer = CreateUpdateUploadMediaSerializer(media)
                return serializer.data
        except:
            return obj.portfolio[0]

# class bookingClientArtistDetailsSerializer(serializers.ModelSerializer):
#     profile_picture = CreateUpdateUploadMediaSerializer()
#     full_name = serializers.SerializerMethodField()
#     class Meta:
#         model = UserModel
#         fields = ["id","full_name","profile_picture"]

#     def get_full_name(self, obj):
#         return obj.first_name+" "+obj.last_name

# class ManageAddressBookingDetailsModule(serializers.ModelSerializer):
#     class Meta:
#         model = ManageAddressModel
#         fields = "__all__"

# #booking Module
# class BookingDetailsModuleSerializer(serializers.ModelSerializer):
#     client = serializers.SerializerMethodField()
#     artist = serializers.SerializerMethodField()
#     address = serializers.SerializerMethodField()
#     profession= serializers.SerializerMethodField()   # category
#     description = serializers.SerializerMethodField()
#     service_fee = serializers.SerializerMethodField()
#     service = serializers.SerializerMethodField()   # sub-category
#     class Meta:
#         model = BookingTalentModel
#         fields = ["id","client","artist","profession","address","description","date","time","duration","offer_price","service_fee","service","status","currency"]

#     def get_client(self, obj):
#         id=obj.first().client.id
#         # id = obj.client
#         user = UserModel.objects.get(id =id)
#         serializer = bookingClientArtistDetailsSerializer(user)
#         print(serializer.data,"44444444444444444444")
#         return serializer.data
    
#     def get_artist(self, obj):
#         print(obj.first().talent.id,"2222222222")
#         id = obj.first().talent.id
#         user = UserModel.objects.get(id =id)
#         serializer = bookingClientArtistDetailsSerializer(user)
#         print(serializer.data,"4444444444444444444455555555555555")
#         return serializer.data

#     def get_address(self, obj):
#         id = obj.address
#         address = ManageAddressModel.objects.get(id=id)
#         serializer = ManageAddressBookingDetailsModule(address)
#         return serializer.data

#     def get_profession(self, obj):
#         id = obj.artist
#         category =TalentDetailsModel.objects.get(user_id=id).categories
#         serializer = CategorySerializer(category, many=True)
#         return serializer.data

#     def get_service(self, obj):
#         id = obj.artist
#         sub_categories = TalentDetailsModel.objects.get(user_id=id).sub_categories
#         serializers = SubCategorySerializer(sub_categories, many = True)
#         return serializers.data

#     def get_service_fee(self, obj):
#         service = 15
#         return service
    
#     def get_description(self, obj):
#         return obj.comment
        

        



        

class CreateUpdateTalentUserByAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id", "profile_picture", "name", "email", "gender", "country_code", "phone_no",\
                  "date_of_birth", "experience", "address", "city", "state", "country")
        
class CreateModelStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentDetailsModel
        fields = ('id', 'bust', 'waist', 'hips', 'height_feet', 'height_inches', 'weight', 'hair_color',\
                   'eye_color', 'booking_method', 'portfolio', 'cover_photo', 'categories', 'sub_categories')        
        
class CreateRolePermissionSubAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionModel
        fields = ['id','module','can_add_edit','can_view','can_be_delete']

class GetRolePermissionSubAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionModel
        fields = ['id','module', 'can_add_edit', 'can_view', 'can_be_delete']

class GetSubAdminSerializer(serializers.ModelSerializer):
    profile_picture = CreateUpdateUploadMediaSerializer()
    permissions = serializers.SerializerMethodField()
    class Meta:
        model = UserModel
        fields = ["id","name", "email", "phone_no","profile_picture", "permissions"]
    def get_permissions(self, obj):
        try:
            p = PermissionModel.objects.filter(user=obj.id)
            serializer = GetRolePermissionSubAdminSerializer(p, many=True)
            return serializer.data
        except:
            return None  

class CreateSubAdminSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserModel
        fields = ("id","name","email","phone_no","profile_picture",'role')
        extra_kwargs = {'role': {'default': 4}}

class BookingsSerializer(serializers.ModelSerializer):
    talent = TalentBasicDetails()
    client = TalentBasicDetails()
    address = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    class Meta:
        model = BookingTalentModel
        fields = ["id", "talent", "client", "address", "date", "time", "duration", "offer_price", "comment",\
                   "currency", "status"]
    def get_address(self, obj):
        try:
            return obj.client.address
        except Exception as e:
            return None    
    def get_status(self, obj):
        try:
            return obj.get_status_display()
        except Exception as e:
            return obj.status

