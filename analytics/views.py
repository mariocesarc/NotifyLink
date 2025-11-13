from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST, require_GET

from analytics.models import LinkClick, ClickNotification
from analytics.utils import get_client_ip, send_telegram_message
from links.models import Link

User = get_user_model()


@require_POST
def count_link_click(request, link_uuid):

    link = Link.objects.select_related('user').get(id=link_uuid, is_active=True)

    # extract analytics data
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    ip_address = get_client_ip(request)

    # create click record
    link_click = LinkClick.objects.create(
        link=link,
        ip_address=ip_address,
        user_agent=user_agent,
        click_count=1
    )

    if link.user.notifications_enabled and link.user.remaining_notifications > 0:

        ## send telegram notification

        user = link.user
        user.remaining_notifications = user.remaining_notifications - 1
        user.save()

        message = 'La ip {} visitó tu link **{}**'.format(link_click.ip_address, link.name)
        success = send_telegram_message(user, message)

        click_notification = ClickNotification.objects.create(
            type=ClickNotification.Type.TELEGRAM,
            link=link,
        )
        click_notification.success = success
        click_notification.save()

    return JsonResponse({
        'success': True,
        'redirect_url': link.link,
        'link_name': link.name
    })


@never_cache
@login_required
@require_GET
def dashboard(request):
    user = request.user

    now = timezone.now()

    day_start = now - timedelta(days=1)
    week_start = now - timedelta(days=7)
    month_start = now - timedelta(days=30)

    day_stats = LinkClick.objects.filter(link__user=user, timestamp__gte=day_start)\
        .values('link__name', 'link__id')\
        .annotate(total_clicks=Sum('click_count'))\
        .order_by('-total_clicks')

    week_stats = LinkClick.objects.filter(link__user=user, timestamp__gte=week_start)\
        .values('link__name', 'link__id')\
        .annotate(total_clicks=Sum('click_count'))\
        .order_by('-total_clicks')

    month_stats = LinkClick.objects.filter(link__user=user, timestamp__gte=month_start)\
        .values('link__name', 'link__id')\
        .annotate(total_clicks=Sum('click_count'))\
        .order_by('-total_clicks')

    total_day_clicks = sum(stat['total_clicks'] for stat in day_stats)
    total_week_clicks = sum(stat['total_clicks'] for stat in week_stats)
    total_month_clicks = sum(stat['total_clicks'] for stat in month_stats)
    
    context = {
        'day_stats': day_stats,
        'week_stats': week_stats,
        'month_stats': month_stats,
        'total_day_clicks': total_day_clicks,
        'total_week_clicks': total_week_clicks,
        'total_month_clicks': total_month_clicks,
        'user': user,
    }
    
    return render(request, 'analytics/dashboard.html', context)
