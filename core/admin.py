from django.contrib import admin
from core.models import User, SubscriptionPlan, SubscriptionPayment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'current_plan', 'date_joined', 'is_staff', 'is_superuser')
    exclude = ('password',)
    search_fields = ('username', 'email')


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'billing_cycle')


@admin.register(SubscriptionPayment)
class SubscriptionPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'amount', 'paid_at', 'status')
    search_fields = ('user__username', 'user__email')
