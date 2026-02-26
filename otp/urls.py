from django.urls import path
from otp.views import GetOtpView

urlpatterns = [
    path('get-otp/', GetOtpView.as_view(), name='get_otp'),
]