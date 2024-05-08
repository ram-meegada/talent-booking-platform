from django.urls import path
from artist_app.views import uploadMediaView, adminView, chatView, ratingsView

urlpatterns = [
    path("media", uploadMediaView.UploadMediaView.as_view()),
    path("show-questions", adminView.GetAllQuestionsAnswers.as_view()),
    path("terms-and-conditions-show", adminView.GetTermsAndConditions.as_view()),

    #### Chat ####
    path("all-chats", chatView.GetChatsView.as_view()),
    path("conversation/<int:session>", chatView.ConversationView.as_view()),

    #### ratings ####
    path("ratings/<int:talent_id>", ratingsView.AddRatingView.as_view()),
    path("user-ratings/<int:talent_id>", ratingsView.GetUserRatingView.as_view()),
]