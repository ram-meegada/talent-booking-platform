from django.urls import path
from artist_app.views import clientView, adminView, talentView

urlpatterns = [
    path("signup", clientView.SignUpView.as_view()),
    path("verify-otp", clientView.VerifyOtpViaMailView.as_view()),
    path("log-in", clientView.LogInView.as_view()),
    path("resend-otp", clientView.ResendOtpView.as_view()),

    path("otp-to-user", talentView.ResendOtpAfterLoginView.as_view()),

    path("edit-profile", clientView.EditClientDetailsByTokenView.as_view()),
    path("change-password", adminView.ChangePasswordByTokenView.as_view()),
    path("profile-details", clientView.clientDetailsbyTokenView.as_view()),
    path("user-forgot-password",adminView.resendOTPView.as_view()),
    path("user-reset-password",clientView.ResetPassword.as_view()),

    ################# ADDRESS-MANAGE #########################
    path("address",clientView.AddClientNewAddressDetailsView.as_view()),
    path("address-details/<int:id>",clientView.EditClientAddressDetailsView.as_view()),
    path("all-address",clientView.ShowAllAddressesDetailsView.as_view()),
    path("address-details-by-id",clientView.GetAddressDetialsByIdView.as_view()),
    path("delete-address/<int:id>",clientView.DeleteClientAddressDetailsBYIDView.as_view()),

    #################### category listing #####################
    path("category",clientView.ListingAllCategories.as_view()),
    path("search-category", clientView.ListingAllCategoriesBasedOnCategoryView.as_view()),
    path("sub-categories",clientView.ListingAllSubCategoriesBasedOnCategories.as_view()),

    ############### booking #####################
    path("talent-detials", clientView.ListingAllTalent.as_view()),
    path("talent-detials-for-booking/<int:talent_id>", clientView.TalentDetailsForBookingView.as_view()),
    path("filter-talent", clientView.FilterAndSortView.as_view()),

    path("talent-detials-by-id/<int:id>",clientView.TalentDetailsById.as_view()),
    path("book-talent",clientView.BookTalentView.as_view()),
    path("talent-slots-by-date", clientView.GetTalentSlotsView.as_view()),
    path("fetch-booking-details/<int:id>", clientView.GetAllBookTalentDetails.as_view()),

    path("ongoing-bookings", clientView.OngoingBookingsView.as_view()),
    path("completed-bookings", clientView.CompletedBookingsView.as_view()),
    path("cancelled-bookings", clientView.CancelledBookingsView.as_view()),
    path("mark-booking-completed/<int:booking_id>", clientView.MarkBookingCompletedView.as_view()),
    path("accept-decline-booking/<int:booking_id>", clientView.AcceptOrCancelBookingsView.as_view()),
    path("complete-payment/<int:booking_id>", clientView.CompletePaymentView.as_view()),

    path("all-services/<int:id>", clientView.FetchAllTalentServicesView.as_view()),

    path("tags", clientView.TagsListingView.as_view()),
]
