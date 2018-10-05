from django.urls import path
from .views import Profile, LoginView


urlpatterns = [
    path('my-profile/', Profile.as_view(), name='my-profile'),
    path('login/', LoginView.as_view(), name="login"),
]
