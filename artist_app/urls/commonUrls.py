from django.urls import path
from artist_app.views import uploadMediaView, adminView, chatView

urlpatterns = [
    path("media", uploadMediaView.UploadMediaView.as_view()),
    path("show-questions", adminView.GetAllQuestionsAnswers.as_view()),
    path("terms-and-conditions-show", adminView.GetTermsAndConditions.as_view()),

    #### Chat ####
    path("all-chats", chatView.GetChatsView.as_view()),
    path("conversation/<int:session>", chatView.ConversationView.as_view()),
]