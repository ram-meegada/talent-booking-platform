from django.urls import path
from artist_app.views import clientView

urlpatterns = [
    path("signup/", clientView.SignUpView.as_view()),
    path("verify-otp/", clientView.VerifyOtpViaMailView.as_view()),
    path("login/", clientView.LogInView.as_view()),
    path("resend-otp/",clientView.ResendOtpView.as_view()),
    
    

]