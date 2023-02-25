from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from .serializers import OrderSerializer, OrderMiniSerializer
from .models import Order, OrderItem, ShippingAddress
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from store.models import Product
from datetime import datetime


class CreateOrderApiView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        data = self.request.data
        orderItems = data['order_items']
        total_price = 0
        if orderItems and len(orderItems) == 0:
            return Response(data={'message': 'No order items'}, status=status.HTTP_400_BAD_REQUEST)
        for i in orderItems:
            product = Product.object.get(pk=i['product'])
            total_price += product.price
        total_price += data['shipping_address']['shipping_price']
        order = serializer.save(user=self.request.user, total_price=total_price)
        ShippingAddress.object.create(
            order=order,
            state__id=data['shipping_address']['state_id'],
            city__id=data['shipping_address']['city_id'],
            detail=data['shipping_address']['detail'],
            post_code=data['shipping_address']['post_code'],
            shipping_price=data['shipping_address']['shipping_price'],
            phone_number=data['shipping_address']['phone_number']
        )

        for i in orderItems:
            product = Product.objects.prefetch_related('images').get(pk=i['product'])

            item = OrderItem.objects.create(
                order=order,
                product=product,
                title=product.title,
                image=product.images[0].url,
                color=i['color'],
                size=i['size'],
                qty=i['qty']
            )
            product.stock -= item.qty
            product.save()

        return Response(serializer.data)


class MyOrdersApiView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderMiniSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class OrderByIDApiView(RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            order = Order.objects.get(pk=self.kwargs['pk'])
            if self.request.user.is_staff or order.user == self.request.user:
                return order
            else:
                return Response(data={'message': 'User no authorize to view this order.'},
                                status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response(data={'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


class UpdateOrderToPrep(UpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser]

    def get_object(self):
        return Order.objects.get(pk=self.kwargs['pk'])

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'در حال آماده سازی'
        instance.save()


class UpdateOrderToPosted(UpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser]

    def get_object(self):
        return Order.objects.get(pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'ارسال شده'
        instance.posted_at = datetime.now()
        instance.save()


class UpdateOrderToDelivered(UpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser]

    def get_object(self):
        return Order.objects.get(pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'تحویل داده شده'
        instance.delivered_at = datetime.now()
        instance.save()
# Create your views here.
