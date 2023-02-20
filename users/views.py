from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import UserRegisterSerializer
from rest_framework.permissions import AllowAny
from .models import User


class UserRegisterApiView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        return serializer.save()
# Create your views here.
