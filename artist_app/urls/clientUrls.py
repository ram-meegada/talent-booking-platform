from django.urls import path
from artist_app.views import clientView,adminView

urlpatterns = [
    path("signup", clientView.SignUpView.as_view()),
    path("verify-otp", clientView.VerifyOtpViaMailView.as_view()),
    path("log-in", clientView.LogInView.as_view()),
    path("resend-otp",clientView.ResendOtpView.as_view()),

    ################# ADDRESS-MANAGE #########################
    path("address",clientView.AddClientNewAddressDetailsView.as_view()),
    path("address-details/<int:id>",clientView.EditClientAddressDetailsView.as_view()),
    path("all-address",clientView.ShowAllAddressesDetailsView.as_view()),
    path("delete-address/<int:id>",clientView.DeleteClientAddressDetailsBYIDView.as_view()),

    #################### category listing #####################
    path("category",clientView.ListingAllCategories.as_view()),
    path("sub-categories",clientView.ListingAllSubCategoriesBasedOnCategories.as_view()),

    ############### booking #####################
    path("talent-detials", clientView.ListingAllTalent.as_view()),
    path("talent-detials-by-id/<int:id>",clientView.TalentDetailsById.as_view()),
    path("book-talent",clientView.BookTalentView.as_view()),
    path("talent-slots-by-date", clientView.GetTalentSlotsView.as_view()),
    path("fetch-booking-details/<int:id>",clientView.GetAllBookTalentDetails.as_view()),
    path("all-services/<int:id>", clientView.FetchAllTalentServicesView.as_view()),
    
    
    

]