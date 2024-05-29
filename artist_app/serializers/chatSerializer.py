from rest_framework import serializers
from artist_app.models import ChatSessionModel, UserModel, ChatStorageModel
from artist_app.serializers.uploadMediaSerializer import CreateUpdateUploadMediaSerializer 

class UserDetailsSerializer(serializers.ModelSerializer):
    profile_picture = CreateUpdateUploadMediaSerializer()
    class Meta:
        model = UserModel
        fields = ["id", "email", "first_name", "last_name", "profile_picture"]

class UserChatsSerializer(serializers.ModelSerializer):
    client = UserDetailsSerializer()
    talent = UserDetailsSerializer()
    last_message_details = serializers.SerializerMethodField()
    class Meta:
        model = ChatSessionModel
        fields = ["id", "session_id", "client", "talent", "last_message_details"]
    def get_last_message_details(self, obj):
        data = {}
        last_message_obj = ChatStorageModel.objects.filter(session=obj.id).last()
        data["last_message"] = last_message_obj.message
        data["last_message_timestamp"] = last_message_obj.timestamp
        return data

class ChatSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer()
    class Meta:
        model = ChatStorageModel
        fields = ["id", "session", "user", "message", "timestamp"]