from http import client
from django.urls import path
from artist_app.views import talentView, clientView, adminView

urlpatterns = [
    path("registration", talentView.TalentSignUpView.as_view()),
    path("login", talentView.TalentLoginView.as_view()),

    path("send-otp", talentView.SendEmailOrPhoneView.as_view()),
    path("verify-otp", talentView.VerifyMailOrPhoneView.as_view()),
    path("resend-otp", talentView.ResendOtpView.as_view()),

    path("update-profile", talentView.ProfileSetUpAndUpdateView.as_view()),
    path("edit-profile", talentView.EditProfileByTokenView.as_view()),
    path("profile-details", talentView.TalentUserDetailsView.as_view()),
    path("change-password",adminView.ChangePasswordByTokenView.as_view()),

    ######### bookings ###########
    path("fetch-booking-details/<int:id>",clientView.GetAllBookTalentDetails.as_view()),
    path("upcoming-bookings-listing", talentView.ClientUpcomingBookingListing.as_view()),
    path("recent-offers", talentView.RecentOffersView.as_view()),
    path("counter-offer", talentView.CounterOfferByTalentView.as_view()),
    path("accept-offer", talentView.AcceptOfferByTalentView.as_view()),
    path("decline-offer", talentView.DeclineOfferByTalentView.as_view()),
    path("past-bookings", talentView.ClientPastBookingListing.as_view()),
    path("cancelled-bookings", talentView.CancelledBookingsView.as_view()),


    path("all-categories", talentView.AllCategoriesView.as_view()),
    path("sub-categories", talentView.SubCategoryListingView.as_view()),

    ########### slots #############
    path("add-slots", talentView.GenerateSlotsView.as_view()),
    path("week-timings", talentView.FetchWeeklyTimingsView.as_view()),
    path("day-slots", talentView.GetSlotsByDateView.as_view()),

]
