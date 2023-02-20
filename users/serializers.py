from rest_framework import serializers
from .models import User


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
