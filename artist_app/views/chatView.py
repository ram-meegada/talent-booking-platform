from artist_app.services.chatService import ChatService
from rest_framework.views import APIView
from rest_framework.response import Response

chat_obj = ChatService()

class GetChatsView(APIView):
    def get(self, request):
        result = chat_obj.user_chats(request)
        return Response(result, status=result["status"])

class ConversationView(APIView):
    def get(self, request, session_id):
        result = chat_obj.conversation(request, session_id)
        return Response(result, status=result["status"])