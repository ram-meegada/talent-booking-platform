from django.urls import path
from artist_app.views import uploadMediaView

urlpatterns = [
    path("media", uploadMediaView.UploadMediaView.as_view())
]