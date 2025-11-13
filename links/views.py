import secrets
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from links.models import Link, PageTheme
from links.utils import is_valid_url

User = get_user_model()


@require_GET
def get_user_page(request, username):
    user = get_object_or_404(User, username=username)

    links = Link.objects.filter(user=user, is_active=True).order_by('order')

    context = {
        'user': user,
        'links': links,
        'page_theme': user.page_theme
    }
    return render(request, 'links/user_page.html', context)


@login_required
@require_GET
def config_page(request):
    user = request.user

    links = Link.objects.filter(user=user).order_by('order')

    themes = PageTheme.objects.all()

    context = {
        'user': user,
        'links': links,
        'page_theme': user.page_theme,
        'themes': themes,
    }
    return render(request, 'links/config_page.html', context)


@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        
        display_name = request.POST.get('display_name', '').strip()
        bio = request.POST.get('bio', '').strip()
        theme_id = request.POST.get('theme_id')
        notifications_enabled = request.POST.get('notifications_enabled') == '1'
        
        user.display_name = display_name
        user.bio = bio
        user.notifications_enabled = notifications_enabled
        
        if theme_id:
            try:
                theme = PageTheme.objects.get(id=theme_id)
                user.page_theme = theme
            except PageTheme.DoesNotExist:
                pass
        
        if 'avatar' in request.FILES:
            avatar_file = request.FILES['avatar']
            max_size = 5 * 1024 * 1024  # max 5MB
            if avatar_file.size > max_size:
                return render_error_with_state(request, 'El archivo de avatar es demasiado grande. El tamaño máximo permitido es 5MB.')
            user.avatar = avatar_file
        elif request.POST.get('clear_avatar'):
            user.avatar = None
        
        user.save()
        
        # return updated preview with success message
        preview_html = render_to_string('links/partials/preview.html', {
            'user': user,
            'links': Link.objects.filter(user=user, is_active=True).order_by('order'),
            'page_theme': user.page_theme
        })
        
        success_script = render_to_string('links/partials/success_script.html')
        
        return render(request, 'links/partials/preview_update.html', {
            'preview_html': preview_html,
            'success_script': success_script
        })
    
    return render_preview(request)


@login_required
@require_POST
def add_link(request):
    user = request.user
    
    name = request.POST.get('name', '').strip()
    url = request.POST.get('url', '').strip()
    link_type = request.POST.get('type', 'generic')
    
    if name and url:
        # validate URL format
        if not is_valid_url(url):
            return render_error_with_state(request, 'Formato de URL inválido. Por favor ingresa una URL válida como "ejemplo.com" o "https://ejemplo.com"')
            
        # ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        Link.objects.create(
            user=user,
            name=name,
            link=url,
            type=link_type
        )
    
    return render_links_and_preview(request)


@login_required
@require_POST
def delete_link(request, link_id):
    user = request.user

    link = Link.objects.get(id=link_id, user=user)
    link.delete()

    return render_links_and_preview(request)


@login_required
@require_POST
def toggle_link(request, link_id):
    user = request.user

    link = Link.objects.get(id=link_id, user=user)
    link.is_active = not link.is_active
    link.save()

    return render_links_and_preview(request)


@login_required
@require_POST
def move_link(request, link_id):
    user = request.user

    direction = request.POST.get('direction')

    link = Link.objects.get(id=link_id, user=user)
    current_order = link.order

    if direction == 'up' and current_order > 1:
        link.move_to(current_order - 1)
    elif direction == 'down':
        max_order = Link.objects.filter(user=user).count()
        if current_order < max_order:
            link.move_to(current_order + 1)

    return render_links_and_preview(request)


@login_required
@require_POST
def update_link(request, link_id):
    user = request.user

    link = Link.objects.get(id=link_id, user=user)

    name = request.POST.get('name', '').strip()
    url = request.POST.get('url', '').strip()
    link_type = request.POST.get('type', 'generic')

    if name and url:
        # Validate URL format
        if not is_valid_url(url):
            return render_error_with_state(request, 'Formato de URL inválido. Por favor ingresa una URL válida como "ejemplo.com" o "https://ejemplo.com"')

        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        link.name = name
        link.link = url
        link.type = link_type
        link.save()

    return render_links_and_preview(request)


def render_error_with_state(request, error_message):
    user = request.user

    links = Link.objects.filter(user=user).order_by('order')
    active_links = links.filter(is_active=True)

    error_html = render_to_string('links/partials/error_message.html', {
        'error_message': error_message
    })
    
    links_html = render_to_string('links/partials/links_list.html', {
        'links': links
    })
    
    preview_html = render_to_string('links/partials/preview.html', {
        'user': user,
        'links': active_links,
        'page_theme': user.page_theme
    })
    
    return render(request, 'links/partials/error_with_preview.html', {
        'error_html': error_html,
        'links_html': links_html,
        'preview_html': preview_html
    })


def render_links_and_preview(request):
    user = request.user

    links = Link.objects.filter(user=user).order_by('order')
    active_links = links.filter(is_active=True)

    links_html = render_to_string('links/partials/links_list.html', {
        'links': links
    })
    
    preview_html = render_to_string('links/partials/preview.html', {
        'user': user,
        'links': active_links,
        'page_theme': user.page_theme
    })
    
    return render(request, 'links/partials/links_with_preview.html', {
        'links_html': links_html,
        'preview_html': preview_html
    })


def render_preview(request):
    user = request.user

    active_links = Link.objects.filter(user=user, is_active=True).order_by('order')
    
    return render(request, 'links/partials/preview.html', {
        'user': user,
        'links': active_links,
        'page_theme': user.page_theme
    })


@login_required
@require_POST
def telegram_connect(request):
    user = request.user

    verification_token = secrets.token_urlsafe(12)

    user.telegram_token = verification_token
    user.token_expires = timezone.now() + timedelta(minutes=10)
    user.save()

    return render(request, 'links/partials/telegram_instructions.html', {
        'verification_code': verification_token,
        'bot_username': 'notifylink_bot'  # Replace with your bot username
    })


@login_required
@require_POST
def telegram_check(request):
    user = request.user
    
    if user.telegram_chat_id:
        return render(request, 'links/partials/telegram_success.html')
    else:
        return render(request, 'links/partials/telegram_pending.html')


@login_required
@require_POST
def telegram_disconnect(request):
    user = request.user
    user.telegram_chat_id = ''
    user.telegram_token = None
    user.token_expires = None
    user.save()

    return render(request, 'links/partials/page_reload.html')
