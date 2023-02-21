from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from .serializers import UserRegisterSerializer, UserSerializer, UserChangePasswordSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User


class UserRegisterApiView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        return serializer.save()


class GetMe(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UpdateProfile(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserChangePassword(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_pass = request.data.get('old_password')
        new_pass = request.data.get('new_password')
        if instance.check_password(old_pass):
            instance.password = make_password(new_pass)
            instance.save()
            return Response(status=status.HTTP_200_OK, data={'message': 'Password changed successfully.'})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Password is wrong!'})
