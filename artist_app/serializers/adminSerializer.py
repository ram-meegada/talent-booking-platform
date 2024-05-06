from rest_framework import serializers
from artist_app.models.talentCategoryModel import TalentCategoryModel
from artist_app.models.talentSubCategoryModel import TalentSubCategoryModel
from artist_app.models.faqModel import FAQModel
from artist_app.models import TermAndConditionModel
from artist_app.models import UserModel
from artist_app.models.manageAddressModel import ManageAddressModel



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
    address = ManageAddressByAdminSerializer()
    class Meta:
        model = UserModel
        fields = ["id","full_name","email","phone_no","address"]

    def get_full_name(self, obj):
        
        return obj.first_name +" "+obj.last_name