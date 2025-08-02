from django.urls import path, include
from rest_framework import routers
from django.urls import path
from .views import (
    CategoryListView,
    CategoryDetailView,
    ProductListByCategoryView,
    ProductDetailView,
    SaveViewSet,
    CartViewSet,
    SaveItemListApiView,
    SaveItemCreateApiView,
    SaveItemDetailAPIView,
    CartItemListApiView,
    CartItemCreateAPIView,
    CartItemDetailAPIView,
    CartItemStatusListApiView,
    CartItemStatusDetailApiView,
    ReviewViewSet
)

router = routers.SimpleRouter()
router.register(r'save', SaveViewSet, basename='savee')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'review', ReviewViewSet, basename='review')



urlpatterns = [
    path('', include(router.urls)),

    path('save_item/create/', SaveItemCreateApiView.as_view(), name='save_item_create'),
    path('save_item/', SaveItemListApiView.as_view(), name='save_item_list'),
    path('save_item/<int:pk>/', SaveItemDetailAPIView.as_view(), name='save_item_detail'),
    path('cart_item/create/', CartItemCreateAPIView.as_view(), name='cart_item_create'),
    path('cart_item/', CartItemListApiView.as_view(), name='cart_item_list'),
    path('cart_item/<int:pk>/', CartItemDetailAPIView.as_view(), name='cart_item_detail'),

    path('categories/', CategoryListView.as_view(), name='category-list'),                  # без подкатегорий
    # path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),     # с подкатегориями
    path('categories/<int:category_id>/products/', ProductListByCategoryView.as_view(), name='products-by-category'),

    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    path('cart_status/', CartItemStatusListApiView.as_view(), name='cart_current_status'),
    path('cart_status/<int:pk>/', CartItemStatusDetailApiView.as_view(), name='cart_current_status_detail'),
]