from rest_framework import viewsets
from django.contrib.auth.models import User
from products.models import Category, Product
from site_api.serializers import UserSerializers, ProductProfileSerializers, CategorySerializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductProfileSerializers


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
