from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

from links.models import Link

User = get_user_model()


def get_user_page(request, username):
    user = get_object_or_404(User, username=username)

    links = Link.objects.filter(user=user, is_active=True).order_by('order')

    context = {
        'user': user,
        'links': links,
        'page_theme': user.page_theme
    }

    return render(request, 'links/user_page.html', context)
