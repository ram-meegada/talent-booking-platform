from rest_framework import serializers
from artist_app.models.userModel import UserModel


class CreateClientSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["first_name","last_name","password","email","phone_no","country_code","address","city","state","country","role"]
