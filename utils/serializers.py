from rest_framework import serializers
from .models import Color, Size, State, City


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = __all__


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = __all__


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = __all__


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name')
