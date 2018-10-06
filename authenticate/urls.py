from django.urls import path
from .views import Profile, LoginView, UserViews, user_patch_delete

urlpatterns = [
    path('my-profile/', Profile.as_view(), name='my-profile'),
    path('login/', LoginView.as_view(), name="login"),

    # admins only
    path('<int:pk>', user_patch_delete, name='user-edit'),
    path('', UserViews.as_view(), name="user")
]
