from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from .models import Product
from .serialziers import ProductSerializer
from rest_framework.permissions import IsAdminUser, AllowAny
from users.perimissions import IsAdminOrReadOnly


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

    def get_queryset(self):
        return self.queryset.filter(is_available=True)
