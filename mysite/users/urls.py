from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'users', SellerProfileViewSet, basename='users-list')
router.register(r'buyer', BuyerProfileViewSet, basename='buyer_list')
router.register(r'sellers', SellerAdminViewSet, basename='sellers')



urlpatterns = [
    path('', include(router.urls)),
    path('stats/', seller_stats, name='users-stats'),
    path('admin/dashboard/', AdminDashboardAPIView.as_view(), name='admin-dashboard'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change_password/', change_password, name='change_password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('password_reset/verify_code/', verify_reset_code, name='verify_reset_code'),
    path('user/', UserProfilesListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfilesDetailAPIView.as_view(), name='user_detail'),

    path('send_email/', SendEmailCodeView.as_view(), name='send_email_code'),
    path('verify_email/', VerifyEmailCodeView.as_view(), name='verify_email_code'),

]
