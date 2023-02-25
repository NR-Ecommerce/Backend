from .views import CreateOrderApiView, MyOrdersApiView, OrderByIDApiView, UpdateOrderToPrep, UpdateOrderToDelivered, \
    UpdateOrderToPosted, OrderListApiView, DestroyOrder
from django.urls import path

urlpatterns = [
    path('', OrderListApiView.as_view(), name='orders'),
    path('create/', CreateOrderApiView.as_view(), name='create_order'),
    path('delete/<int:pk>/', DestroyOrder.as_view(), name='delete'),
    path('my-order/', MyOrdersApiView.as_view(), name='my_order'),
    path('get/<int:pk>', OrderByIDApiView.as_view(), name='get_order'),
    path('update/prep/<int:pk>', UpdateOrderToPrep.as_view(), name='prep_order'),
    path('update/posted/<int:pk>', UpdateOrderToPosted.as_view(), name='post_order'),
    path('update/delivered/<int:pk>', UpdateOrderToDelivered.as_view(), name='delivered_order'),
]
