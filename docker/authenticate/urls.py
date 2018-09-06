from django.urls import path
from .views import RegisterUserView, Profile


urlpatterns = [
    path('/register', RegisterUserView.as_view(), name='register'),
    path('/my-profile', Profile.as_view(), name='my-profile')
]
