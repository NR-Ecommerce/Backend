from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from .serializers import OrderSerializer, OrderMiniSerializer
from .models import Order, OrderItem, ShippingAddress
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from store.models import Product
from datetime import datetime


class OrderListApiView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]


class DestroyOrder(DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        return Order.objects.get(pk=self.kwargs['pk'])


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

        # Calculating the final price
        for i in orderItems:
            product = Product.objects.get(pk=i['product'])
            total_price += product.price
        total_price += data['shipping_address']['shipping_price']

        # Creating Order
        order = serializer.save(user=self.request.user, total_price=total_price)

        # Creating shipping address
        ShippingAddress.objects.create(
            order=order,
            state_id=data['shipping_address']['state_id'],
            city_id=data['shipping_address']['city_id'],
            detail=data['shipping_address']['detail'],
            post_code=data['shipping_address']['post_code'],
            shipping_price=data['shipping_address']['shipping_price'],
            phone_number=data['shipping_address']['phone_number']
        )

        # Creating each order items
        for i in orderItems:
            product = Product.objects.prefetch_related('images').get(pk=i['product'])

            item = OrderItem.objects.create(
                order=order,
                product=product,
                title=product.title,
                image=product.images.first().image.url,
                color=i['color'],
                size=i['size'],
                price=product.price,
                qty=i['qty']
            )
            product.stock -= item.qty
            product.total_sold += 1
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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == 'پرداخت شده':
            instance.status = 'در حال آماده سازی'
            instance.save()
            return Response(status=status.HTTP_200_OK, data={'message': 'status changed successfully'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'you cant change this status!'})


class UpdateOrderToPosted(UpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser]

    def get_object(self):
        return Order.objects.get(pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == 'در حال آماده سازی':
            instance.status = 'ارسال شده'
            instance.posted_at = datetime.now()
            instance.save()
            return Response(status=status.HTTP_200_OK, data={'message': 'status changed successfully'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'you cant change this status!'})


class UpdateOrderToDelivered(UpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser]

    def get_object(self):
        return Order.objects.get(pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == 'ارسال شده':
            instance.status = 'تحویل داده شده'
            instance.delivered_at = datetime.now()
            instance.save()
            return Response(status=status.HTTP_200_OK, data={'message': 'status changed successfully'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'you cant change this status!'})
# Create your views here.
