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
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'phone_number': str(user.phone_number) if user.phone_number else None,
            'role': user.role,
            'avatar': user.avatar.url if user.avatar else None,
        }
        return Response(data)



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




class SendEmailCodeView(APIView):
    def post(self, request):
        serializer = SendEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user, created = User.objects.get_or_create(email=email, defaults={'username': email})

        code = EmailVerification.generate_code()
        EmailVerification.objects.create(user=user, code=code)

        try:
            send_mail(
                subject='Код подтверждения',
                message=f'Ваш код подтверждения: {code}',
                from_email='your_email@gmail.com',
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Код отправлен на email."}, status=status.HTTP_200_OK)




class VerifyEmailCodeView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)

        try:
            verification = EmailVerification.objects.filter(
                user=user, code=code, is_used=False
            ).latest('created_at')
        except EmailVerification.DoesNotExist:
            return Response({"error": "Неверный код."}, status=status.HTTP_400_BAD_REQUEST)

        if verification.is_expired():
            return Response({"error": "Код истёк."}, status=status.HTTP_400_BAD_REQUEST)

        verification.is_used = True
        verification.save()

        user.is_active = True  # или user.email_verified = True, если у тебя есть такое поле
        user.save()

        return Response({"message": "Email успешно подтверждён."}, status=status.HTTP_200_OK)