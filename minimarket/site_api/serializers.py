from django.contrib.auth.models import User
from rest_framework import serializers
from products.models import Category, Product, ProductPhoto, Property, PropertyProduct


class UserSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_staff', 'username', 'email']


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'icon_photo']


class PropertyProductSerialaizers(serializers.ModelSerializer):
    class Meta:
        model = PropertyProduct
        fields = "__all__"


class PropertySerialaizers(serializers.ModelSerializer):
    class Meta:
        value = PropertyProductSerialaizers(many=True, read_only=True)
        model = Property
        fields = "__all__"


class ProductProfileSerializers(serializers.ModelSerializer):
    product_photo = serializers.StringRelatedField(many=True)
    # properties = serializers.StringRelatedField(many=True)
    properties = PropertySerialaizers(many=True, read_only=True)
    category = serializers.StringRelatedField()
    # category = serializers.SerializerMethodField('product')
    #
    # def product_in_shop(self, request):
    #     queryset = []
    #     for i in ProductInShop.objects.filter(name_id=request.id):
    #         queryset.append({'shop_id': i.in_shop.id, 'shop_name': i.in_shop.name, 'amount': i.amount})
    #     return queryset

    class Meta:
        model = Product
        # queryset = Product.objects.all().select_related('category').prefetch_related("product_photo")
        fields = ['id', 'article', 'category', 'name', 'properties',
                  'description', "product_photo", 'price', 'amount']  # , 'in_shop']'photo',
