from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import OrderSerializer
from .models import Order, OrderItem, ShippingAddress
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from store.models import Product


class CreateOrderApiView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        data = self.request.data
        orderItems = data['order_items']
        total_price = 0
        if orderItems and len(orderItems)==0:
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
# Create your views here.
