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


class PropertySerializers(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"


class PropertyProductSerializers(serializers.ModelSerializer):
    property = serializers.StringRelatedField()

    class Meta:
        # value = PropertySerializers(many=True, read_only=True)
        model = PropertyProduct
        fields = ['property', 'value']


class ProductProfileSerializers(serializers.ModelSerializer):
    product_photo = serializers.StringRelatedField(many=True)
    # properties = serializers.StringRelatedField(many=True)
    product_properties = PropertyProductSerializers(many=True, read_only=True)
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['id', 'article', 'category', 'name',  # 'properties',
                  'description', "product_photo", 'price', 'amount', 'product_properties']  # , 'in_shop']'photo',
