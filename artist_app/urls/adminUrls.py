from django.urls import path
from artist_app.views import adminView

urlpatterns = [
    path("category/", adminView.AddTalentCategoryView.as_view()),
    path("sub-category/", adminView.AddTalentSubCategoryView.as_view()),
]