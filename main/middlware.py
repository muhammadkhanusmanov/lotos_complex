# middleware.py
from django.http import JsonResponse
from .models import TelegramUser

class TelegramAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            user_id = request.headers.get('X-Telegram-User-Id') or request.data.get('user_id')
            
            if not user_id:
                return JsonResponse({'error': 'User ID required'}, status=401)
            
            try:
                user = TelegramUser.objects.get(user_id=user_id)
                request.user = user
            except TelegramUser.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        
        return self.get_response(request)