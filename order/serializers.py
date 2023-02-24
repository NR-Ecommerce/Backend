from rest_framework import serializers
from .models import Order, OrderItem, ShippingAddress
from utils.serializers import ColorSerializer, SizeSerializer, StateSerializer, CitySerializer


class OrderItemSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    size = SizeSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class ShippingAddressSerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address = ShippingAddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'user', 'total_price', 'items', 'address', 'status', 'paid_at', 'posted_at', 'delivered_at'
        )
        read_only_fields = (
            'user', 'status', 'paid_at', 'posted_at', 'delivered_at', 'total_price'
        )
