from django.urls import path
from .views import Profile
from rest_framework.authtoken import views


urlpatterns = [
    path('my-profile/', Profile.as_view(), name='my-profile'),
    path('login/', views.obtain_auth_token),
]
