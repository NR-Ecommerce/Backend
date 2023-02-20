from django.urls import path
from .views import UserRegisterApiView, GetMe, UpdateProfile, UserChangePassword


urlpatterns = [
    path('register/', UserRegisterApiView.as_view(), name='create_user'),
    path('me/', GetMe.as_view(), name='me'),
    path('me/update/', UpdateProfile.as_view(), name='update_profile'),
    path('me/change-password/', UserChangePassword.as_view(), name='change_password')
]
