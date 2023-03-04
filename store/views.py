from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from .models import Product
from .serialziers import ProductSerializer
from rest_framework.permissions import IsAdminUser, AllowAny
from users.perimissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Product.objects.prefetch_related('details__sizes').all()

    # def perform_create(self, serializer):


class ProductListApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['price', 'created_at', 'total_sold']
    filterset_class = ProductFilter
    pagination_class = PageNumberPagination
    search_fields = ['title', 'description', 'category__name']

    def get_queryset(self):
        return self.queryset.filter(is_available=True)
