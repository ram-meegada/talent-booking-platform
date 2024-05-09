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
# from artist_python_backend.artist_app.models import manageAddressModel



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
        fields = ["id","email","first_name","last_name","phone_no","address","city","state","country"]


class ManageAddressByAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManageAddressModel
        fields = ["id","address_location","user"]

class GetAllClientsDetailsSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    addresses = serializers.SerializerMethodField()
    class Meta:
        model = UserModel
        fields = ["id","full_name","email","phone_no","addresses"]

    def get_full_name(self, obj):
        try:
            fullname=obj.first_name +" "+ obj.last_name
            return fullname
        except:
            return None
    
    def get_addresses(self,obj):
        print(obj,"11122222112")
        try:
            user_obj= ManageAddressModel.objects.filter(user_id=obj)
            print(user_obj,"8888888888888")
            serializer=ManageAddressByAdminSerializer(user_obj, many=True)
            return serializer.data
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

    class Meta:
        model = TalentDetailsModel
        fields = ["id","name","email","profile_picture","gender","phone_no","date_of_birth","experience",'booking_method',"address","categories","sub_categories"]


    def get_date_of_birth(self, obj):
        return obj.user.date_of_birth

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

# class 
        

