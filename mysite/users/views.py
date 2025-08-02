from rest_framework import viewsets, generics, status
from .serializers import *
from .models import *
from halal_app.models import Product, Order
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import update_session_auth_hash
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from .permissions import IsAdminUserCustom


class SellerAdminViewSet(viewsets.ModelViewSet):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializers
    permission_classes = [IsAdminUser]


    @action(detail=True, methods=['post'], url_path='toggle-block')
    def toggle_block(self, request, pk=None):
        seller = self.get_object()

        seller.is_blocked = not seller.is_blocked
        seller.save()

        status_text = "заблокирован" if seller.is_blocked else "разблокирован"
        return Response({
            "message": f"Продавец {seller.full_name} был {status_text}.",
            "is_blocked": seller.is_blocked
        })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def seller_stats(request):
    total = SellerProfile.objects.count()
    blocked = SellerProfile.objects.filter(is_blocked=True).count()

    return Response({
        "total_sellers": total,
        "blocked_sellers": blocked,
        "active_sellers": total - blocked,
        "registered_sellers": total
    })



class RegisterView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer


class CustomLoginView(generics.GenericAPIView):
    serializer_class = CustomLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'detail': 'Невалидный токен'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        update_session_auth_hash(request, request.user)
        return Response({'message': 'Пароль успешно изменён.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_reset_code(request):
    serializer = VerifyResetCodeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Пароль успешно сброшен.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfilesListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfilesSerializer


    def get_queryset(self):
        return UserProfile.objects.filter(username=self.request.user.username)


class UserProfilesDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfilesSerializer


    def get_queryset(self):
        return UserProfile.objects.filter(username=self.request.user.username)


class BuyerProfileViewSet(viewsets.ModelViewSet):
    queryset = BuyerProfile.objects.all()
    serializer_class = BuyerProfileSerializers


class SellerProfileViewSet(viewsets.ModelViewSet):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializers


class AdminDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserCustom]

    def get(self, request):
        users_count = UserProfile.objects.count()
        sellers_count = SellerProfile.objects.count()
        products_count = Product.objects.count()
        orders_count = Order.objects.count()

        return Response({
            "users": users_count,
            "sellers": sellers_count,
            "products": products_count,
            "orders": orders_count,
        })
