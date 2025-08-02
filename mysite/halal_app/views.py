from rest_framework import generics, viewsets
from rest_framework import filters
from .models import Category, Product, Save, SaveItem, Cart, CartItem, Review
from .serializers import (
    CategoryDetailSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    CategorySimpleSerializer,
    SaveSerializer,
    SaveItemSerializer,
    SaveItemListSerializer,
    CartSerializer,
    CartItemSerializer,
    CartItemListSerializer,
    ReviewSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategoryDetailSerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = 'pk'


class ProductListByCategoryView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']  # По каким полям ищем

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        queryset = Product.objects.filter(category_id=category_id)

        # Фильтр поиска применяется автоматически через filter_backends
        return queryset

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'pk'


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class SaveViewSet(viewsets.ModelViewSet):
    queryset = Save.objects.all()
    serializer_class = SaveSerializer


class SaveItemCreateApiView(generics.CreateAPIView):
    serializer_class = SaveItemSerializer


class SaveItemListApiView(generics.ListAPIView):
    queryset = SaveItem.objects.all()
    serializer_class = SaveItemListSerializer


class SaveItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SaveItem.objects.all()
    serializer_class = SaveItemListSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemCreateAPIView(generics.CreateAPIView):
    serializer_class = CartItemSerializer


class CartItemListApiView(generics.ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemListSerializer


class CartItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemListSerializer


class CartItemStatusListApiView(generics.ListAPIView):
    queryset = CartItem.objects.filter(status='в пути')
    serializer_class = CartItemListSerializer


class CartItemStatusDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.filter(status='в пути')
    serializer_class = CartItemListSerializer

