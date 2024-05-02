from django.urls import path
from artist_app.views import uploadMediaView,adminView

urlpatterns = [
    path("media", uploadMediaView.UploadMediaView.as_view()),
    path("show-questions",adminView.GetAllQuestionsAnswers.as_view()),
]