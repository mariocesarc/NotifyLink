import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST

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
    LinkClick.objects.create(
        link=link,
        ip_address=ip_address,
        user_agent=user_agent,
        click_count=1
    )

    if link.user.notifications_enabled and link.user.remaining_notifications > 0:
        ## send telegram notification
        click_notification = ClickNotification.objects.create(
            type=ClickNotification.Type.TELEGRAM,
            link=link,
        )
        user = link.user
        user.remaining_notifications = user.remaining_notifications - 1
        user.save()
        message = 'La ip {} visitó tu link **{}**'.format(link.ip_address, link.name)
        success = send_telegram_message(user, message)
        click_notification.success = success
        click_notification.save()

    # return success response
    return JsonResponse({
        'success': True,
        'redirect_url': link.link,
        'link_name': link.name
    })
