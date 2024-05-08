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
    class Meta:
        model = ChatSessionModel
        fields = ["id", "session_id", "client", "talent"]

class ChatSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer()
    class Meta:
        model = ChatStorageModel
        fields = ["id", "session", "user", "message", "timestamp"]