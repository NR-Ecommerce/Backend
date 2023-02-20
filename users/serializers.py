from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'phone_number', 'password', 'first_name', 'last_name',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        user = self.Meta.model.objects.create_user(phone_number=phone_number, first_name=first_name,
                                                   last_name=last_name, password=password)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'phone_number', 'first_name', 'last_name'
        )


class UserChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = (
            'phone_number', 'first_name', 'last_name', 'old_password', 'new_password'
        )
        read_only_fields = (
            'phone_number', 'first_name', 'last_name'
        )

    def update(self, instance, validated_data):
        if instance.check_password(validated_data.get('old_password')):
            instance.password = make_password(validated_data.get('new_password'))
            instance.save()
            return instance
        return serializers.ValidationError('Password is wrong!')
