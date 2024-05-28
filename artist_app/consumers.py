# import json
# from datetime import datetime
# from time import sleep
# from channels.db import database_sync_to_async
# from asgiref.sync import sync_to_async, async_to_sync
# from channels.generic.websocket import AsyncWebsocketConsumer
# from artist_app.models.chatSessionModel import ChatSessionModel
# from artist_app.models.chatStorageModel import ChatStorageModel
# from artist_app.models.userModel import UserModel
# from django.db.models import Q
# from artist_app.utils.sendOtp import generate_encoded_id
# import string
# import random

# def generate_session_id():
#     chars = string.ascii_letters + string.digits
#     alpha_numeric = ''.join([random.choice(chars) for i in range(10)])
#     return alpha_numeric

# class ChattingConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user1 = self.scope['url_route']['kwargs']['user1']
#         self.user2 = self.scope['url_route']['kwargs']['user2']
#         self.session = await database_sync_to_async(self.create_or_get_session)(self.user1, self.user2)
#         await self.channel_layer.group_add(self.session.session_id, self.channel_name)
#         await self.accept()

#     def create_or_get_session(self, user1, user2):
#         new_session_id = generate_session_id()
#         try:
#             session = ChatSessionModel.objects.get(Q(client_id=user1, talent_id=user2) |
#                                                    Q(client_id=user2, talent_id=user1))
#         except ChatSessionModel.DoesNotExist:
#             get_user1 = UserModel.objects.get(id=user1)
#             get_user2 = UserModel.objects.get(id=user2)
#             if get_user1.role == 1:
#                 session = ChatSessionModel.objects.create(session_id=new_session_id, client_id=get_user1.id, \
#                                                           talent_id=get_user2.id)
#             elif get_user1.role == 2:
#                 session = ChatSessionModel.objects.create(session_id=new_session_id, client_id=get_user2.id, \
#                                                           talent_id=get_user1.id)
#         return session
        
#     async def receive(self, text_data):
#         newMessage = json.loads(text_data)
#         await self.channel_layer.group_send(self.session.session_id,
#                     {
#                         'type': 'chat_message',
#                         'msg': json.dumps(newMessage)
#                     }
#                 )
#         save_chat = await database_sync_to_async(ChatStorageModel.objects.create)\
#                                                 (session_id=self.session.id, user_id=self.user1, \
#                                                  message=newMessage["message"])

#     async def chat_message(self, event):
#         print('-----------event["msg"]------------')
#         await self.send(text_data=event["msg"])

#     async def disconnect(self, close_code):
#         print('websocket disconnected.....', close_code)






import json
from datetime import datetime
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from artist_app.models.chatSessionModel import ChatSessionModel
from artist_app.models.chatStorageModel import ChatStorageModel
from artist_app.models.userModel import UserModel
from django.db.models import Q
from artist_app.serializers.chatSerializer import ChatSerializer  # Import the user serializer
import string
import random
def generate_session_id():
    chars = string.ascii_letters + string.digits
    alpha_numeric = ''.join([random.choice(chars) for _ in range(10)])
    return alpha_numeric

class ChattingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user1 = self.scope['url_route']['kwargs']['user1']
        self.user2 = self.scope['url_route']['kwargs']['user2']
        self.session = await database_sync_to_async(self.create_or_get_session)(self.user1, self.user2)
        await self.channel_layer.group_add(self.session.session_id, self.channel_name)
        await self.accept()

    def create_or_get_session(self, user1, user2):
        new_session_id = generate_session_id()
        try:
            session = ChatSessionModel.objects.get(Q(client_id=user1, talent_id=user2) |
                                                   Q(client_id=user2, talent_id=user1))
        except ChatSessionModel.DoesNotExist:
            get_user1 = UserModel.objects.get(id=user1)
            get_user2 = UserModel.objects.get(id=user2)
            if get_user1.role == 1:
                session = ChatSessionModel.objects.create(session_id=new_session_id, client_id=get_user1.id, 
                                                          talent_id=get_user2.id)
            elif get_user1.role == 2:
                session = ChatSessionModel.objects.create(session_id=new_session_id, client_id=get_user2.id, 
                                                          talent_id=get_user1.id)
        return session

    async def receive(self, text_data):
        new_message_data = json.loads(text_data)
        message_text = new_message_data["message"]
        timestamp = datetime.now().isoformat()

        user = await database_sync_to_async(UserModel.objects.get)(id=self.user1)
        user_data = ChatSerializer(user).data  # Serialize the user data

        # Save the message to the database
        saved_message = await database_sync_to_async(ChatStorageModel.objects.create)(
            session_id=self.session.id, 
            user_id=self.user1, 
            message=message_text
        )

        # Create the response message format
        response_message = {
            "id": saved_message.id,
            "session": self.session.id,
            "user": user_data,
            "message": message_text,
            "timestamp": timestamp
        }

        await self.channel_layer.group_send(
            self.session.session_id,
            {
                'type': 'chat_message',
                'msg': json.dumps(response_message)  # Send the formatted response message
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=event["msg"])

    async def disconnect(self, close_code):
        print('websocket disconnected.....', close_code)


