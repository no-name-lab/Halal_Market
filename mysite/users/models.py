from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from phonenumber_field.modelfields import PhoneNumberField



class UserProfile(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('seller', 'Продавец'),
        ('buyer', 'Покупатель'),
    ]

    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(region='KG', unique=True)
    avatar = models.ImageField(upload_to="avatar/", null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = f"Ваш код для сброса пароля: {reset_password_token.key}"

    send_mail(
        subject="Сброс пароля на сайте",
        message=email_plaintext_message,
        from_email="noreply@somehost.local",
        recipient_list=[reset_password_token.user.email],
        fail_silently=False,
    )


class SellerProfile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='seller_profile')
    name_shop = models.CharField(max_length=120, null=True, blank=True)
    categories = models.ManyToManyField('halal_app.Category', blank=True)
    image = models.ImageField(upload_to='marketer_images/', null=True, blank=True)
    description = models.TextField(blank=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.name_shop or self.user.username

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'


class BuyerProfile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='buyer_profile')
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
