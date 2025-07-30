from django.contrib import admin
from .models import *
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import SellerProfile, UserProfile
from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from .models import SellerProfile


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'full_name', 'email', 'phone_number', 'is_blocked')
    list_filter = ('is_blocked',)
    search_fields = ('name_shop', 'user__first_name', 'user__last_name', 'user__email', 'user__phone_number')

    actions = ['block_sellers', 'unblock_sellers']

    def shop_name(self, obj):
        return obj.name_shop
    shop_name.admin_order_field = 'name_shop'
    shop_name.short_description = 'Название магазина'

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    full_name.admin_order_field = 'user__first_name'
    full_name.short_description = 'ФИО'

    def email(self, obj):
        return obj.user.email
    email.admin_order_field = 'user__email'
    email.short_description = 'Email'

    def phone_number(self, obj):
        return obj.user.phone_number
    phone_number.admin_order_field = 'user__phone_number'
    phone_number.short_description = 'Телефон'

    def block_sellers(self, request, queryset):
        updated = queryset.update(is_blocked=True)
        self.message_user(request, f"{updated} продавцов заблокированы.")
    block_sellers.short_description = "Заблокировать выбранных продавцов"

    def unblock_sellers(self, request, queryset):
        updated = queryset.update(is_blocked=False)
        self.message_user(request, f"{updated} продавцов разблокированы.")
    unblock_sellers.short_description = "Разблокировать выбранных продавцов"


admin.site.register(UserProfile)
admin.site.register(BuyerProfile)
