from django.contrib import admin
from rest_framework import routers
from django.urls import path, include
from site_api.api import ProductApiList, UserViewSet, \
    ProductDetailApi, CategoryApiList


router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = router.urls + [
    path('products/', ProductApiList.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailApi.as_view(), name='products_detail_api'),
    path('category/', CategoryApiList.as_view(), name='category'),
    ]
