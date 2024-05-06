from django.urls import path
from artist_app.views import adminView

urlpatterns = [
    path("category/", adminView.AddTalentCategoryView.as_view()),
    path("sub-category/", adminView.AddTalentSubCategoryView.as_view()),
    path("questions",adminView.AddQuestionsAndAnswersView.as_view()),
    path("update-question/<int:id>",adminView.UpdateQuestionsAnswersView.as_view()),
    path("delete-question/<int:id>",adminView.DeleteQuestionAnswerView.as_view()),
    path("terms-and-conditions",adminView.AddTermsAndConditions.as_view()),
    path("update-terms-and-conditions/<int:id>",adminView.UpdateTermsAndConditions.as_view()),

]