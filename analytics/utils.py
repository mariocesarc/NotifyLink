import requests
from django.conf import settings


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_telegram_message(user, message):
    if user.telegram_chat_id:
        url = 'https://api.telegram.org/bot{}/sendMessage'.format(settings.TELEGRAM_BOT_TOKEN)
        data = {
            'chat_id': user.telegram_chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, data=data)
        return response.status_code == 200
    else:
        return False
