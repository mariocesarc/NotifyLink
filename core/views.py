from django.shortcuts import render
from core.models import SubscriptionPlan


def main_page(request):
    plans = SubscriptionPlan.objects.order_by('price')
    return render(request, 'main.html', {'plans': plans})


def sign_in(request):
    return render(request, '')


def sign_up(request):
    return render(request, '')
