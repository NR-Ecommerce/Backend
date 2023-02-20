from django.urls import path
from .views import UserRegisterApiView


urlpatterns = [
    path('register/', UserRegisterApiView.as_view(), name='create_user'),
]
