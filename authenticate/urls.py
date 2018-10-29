from django.urls import path
from .views import Profile, LoginView, UserViews, user_patch_delete, password

urlpatterns = [
    path('my-profile/', Profile.as_view(), name='my-profile'),
    path('login/', LoginView.as_view(), name="login"),

    # admins only
    path('password/', password, name='password'),
    # changing the user informations or delete it
    path('<int:pk>', user_patch_delete, name='user-edit'),
    # POST for creating new users
    path('', UserViews.as_view(), name="user")
]
