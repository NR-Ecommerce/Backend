from rest_framework import serializers
from .models import Category, ProductType, ProductProp, Product, ProductPropValue, ProductImage, ProductDetail
from utils.serializers import ColorSerializer, SizeSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = __all__


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = __all__


class ProductPropSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductProp
        fields = __all__


class ProductPropValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPropValue
        fields = __all__


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = __all__


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = __all__


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    props = ProductPropValueSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    details = ProductDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'title', 'category', 'description', 'stock', 'price', 'is_available', 'created_at'
        )
        read_only_fields(
            'created_at'
        )

