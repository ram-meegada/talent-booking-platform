from django.urls import path
from artist_app.views import adminView

urlpatterns = [
    #  admin onboarding urls
    path("admin-log-in",adminView.AdminLoginView.as_view()),
    path("forgot-password",adminView.ForgotPasswordView.as_view()),
    path("send-otp",adminView.resendOTPView.as_view()),
    path("verify-otp",adminView.VerifyOTPViewAdminSide.as_view()),
    path("change-password",adminView.ChangePasswordByTokenView.as_view()),
    path("admin-details",adminView.GetAdminDetailsByTokenView.as_view()),
    path("update-details",adminView.UpdateAdminDetailsByTokenView.as_view()),
    path("admin-log-out",adminView.LogOutView.as_view()),

    # 

    # FAQs urls
    path("questions",adminView.AddQuestionsAndAnswersView.as_view()),
    path("update-question/<int:id>",adminView.UpdateQuestionsAnswersView.as_view()),
    path("delete-question/<int:id>",adminView.DeleteQuestionAnswerView.as_view()),

    # terms and conditions urls
    path("terms-and-conditions",adminView.AddTermsAndConditions.as_view()),
    path("update-terms-and-conditions/<int:id>",adminView.UpdateTermsAndConditions.as_view()),


    # manage customer urls
    path("all-customers",adminView.GetAllCustomerView.as_view()),
    path("add-customer",adminView.AddCustomerByAdminView.as_view()),
    path("customers-details-by-id/<int:id>",adminView.GetAllCustomerDetailsByidView.as_view()),
    path("edit-customer-by-id/<int:id>",adminView.updateCustomerDetailsByAdminView.as_view()),
    path("delete-customer-by-id/<int:id>",adminView.DeleteCustomerByAdminView.as_view()),

    # manage categories Urls
    path("category", adminView.AddTalentCategoryView.as_view()),
    path("all-category",adminView.GetAllCategoriesView.as_view()),
    path("get-categories-details-by-id/<int:id>",adminView.GetCategoriesDetailsByIdView.as_view()),
    path("update-categories-detail-by-id/<int:id>",adminView.UpdateCategoriesByIdView.as_view()),
    path("delete-category-by-id/<int:id>",adminView.DeleteCategoriesByIdView.as_view()),
    path("sub-category-based-on-category",adminView.GetAllSubCategoryBasedOnCategoryView.as_view()),
    path("sub-category/", adminView.AddTalentSubCategoryView.as_view()),
    path("delete-subcategory-by-id/<int:id>",adminView.DeleteSubcategoryByIdView.as_view()),
    path("update-subcategory-by-id/<int:id>",adminView.UpdateSubcategoryByIdView.as_view()),
    path("get-subcategory-by-id/<int:id>",adminView.GetSubCategoryByIdView.as_view()),

    #manage artist urls
    path("get-all-artist-details",adminView.GetAllArtistDetialsView.as_view()),
    path("get-artist-details-by-id/<int:id>",adminView.GetArtistDetailsByIdView.as_view()),
    path("update-artist-details-by-id/<int:id>",adminView.UpdateArtistDetailsByIdView.as_view()),
    path("delete-artist-details-by-id/<int:id>",adminView.DeleteArtistByIdView.as_view()),
    path("add-artist",adminView.AddArtistThroughAdminView.as_view()),
    
    # booking module Urls
    # path("get_booking_details",adminView.BookingDetailsView.as_view()),



]
