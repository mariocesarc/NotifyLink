import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from analytics.utils import send_telegram_message

User = get_user_model()


@require_POST
@csrf_exempt
def telegram_webhook(request):
    try:
        data = json.loads(request.body or '{}')
    except Exception:
        return JsonResponse({'ok': False})

    message = data.get('message')
    # ignore if there is no message
    if not isinstance(message, dict):
        return JsonResponse({'ok': True})

    text = message.get('text', '')
    chat_id = (message.get('chat') or {}).get('id')

    if text.startswith('/start '):
        token = text.split(' ', 1)[1]
        user = User.objects.filter(telegram_token=token, token_expires__gt=timezone.now()).first()
        if user:
            user.telegram_chat_id = str(chat_id) if chat_id else ''
            user.telegram_token = ''
            user.token_expires = None
            user.save()
            send_telegram_message(user, 'vinculado correctamente!')

    return JsonResponse({'ok': True})
