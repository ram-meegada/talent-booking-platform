from http import client
from django.urls import path
from artist_app.views import talentView

urlpatterns = [
    path("registration", talentView.TalentSignUpView.as_view()),
    path("login", talentView.TalentLoginView.as_view()),

    path("send-otp", talentView.SendEmailOrPhoneView.as_view()),
    path("verify-otp", talentView.VerifyMailOrPhoneView.as_view()),
    path("resend-otp", talentView.ResendOtpView.as_view()),

    path("sub-categories", talentView.SubCategoryListingView.as_view()),
    path("update-profile", talentView.ProfileSetUpAndUpdateView.as_view()),
    path("profile-details", talentView.TalentUserDetailsView.as_view()),
    path("upcoming-bookings-listing",talentView.ClientUpcomingBookingListing.as_view()),
    path("past-booked-client-list",talentView.ClientPastBookingListing.as_view()),
    path("cancel-booked-client-list",talentView.ClientdeclineParamenterListing.as_view())


]