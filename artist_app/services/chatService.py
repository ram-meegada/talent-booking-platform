from artist_app.models import ChatSessionModel, ChatStorageModel
from artist_app.serializers.chatSerializer import UserChatsSerializer, ChatSerializer
from django.db.models import Q

class ChatService():
    def user_chats(self, request):
        chats = ChatSessionModel.objects.filter(Q(client_id=request.user.id) | Q(talent_id=request.user.id))
        serializer = UserChatsSerializer(chats, many=True)
        return {"data": serializer.data, "message": "Chats fetched successfully", "status": 200}

    def conversation(self, request, session):
        chat = ChatStorageModel.objects.filter(session=session)
        serializer = ChatSerializer(chat, many=True)
        return {"data": serializer.data, "message": "Chat fetched successfully", "status": 200}
