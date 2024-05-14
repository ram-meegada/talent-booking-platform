from rest_framework import serializers
from artist_app.models.userModel import UserModel
from artist_app.models.manageAddressModel import ManageAddressModel
from artist_app.models.talentSubCategoryModel import TalentSubCategoryModel
from artist_app.models.talentDetailsModel import TalentDetailsModel
from artist_app.serializers.uploadMediaSerializer import CreateUpdateUploadMediaSerializer
from artist_app.models.uploadMediaModel import UploadMediaModel
from artist_app.models.bookingTalentModel import BookingTalentModel
from artist_app.utils.sendOtp import generate_access_token

class CreateClientSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id", "profile_picture", "first_name", "email", "last_name", "gender", "country_code", "phone_no",\
                  "date_of_birth", "experience", "address", "city", "state", "country", "encoded_id")

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
        fields = ["address_location", "house_flat_block_no", "landmark", "street_no", "phone_no_manage_address", "address_type"]

class SubCategories(serializers.ModelSerializer):
    class Meta:
        model = TalentSubCategoryModel
        fields =["name"]
class TalentBasedOnSubcategories(serializers.ModelSerializer):
    profile_picture = CreateUpdateUploadMediaSerializer()
    class Meta:
        model = TalentDetailsModel
        fields = fields = ('id', 'bust', 'waist', 'hips', 'height_feet', 'height_inches', 'weight', 'hair_color', 'eye_color', 'booking_method')

class TalentDetailsBasedOnSubcategories(serializers.ModelSerializer):
    class Meta:
        model = TalentDetailsModel
        fields =["id","bust","waist","hips","height_feet","height_inches","weight","hair_color","eye_color","booking_method","portfolio","cover_photo"]
class TalentBasicDetails(serializers.ModelSerializer):
    profile_picture = CreateUpdateUploadMediaSerializer()
    professional_details = serializers.SerializerMethodField()
    class Meta:
        model = UserModel
        fields = ["id", "first_name","last_name","profile_picture","experience","phone_no","city","country",\
                  "state", "professional_details"]
    def get_professional_details(self, obj):
        details = TalentDetailsModel.objects.filter(user=obj.id).first()
        if details:
            serializer = TalentDetailsBasedOnSubcategories(details)
            return serializer.data
        else:
            return {}    


class BookingProposalSerializers(serializers.ModelSerializer):
    pass




class BookingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingTalentModel
        fields = "__all__"


class ShowBookingDetailsSerializer(serializers.ModelSerializer):
    # user = CreateClientSerializers()
    class Meta:
        model = BookingTalentModel
        fields = "__all__"


