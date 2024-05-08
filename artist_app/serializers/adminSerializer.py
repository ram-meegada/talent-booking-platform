from rest_framework import serializers
from artist_app.models.talentCategoryModel import TalentCategoryModel
from artist_app.models.talentSubCategoryModel import TalentSubCategoryModel
from artist_app.models.faqModel import FAQModel
from artist_app.models import TermAndConditionModel
from artist_app.models import UserModel
from artist_app.models.manageAddressModel import ManageAddressModel
from artist_app.serializers.uploadMediaSerializer import CreateUpdateUploadMediaSerializer
# from artist_python_backend.artist_app.models import manageAddressModel



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentCategoryModel
        fields = ["id", "name"]

class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
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

class AdminLoginserializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id","email"]

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
    address = serializers.SerializerMethodField()
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
    class Meta:
        model = UserModel
        fields = ["id","username","country_code","email","phone_no","address","profile_picture"]

class GetAllCategoriesSerializers(serializers.ModelSerializer):
    update_at = serializers.SerializerMethodField()
    class Meta:
        model = TalentCategoryModel
        fields = ["id","name","update_at","is_active"]

    def get_update_at(self, obj):
       return obj.update_at.date()

class SubcategoryDetailsByCategoryIdSerializer(serializers.ModelSerializer):
    update_at  = serializers.SerializerMethodField()

    class Meta:
        model = TalentSubCategoryModel
        fields = ["id","name","update_at","is_active"]

        def get_update_at(self, obj):
            return obj.update_at.date()
