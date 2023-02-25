from django.urls import path, include
from rest_framework import routers
from .views import ProductViewSet, ProductListApiView

router = routers.DefaultRouter()
router.register('products', ProductViewSet)

urlpatterns = [
    path('', ProductListApiView.as_view(), name='get_product'),
    path('', include(router.urls)),
]
