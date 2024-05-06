from django.urls import path
from artist_app.views import adminView

urlpatterns = [
    path("category/", adminView.AddTalentCategoryView.as_view()),
    path("sub-category/", adminView.AddTalentSubCategoryView.as_view()),
    # FAQs urls
    path("questions",adminView.AddQuestionsAndAnswersView.as_view()),
    path("update-question/<int:id>",adminView.UpdateQuestionsAnswersView.as_view()),
    path("delete-question/<int:id>",adminView.DeleteQuestionAnswerView.as_view()),
    # terms and conditions urls
    path("terms-and-conditions",adminView.AddTermsAndConditions.as_view()),
    path("update-terms-and-conditions/<int:id>",adminView.UpdateTermsAndConditions.as_view()),
    #  admin onboarding urls
    path("admin-log-in",adminView.AdminLoginView.as_view()),
    path("forgot-password",adminView.ForgotPasswordView.as_view()),
    path("send-otp",adminView.resendOTPView.as_view()),
    path("verify-otp",adminView.VerifyOTPViewAdminSide.as_view()),
    # manage customer urls

    path("fetch-all-customers",adminView.GetAllCustomerView.as_view()),
    path("add-customer",adminView.AddCustomerByAdminView.as_view()),
    path("edit-customer-by-id/<int:id>",adminView.updateCustomerDetailsByAdminView.as_view()),
    path("delete-customer-by-id/<int:id>",adminView.DeleteCustomerByAdminView.as_view()),
    

]