from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, \
    UpdateModelMixin, DestroyModelMixin
from products.models import Category, Product, ProductPhoto, Property, PropertyProduct, PropertyCategory
from site_api.serializers import UserSerializers, ProductProfileSerializers, CategorySerializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class ProductApiList(ListModelMixin, CreateModelMixin, GenericAPIView):
    """
    Представление для получения списка товаров
    """
    queryset = Product.objects.all()[:50]  # .select_related('category').prefetch_related("product_photo")[:50]
    serializer_class = ProductProfileSerializers

    def get(self, request):
        return self.list(request)

    def get_queryset(self):  # фильтрация
        queryset = Product.objects.all()
        name = self.request.query_params.get('name', 0)
        category = self.request.query_params.get('category', 0)
        if name and category:
            queryset = Product.objects.filter(name=name, category=category)
        elif name:
            queryset = Product.objects.filter(name=name)
        elif category:
            queryset = Product.objects.filter(category=category)
        return queryset

    def post(self, request):
        return self.create(request)


class ProductDetailApi(UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    """
    Представление для получения детальной информации о товаре,
    а также для его редактирования и удаления
    """
    queryset = Product.objects.all()
    serializer_class = ProductProfileSerializers

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CategoryApiList(ListModelMixin, CreateModelMixin, GenericAPIView):
    """
    Представление для получения списка магазинов
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    def get(self, request):
        return self.list(request)

    def get_queryset(self):  # фильтрация
        queryset = Category.objects.all()
        name = self.request.query_params.get('name', 0)
        if name:
            queryset = Category.objects.filter(name=name)
        return queryset

    def post(self, request):
        return self.create(request)
