import json
from datetime import datetime

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from analytics.utils import send_telegram_message

User = get_user_model()


@csrf_exempt
def telegram_webhook(request):
    data = json.loads(request.body)

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')

        if text.startswith('/start '):
            token = text.split(' ', 1)[1]

            user = User.objects.get(
                telegram_token=token,
                token_expires__gt=datetime.now()
            )

            # connect the account
            user.telegram_chat_id = str(chat_id)
            user.telegram_token = None
            user.token_expires = None
            user.save()

            send_telegram_message(user, 'Vinculado correctamente!')

            return JsonResponse({'ok': True})

    return JsonResponse({'ok': False})
