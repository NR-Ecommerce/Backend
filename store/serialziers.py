from rest_framework import serializers
from .models import Category, ProductType, ProductProp, Product, ProductPropValue, ProductImage, ProductDetail
from utils.serializers import ColorSerializer, SizeSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'


class ProductPropSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductProp
        fields = '__all__'


class ProductPropValueSerializer(serializers.ModelSerializer):
    product_prop = ProductPropSerializer(read_only=True)

    class Meta:
        model = ProductPropValue
        fields = (
            'id', 'product', 'product_prop', 'value'
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    sizes = SizeSerializer(read_only=True, many=True)

    class Meta:
        model = ProductDetail
        fields = (
            'id', 'product', 'color', 'sizes'
        )


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True)
    props = ProductPropValueSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    details = ProductDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'title', 'category', 'description', 'stock', 'price', 'props', 'images', 'details', 'is_available',
            'created_at'
        )
        read_only_fields = (
            'created_at',
        )
