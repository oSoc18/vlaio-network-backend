from django.urls import path
from .views import Profile, LoginView, UserViews


urlpatterns = [
    path('my-profile/', Profile.as_view(), name='my-profile'),
    path('login/', LoginView.as_view(), name="login"),

    # admins only
    path('', UserViews.as_view(), name="user")
]
