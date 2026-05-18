import hashlib
import hmac
import json
import urllib.parse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.conf import settings
from apps.accounts.models import User

def validate_telegram_auth(init_data):
    """Validate Telegram WebApp init data"""
    data_dict = {}
    for item in init_data.split('&'):
        key, value = item.split('=', 1)
        data_dict[key] = value
    
    received_hash = data_dict.pop('hash', '')
    
    # Sort keys and create check string
    check_string = '\n'.join(f"{k}={v}" for k, v in sorted(data_dict.items()))
    
    secret_key = hashlib.sha256(settings.TELEGRAM_BOT_TOKEN.encode()).digest()
    computed_hash = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()
    
    return computed_hash == received_hash

def telegram_miniapp_view(request):
    """Telegram Mini App main view"""
    workspace_id = request.GET.get('workspace_id')
    user_id = request.GET.get('user_id')
    context = {
        'workspace_id': workspace_id,
        'user_id': user_id,
    }
    return render(request, 'telegram/miniapp.html', context)

@csrf_exempt
def telegram_auth_view(request):
    """Handle Telegram WebApp authentication"""
    if request.method == 'POST':
        data = json.loads(request.body)
        init_data = data.get('initData')
        
        if validate_telegram_auth(init_data):
            # Parse init data
            parsed = dict(urllib.parse.parse_qsl(init_data))
            user_data = json.loads(parsed['user'])
            
            try:
                user = User.objects.get(telegram_id=user_data['id'])
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=f"tg_{user_data['id']}",
                    telegram_id=user_data['id'],
                    first_name=user_data.get('first_name', ''),
                    last_name=user_data.get('last_name', ''),
                )
            
            login(request, user)
            return JsonResponse({'success': True, 'user_id': user.id})
        
        return JsonResponse({'success': False}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
