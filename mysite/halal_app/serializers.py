from rest_framework import serializers
from .models import (Category, Brand, Product, ProductImage, Customer, Order, OrderItem, Review, Save,
                     SaveItem, Cart, CartItem)
from users.serializers import SellerProfileSerializers, BuyerProfileSerializers


class RecursiveCategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='category_name')
    image = serializers.ImageField(source='category_image')
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['title', 'image', 'subcategories']

    def get_subcategories(self, obj):
        if obj.subcategories.exists():
            return RecursiveCategorySerializer(obj.subcategories.all(), many=True).data
        return []


class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class CategoryDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='category_name')
    image = serializers.ImageField(source='category_image')
    subcategories = RecursiveCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'subcategories']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'rating', 'customer', 'comment', 'reply', 'created_at']


class ProductListSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(read_only=True, many=True)
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price', 'weight', 'images']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    review = ReviewSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = "__all__"


class SaveItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveItem
        fields = "__all__"


class SaveItemListSerializer(serializers.ModelSerializer):
    products = ProductListSerializer()

    class Meta:
        model = SaveItem
        fields = ['id', 'products']


class SaveSerializer(serializers.ModelSerializer):
    buyer_saves = SaveItemListSerializer(many=True, read_only=True)
    user_save = BuyerProfileSerializers()

    class Meta:
        model = Save
        fields = ['id', 'user_save', 'buyer_saves']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"


class CartItemListSerializer(serializers.ModelSerializer):
    items = ProductListSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'items', 'cart', 'quantity', 'status']


class CartSerializer(serializers.ModelSerializer):
    total_product_count = serializers.SerializerMethodField()
    cart_items = CartItemListSerializer(many=True, read_only=True)
    user_cart = BuyerProfileSerializers()

    class Meta:
        model = Cart
        fields = ['id', 'user_cart', 'total_product_count', 'cart_items']

    def get_total_product_count(self, obj):
        return obj.get_total_product_count()

