from django.contrib import admin
from core.models import User, SubscriptionPlan, SubscriptionPayment


admin.site.register(User)
admin.site.register(SubscriptionPlan)
admin.site.register(SubscriptionPayment)
